from flask import Flask, request, render_template, jsonify
from sentence_transformers import SentenceTransformer, util
import numpy as np
import torch.nn.functional as F
from keybert import KeyBERT
import torch
import pickle
import os
import json

app = Flask(__name__)
TOP_K = 3

model = SentenceTransformer("all-mpnet-base-v2")
kw_model = KeyBERT(model=model)
device = "cuda" if torch.cuda.is_available() else "cpu"

prior_art_data = []
for filename in os.listdir("patent_data"):
    if filename.endswith(".pkl"):
        try:
            file_path = os.path.join("patent_data", filename)
            with open(file_path, "rb") as f:
                prior_art_data.extend(pickle.load(f))
        except pickle.PickleError as e:
            print(f"Error decoding pickle from {filename}: {e}")
        except Exception as e:
            print(f"An error occurred while processing {filename}: {e}")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    user_invention_description = request.form["invention_description"]

    if not user_invention_description:
        return jsonify({"error": "Invention description is required"}), 400

    # print("User invention description:", user_invention_description)

    # Create embedding of the users invention description.
    user_invention_embedding = model.encode(
        user_invention_description, convert_to_tensor=True
    ).to(device)

    keywords_with_scores = kw_model.extract_keywords(
        user_invention_description,
        keyphrase_ngram_range=(1, 4),
        stop_words="english",
        top_n=10,
    )

    user_keyphrases = [keyword[0] for keyword in keywords_with_scores]
    # vector size 10.
    keyword_weights = torch.tensor([keyword[1] for keyword in keywords_with_scores])

    # 10 X 768 (10 keyphrases, 768 dimensions)
    user_keyword_embeddings = model.encode(user_keyphrases, convert_to_tensor=True).to(
        device
    )

    # Reshape vector to 10X1 matrix of keyword weights.
    keyword_weights = keyword_weights.unsqueeze(1).to(device)

    # (10 X 768) * (10 X 1) -> (10 x 768); each embedding is scaled by its score.
    weighted_embeddings = user_keyword_embeddings * keyword_weights
    weighted_average_embedding = torch.sum(weighted_embeddings, dim=0) / torch.sum(
        keyword_weights, dim=0
    )

    aggregated_user_keyword_embedding = weighted_average_embedding.to(device)

    results = []

    for prior_art in prior_art_data:
        prior_art_abstract_embedding = torch.tensor(prior_art.get("embedding")).to(
            device
        )

        prior_art_keyphrase_embedding = torch.tensor(
            prior_art.get("aggregated_keyword_embedding")
        ).to(device)

        # Dot produuct between abstract and complete user description.
        abstract_similarity = util.cos_sim(
            user_invention_embedding, prior_art_abstract_embedding
        ).item()

        # Dot product between keywords in user description and keywords in prior art.
        keyphrase_similarity = util.cos_sim(
            aggregated_user_keyword_embedding,
            prior_art_keyphrase_embedding,
        ).item()

        overall_similarity = 0.7 * abstract_similarity + 0.3 * keyphrase_similarity

        if overall_similarity >= 0.3:
            print(
                (
                    f"Title: {prior_art.get("title")} \n "
                    f"Keyword similarity: {keyphrase_similarity:.4f} | "
                    f"Abstract similarity: {abstract_similarity:.4f} | "
                    f"overall similarity: {overall_similarity:.4f}"
                    f"\nPrior art keywords: {prior_art.get('keywords', [])} \n"
                    f"\nUser keywords: {user_keyphrases}"
                )
            )
            results.append(
                {
                    "title": prior_art.get("title"),
                    "abstract": prior_art.get("abstract"),
                    "similarity": f"{overall_similarity:.4f}",
                    "unified_patents_link": prior_art.get("unified_patents_link"),
                }
            )
    results_sorted = sorted(results, key=lambda x: x["similarity"], reverse=True)
    if not results_sorted:
        return jsonify({"error": "No similar prior art found"}), 404

    top_k_results = results_sorted[:TOP_K]
    return render_template(
        "results.html",
        invention_description=user_invention_description,
        results=top_k_results,
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
