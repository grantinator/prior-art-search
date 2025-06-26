from sentence_transformers import SentenceTransformer, util
from keybert import KeyBERT
import pickle
import torch
import json
import uuid
import re

device = "cuda" if torch.cuda.is_available() else "cpu"

try:
    with open("bquxjob_35bbf224_197a82853c9.json", "r") as f:
        patent_data = json.load(f)
except Exception as e:
    print(f"Error loading JSON file: {e}")
    exit(1)

# Load a pre-trained embedding model and keyBERT.
model = SentenceTransformer("all-mpnet-base-v2")
kw_model = KeyBERT(model=model)

debug = True


def clean_patent_abstract(abstract_text):
    # Define a list of boilerplate phrases to remove
    boilerplate_phrases = [
        "Abstract of the Disclosure",
        "Abstract",
        "disclosed",
        "disclosed herin",
        "of the Disclosure",
        "abstract disclosuer",
        "The present invention relates to",
        "abstract disclosure",
        "Disclosed herein is",
        "disclosed embodiment",
        "TITLE OF THE INVENTION",
        "CARBONLESS MANIFOLD BUSINESS FORMS INVENTOR",
    ]

    cleaned_text = abstract_text

    for phrase in boilerplate_phrases:
        # Use regex to replace the phrase, case-insensitive
        # and handle potential extra spaces/newlines around it
        cleaned_text = re.sub(
            re.escape(phrase.lower()), "", cleaned_text.lower(), flags=re.IGNORECASE
        )

    # Remove multiple spaces, leading/trailing spaces, and newlines
    cleaned_text = re.sub(r"\s+", " ", cleaned_text).strip()
    return cleaned_text


# Process each patent in the patent data.
# Create a url and combine publication number with title.
patents_cleaned = []
for patent in patent_data:

    publication_number = patent.get("publication_number")
    if not publication_number:
        print("Skipping patent with missing publication number.")
        continue

    title = patent.get("title", "")
    publication_number = publication_number.replace("-", "")

    patent["abstract"] = clean_patent_abstract(patent.get("abstract", ""))
    patent["url"] = f"https://patents.google.com/patent/{publication_number}/en"
    patent["title"] = f"{publication_number}: {title}"

    patents_cleaned.append(patent)


# Create embeddings on the clean data.
for patent in patents_cleaned:

    patent["embedding"] = model.encode(patent["abstract"]).tolist()

    keywords_with_scores = kw_model.extract_keywords(
        patent["abstract"],
        keyphrase_ngram_range=(1, 5),
        stop_words="english",
        top_n=10,
    )

    patent["keywords"] = [kw[0] for kw in keywords_with_scores]

    if len(patent.get("keywords")) > 0:
        keyphrases = [keyword[0] for keyword in keywords_with_scores]
        # vector size 10.
        keyword_weights = torch.tensor([keyword[1] for keyword in keywords_with_scores])

        # 10 X 768 (10 keyphrases, 768 dimensions)
        keyword_embeddings = model.encode(keyphrases, convert_to_tensor=True).to(device)

        # Reshape vector to 10X1 matrix of keyword weights.
        keyword_weights = keyword_weights.unsqueeze(1).to(device)

        # (10 X 768) * (10 X 1) -> (10 x 768); each embedding is scaled by its score.
        weighted_embeddings = keyword_embeddings * keyword_weights
        weighted_average_embedding = torch.sum(weighted_embeddings, dim=0) / torch.sum(
            keyword_weights, dim=0
        )
        patent["keyword_embeddings"] = keyword_embeddings
        patent["aggregated_keyword_embedding"] = weighted_average_embedding.tolist()
    else:
        patent["keyword_embeddings"] = None
        patent["aggregated_keyword_embedding"] = None

# Save processed patent data.
with open(f"patent_data/prior_art_data-{uuid.uuid4()}.pkl", "wb") as f:
    pickle.dump(patents_cleaned, f)
