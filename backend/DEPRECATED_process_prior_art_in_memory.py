from sentence_transformers import SentenceTransformer, util
from keybert import KeyBERT
import pickle
import torch


prior_art_data = [
    {
        "publication_number": "US3910441A",
        "title": "Vacuum Insulated Bottle",
        "abstract": "A vacuum insulated bottle utilizing a wide opening vacuum filler is disclosed. A thin walled liner is disposed in the interior of the filler and extends upwardly therefrom to form a narrow mouth opening to the lined interior for providing the pouring and thermal insulating characteristics of a narrow mouth vacuum filler bottle.",
    },
    {
        "publication_number": "US4427123A",
        "title": "Stainless steel thermos bottle",
        "abstract": "A stainless steel thermos bottle comprising inner and outer bottles made of stainless steel, the inner and outer bottles being joined together at tip portions of their bottlenecks to form a double-walled construction, the space created between the two bottles being a vacuum. The surfaces of the inner and outer bottles that surround the space are provided with at least one metal deposit at least on an outer surface of the inner bottle, except for a part or all of the bottleneck surfaces in the space. The part or all of the bottleneck surfaces in the space includes the surface of the joint between the two bottles.",
    },
    {
        "publication_number": "US3456860A",
        "title": "Double wall cup",
        "abstract": "There is disclosed a cup having inner and outer walls drawn from sheets of plastic material and respectively formed with oppositely circumferentially and axially extending ridges which abut each other at spaced points for providing mutual support while minimizing heat transfer between the inner and outer walls",
    },
    {
        "publication_number": "US6405892B1",
        "title": "Thermally Insulated Beverage Glass",
        "abstract": "A thermally insulated beverage glass is provided as an insulated drinking glass made from glass with an interstitial space in the sides and bottom. The sides and bottom of the glass are double-walled, forming an interstitial space for insulating purposes. The interstitial space can be left filled with air, or filled with an insulating material such as Styrofoam®. The interstitial space not only reduces or eliminates condensation from forming on the exterior of the glass when filled with cold liquid on hot, humid days, but it also helps keep the liquid cooler. Alternately, when the glass is filled with hot liquid it also aids in keeping the liquid hotter, longer.",
    },
    {
        "publication_number": "US9139352B2",
        "title": " Insulating container (Cooler Box)",
        "abstract": "An insulating device can include an aperture having a waterproof closure which allows access to the chamber within the insulating device. The closure can help prevent any fluid leakage into and out of the insulating device if the insulating device is overturned or in any configuration other than upright. The closure also prevents any fluid from permeating into the chamber if the insulating device is exposed to precipitation, other fluid, or submersed under water. This construction results in an insulating chamber impervious to water and other liquids when the closure is sealed.",
    },
    {
        "publication_number": "US20080173704A1",
        "title": "US20080173704A1: Container for shipping and storing paper",
        "abstract": "A container for shipping and/or storing a stack of paper is disclosed. The container, according to a disclosed embodiment, comprises a bottom wall and first and second upright, opposing side walls extending from respective edges of the bottom wall. First and second shell portions are connected in a pivotal manner to respective edges of the bottom wall. The shell portions are pivotable toward and away from each to close and open the container, respectively. When the container is closed, the stack is securely contained between the shell portions and the side walls for shipping or storing. When the container is opened, at least two opposing sides of the stack are exposed to facilitate removal of paper from the container. A handle for carrying or lifting the container may be coupled to one of the shell portions.",
    },
    {
        "publication_number": "US9061477B2",
        "title": "US9061477B2: Method and apparatus for making, shipping and erecting boxes",
        "abstract": "A cardboard box with four side panels, four bottom flaps and four top flaps. The box is made from a blank having a first height measured between the outermost edges of the top and bottom flaps. The flaps are rotated into abutting contact with the exterior surface of the panels thereby reducing the overall height of the box to the height of the panel. Adjacent pairs of top and bottom flaps are provided with living hinges that enable them to remain in this position when the box is collapsed. The collapsed box is shipped through the mail in this diminished size and then erected into a box of the same height as the panels.",
    },
    {
        "publication_number": "US6464131B1",
        "title": "US6464131B1: Packing box design (Shipping Carton)",
        "abstract": "The present invention presents an innovative packing box for food-stuffs which may serve as both a shipping carton and as a display box. The carton is constructed from a single, continuous blank of corrugated cardboard or other suitable material. The carton includes inwardly sloping side walls with support ledges to allow for easy stacking of the cartons. The side walls are of folded over design which provides the walls with a double thickness of material for added durability. The carton further includes a front window which provides convenient access to the food-stuffs stored within.",
    },
    {
        "publication_number": "US4279378A",
        "title": "US4279378A: Top gap folding box having a top closure interlock",
        "abstract": "A top gap folding box having four top flaps and a top closure by which the flaps are engaged. Each flap interlocks the adjacent flaps by means of a pair of incisions in the outer edge of the flap which each engage an associated incision in each of the adjacent flaps. The incisions are of a configuration permitting smooth engagement. The material of which the box is made is of a stiff nature, having resistance to bending.",
    },
    {
        "publication_number": "US7669753B2",
        "title": "US7669753B2: Box flap locking system",
        "abstract": "The invention provides a foldable box design having a box flap locking system, comprising: a first flap having an edge with a generally trapezoidal shaped tab cut therein, wherein said generally trapezoidal shaped tab is defined by two inwardly projecting grooves; and a second flap that locks with the first flap, wherein the second flap includes an edge with a second generally trapezoidal shaped tab cut therein, and wherein said second generally trapezoidal shaped tab is defined by two outwardly projecting grooves.",
    },
]

model = SentenceTransformer("all-mpnet-base-v2")
kw_model = KeyBERT(model=model)


for patent in prior_art_data:
    patent["embedding"] = model.encode(patent["abstract"]).tolist()
    keywords_with_scores = kw_model.extract_keywords(
        patent["abstract"],
        keyphrase_ngram_range=(1, 5),
        stop_words="english",
        top_n=10,
    )

    patent["keywords"] = [
        {"keyword": kw[0], "score": kw[1]} for kw in keywords_with_scores
    ]

    if patent["keywords"]:
        keyphrases = [keyword[0] for keyword in keywords_with_scores]
        # vector size 10.
        keyword_weights = torch.tensor([keyword[1] for keyword in keywords_with_scores])

        # 10 X 768 (10 keyphrases, 768 dimensions)
        keyword_embeddings = model.encode(keyphrases, convert_to_tensor=True)

        # Reshape vector to 10X1 matrix of keyword weights.
        keyword_weights = keyword_weights.unsqueeze(1)

        # (10 X 768) * (10 X 1) -> (10 x 768); each embedding is scaled by its score.
        weighted_embeddings = keyword_weights * keyword_weights
        weighted_average_embedding = torch.sum(weighted_embeddings, dim=0) / torch.sum(
            keyword_weights, dim=0
        )
        patent["keyword_embeddings"] = keyword_embeddings
        patent["aggregated_keyword_embedding"] = weighted_average_embedding.tolist()
    else:
        patent["keyword_embeddings"] = None
        patent["aggregated_keyword_embedding"] = None


print("Saving prior art data with embeddings...")

with open("patent_data/prior_art_data.pkl", "wb") as f:
    pickle.dump(prior_art_data, f)
