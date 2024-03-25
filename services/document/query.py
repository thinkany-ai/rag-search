from llama_index.legacy.retrievers import VectorIndexRetriever


def query_results(index, query, min_score=0.80, top_k=10):
    retriever = VectorIndexRetriever(index=index, similarity_top_k=top_k)

    nodes = retriever.retrieve(query)
    results = []

    for node in nodes:
        if node.score > min_score:
            result = {
                "uuid": node.metadata["uuid"],
                "title": node.metadata["title"],
                "snippet": node.metadata["snippet"],
                "link": node.metadata["link"],
                "content": node.text,
                "score": node.score,
            }
            results.append(result)

    sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)

    return sorted_results
