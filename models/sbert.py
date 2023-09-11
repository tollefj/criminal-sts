import numpy as np
from typing import List
from models.LexRank import degree_centrality_scores
from sentence_transformers import SentenceTransformer, util
# from bertopic import BERTopic
# from keybert import KeyBERT
from autofaiss import build_index
# from umap import UMAP
# from hdbscan import HDBSCAN

"""
BERTOPIC:

Fit the model	.fit(docs)
Fit the model and predict documents	.fit_transform(docs)
Predict new documents	.transform([new_doc])
Access single topic	.get_topic(topic=12)
Access all topics	.get_topics()
Get topic freq	.get_topic_freq()
Get all topic information	.get_topic_info()
Get all document information	.get_document_info(docs)
Get representative docs per topic	.get_representative_docs()
Update topic representation	.update_topics(docs, n_gram_range=(1, 3))
Generate topic labels	.generate_topic_labels()
Set topic labels	.set_topic_labels(my_custom_labels)
Merge topics	.merge_topics(docs, topics_to_merge)
Reduce nr of topics	.reduce_topics(docs, nr_topics=30)
Reduce outliers	.reduce_outliers(docs, topics)
Find topics	.find_topics("vehicle")
Save model	.save("my_model")
Load model	BERTopic.load("my_model")
Get parameters	.get_params()
"""

SBERT_MODEL = 'NbAiLab/nb-sbert-base'


def load():
    return SentenceTransformer(SBERT_MODEL)


# def load_keybert(sbert_model):
#     return KeyBERT(model=sbert_model)


# def load_bertopic(docs):
#     umap_model = UMAP(n_neighbors=15, n_components=10,
#                       min_dist=0.0, metric='cosine')
#     hdbscan_model = HDBSCAN(min_cluster_size=10, metric='euclidean',
#                             cluster_selection_method='eom', prediction_data=True)

#     return BERTopic(embedding_model=SBERT_MODEL,
#                     n_gram_range=(1, 2),
#                     umap_model=umap_model,
#                     hdbscan_model=hdbscan_model,
#                     ).fit(docs)


def get_cos(sbert_model, sents):
    embeddings = sbert_model.encode(sents, convert_to_tensor=True)
    cos_scores = util.cos_sim(embeddings, embeddings).numpy()
    return cos_scores


def get_centrality(sbert_model, cos_scores, sents, n_sents=3):
    cos_scores = get_cos(sbert_model, sents)
    centrality = degree_centrality_scores(cos_scores, threshold=None)
    most_central = np.argsort(-centrality)

    best_sents = []
    for idx in most_central[:n_sents]:
        best_sents.append(sents[idx].strip())
    return best_sents


# def get_keywords(keybert_model: KeyBERT, doc, ngram_range=(1, 1), stopwords=None, top_n=5, seed_words=None):
#     return keybert_model.extract_keywords(
#         doc,
#         keyphrase_ngram_range=ngram_range,
#         stop_words=stopwords,
#         top_n=top_n,
#         nr_candidates=100,
#         seed_keywords=seed_words,
#     )


# def get_keywords(keybert_model: KeyBERT, doc: str, **kwargs):
#     """
#         docs: The document(s) for which to extract keywords/keyphrases
#         candidates: Candidate keywords/keyphrases to use instead of extracting them from the document(s)
#                     NOTE: This is not used if you passed a `vectorizer`.
#         keyphrase_ngram_range: Length, in words, of the extracted keywords/keyphrases.
#                     NOTE: This is not used if you passed a `vectorizer`.
#         stop_words: Stopwords to remove from the document.
#                     NOTE: This is not used if you passed a `vectorizer`.
#         top_n: Return the top n keywords/keyphrases
#         min_df: Minimum document frequency of a word across all documents
#                 if keywords for multiple documents need to be extracted.
#                 NOTE: This is not used if you passed a `vectorizer`.
#         use_maxsum: Whether to use Max Sum Distance for the selection
#                     of keywords/keyphrases.
#         use_mmr: Whether to use Maximal Marginal Relevance (MMR) for the
#                     selection of keywords/keyphrases.
#         diversity: The diversity of the results between 0 and 1 if `use_mmr`
#                     is set to True.
#         nr_candidates: The number of candidates to consider if `use_maxsum` is
#                         set to True.
#         vectorizer: Pass in your own `CountVectorizer` from
#                     `sklearn.feature_extraction.text.CountVectorizer`
#         highlight: Whether to print the document and highlight its keywords/keyphrases.
#                     NOTE: This does not work if multiple documents are passed.
#         seed_keywords: Seed keywords that may guide the extraction of keywords by
#                         steering the similarities towards the seeded keywords.
#         doc_embeddings: The embeddings of each document.
#         word_embeddings: The embeddings of each potential keyword/keyphrase across
#                             across the vocabulary of the set of input documents.
#                             NOTE: The `word_embeddings` should be generated through
#                             `.extract_embeddings` as the order of these embeddings depend
#                             on the vectorizer that was used to generate its vocabulary.
#     """
#     return keybert_model.extract_keywords(doc, **kwargs)


def similarity_search(sbert_model, sentences, search_sent):
    embeddings = sbert_model.encode(sentences)
    index, index_infos = build_index(embeddings, save_on_disk=False)

    # Search for the closest matches
    query = sbert_model.encode([search_sent])
    _, index_matches = index.search(query, 1)

    return index_matches


# def get_topics(bertopic_model: BERTopic):
#     return bertopic_model.get_topic(bertopic_model.get_topic_freq().iloc[1].Topic)


# def visualize_topics(bertopic_model: BERTopic):
#     return bertopic_model.visualize_topics()


# def get_topics_by_time(bertopic_model: BERTopic, docs: List[str], timestamps: List[int]):
#     return bertopic_model.topics_over_time(
#         docs=docs,
#         timestamps=timestamps,
#         global_tuning=True,
#         evolution_tuning=True,
#         nr_bins=20
#     )


# def visualize_timetopics(bertopic_model: BERTopic, time_topics):
#     return bertopic_model.visualize_topics_over_time(time_topics, top_n_topics=20)
