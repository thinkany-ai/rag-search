def query_results(index, query, min_score=0.80, top_k=10):
    retriever = index.as_retriever(similarity_top_k=top_k)

    nodes = retriever.retrieve(query)
    results = [
        {
            "uuid": node.metadata["uuid"],
            "title": node.metadata["title"],
            "snippet": node.metadata["snippet"],
            "link": node.metadata["link"],
            "content": node.text,
            "score": node.score,
        }
        for node in nodes if node.score > min_score
    ]

    return results
