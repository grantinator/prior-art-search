import numpy as np
from sentence_transformers import SentenceTransformer


def cosine_similarity(vec1, vec2):
    """Calculates the cosine similarity between two vectors."""
    dot_product = np.dot(vec1, vec2)
    norm_a = np.linalg.norm(vec1)
    norm_b = np.linalg.norm(vec2)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)


# --- 1. Load a Pre-trained Embedding Model ---
print("Loading the embedding model (this may take a moment on first run)...")
model = SentenceTransformer("all-mpnet-base-v2")
print("Model loaded.")


patent_abstract_match = """
    The present invention relates to a box system for keeping medicine 
    and other payloads at a desired temperature for prolonged periods of time. 
    The system generally includes three or more insulating materials between 
    a refrigerant and the payload so that the payload is not cold-shocked by the
    refrigerant but instead maintains a desired temperature range during shipment. 
    An advantage of the box system of certain embodiments of the present 
    disclosure is that the system allows a shipper to use a temperature controlled
    system that is effective in controlling temperature without the need for any
    expensive phase change materials. A box having foldable tabs for securing
    the materials to each other is also disclosed herein.
"""

patent_abstract_similar = """
    The present invention generally relates to an insulated shipping container made 
    entirely of standard recyclable materials for use in transporting heated or cooled payloads. 
    The entire container and its insulation may be placed in a standard recycling bin after use, 
    without any disassembly or separation of materials. The container comprises multiple layers 
    that are easily folded together by the transporter prior to the additional of a payload for 
    delivery to an end user. The container contains multiple formed paper panels that provide a 
    tight seal for insulation purposes.
"""

patent_abstract_no_match = """
    According to some illustrative embodiments, a protective product is provided that includes: 
    at least one expandable slit paper sheet, said at least on expandable slit paper being 
    expanded between opposing ends of said slit paper; a first embossed paper sheet facing said 
    expanded slit paper sheet and a second paper sheet facing an opposite side of said at least one 
    expanded slit paper sheet, at least one of said first embossed paper sheet and said second paper 
    sheet being fixed to said expanded slit paper sheet at the opposing ends of said expanded slit 
    paper sheet and thereby maintaining said expanded paper in its expanded state, said first embossed 
    paper sheet having a plurality of embossings that increase the rigidity of said embossed paper sheet, 
    whereby inhibiting deformation of said embossed paper sheet that is fixed to said expanded slit sheet paper.
"""

no_violation = (
    "This invention is an insulated shipping container system designed to "
    "maintain a desired temperature range for temperature-sensitive goods during transit."
    "The system achieves insulation through the use of a vacuum-sealed double-wall construction, "
    "where the evacuated space between the walls significantly reduces heat transfer. "
    "Inside this vacuum-insulated core, the goods are placed within "
    "a secondary, non-sealed container that provides additional thermal buffering through "
    "the use of a simple air gap. Temperature control is achieved by housing the primary "
    "goods container within the vacuum-insulated walls, and the system is designed for multi-use "
    "and reusability, eliminating the need for single-use refrigerants or complex phase change materials. "
    "The outer shell features an interlocking closure mechanism for secure transport."
)  # Exact match. We expect a high similarity score.
potentional_violation = (
    "This invention is an insulated box system for shipping medical supplies and other temperature-sensitive "
    "items, designed to maintain a stable temperature range for extended periods. The system incorporates at "
    "least two different insulating layers between an internal cooling element and the payload. These insulating "
    "layers are strategically arranged to prevent direct contact cold shock to the payload while ensuring the "
    "desired temperature is maintained. The system is designed to be cost-effective by minimizing the reliance "
    "on expensive phase change materials. The box structure itself includes integrated, snap-fit components for "
    "securing the insulating materials in place."
)
clear_violation = (
    "This invention is a box system specifically designed for maintaining pharmaceuticals and other payloads "
    "at a precise, desired temperature for prolonged periods during shipment. The system incorporates three"
    " distinct insulating materials positioned between a refrigerant source and the payload, carefully "
    "arranged to prevent cold-shocking of the payload and ensure it remains within a specified temperature "
    "range throughout the shipping process. A significant advantage of this box system is its ability to "
    "effectively control temperature without the need for expensive phase change materials. "
    "Furthermore, the box features integrated foldable tabs that securely hold the various insulating "
    "materials in their proper arrangement."
)  # Semantically similar, but different words. Ideally we want to see a match here.


documents = {
    "target_patent": patent_abstract_match,
    "similar_patent": patent_abstract_similar,
    "unrelated_patent": patent_abstract_no_match,
}
queries = {
    "no_violation": no_violation,
    "potentional_violation": potentional_violation,
    "clear_violation": clear_violation,
}

# queries = [no_violation, potentional_violation, clear_violation]

document_to_embeddings = {key: model.encode(value) for key, value in documents.items()}
# Convert queries to embeddings
query_to_embedding = {key: model.encode(value) for key, value in queries.items()}

for query_key, embedding in query_to_embedding.items():
    print(f"\n\n--- Query ---")
    print(f"Query type: {query_key}")
    query_vector = embedding

    for key, document_vector in document_to_embeddings.items():
        print(f"\nComparing with document: {key}")
        similarity = cosine_similarity(query_vector, document_vector)
        print(f"Cosine Similarity with document: {similarity:.4f}\n")

        if similarity > 0.6:
            print(f"Query is semantically similar to the document.")
        elif similarity > 0.3:
            print(f"Query has some semantic similarity to the document.")
        else:
            print(f"Query is not semantically similar to the document.")
