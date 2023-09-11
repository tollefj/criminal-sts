from embedding_match import EmbeddingMatch
import numpy as np

def get_matches(sbert, index, df, query, k=10):
    if isinstance(query, str):
        query = [query]
    emb = sbert.encode(query)
    dists, indices = index.search(emb, k)
    dists = 1 - (1 - dists / dists.max())

    matchers = {}

    for m_idx, (score, indice) in enumerate(zip(dists[0], indices[0])):
        match = df.iloc[indice]
        matcher = matchers.get(match.id, EmbeddingMatch(match.id))
        matcher.add_paragraphs_and_sentences(match.para_id, match.sent_id, score, match.sent_text)
        
        # use the index to find related matches to the already found match:
        nearest_k = 5
        nbrs_score, nbrs_indices = index.search(np.array([match.sbert_768]), k=nearest_k)
        nbrs_score = 1 - (1 - nbrs_score / nbrs_score.max())
        for nbr_score, nbr_indice in zip(nbrs_score[0], nbrs_indices[0]):
            if nbr_indice == indice:
                continue
            r = df.iloc[nbr_indice]
            matcher.add_paragraphs_and_sentences(r.para_id, r.sent_id, nbr_score, r.sent_text, related=True)
        
        matchers[match.id] = matcher

    return matchers