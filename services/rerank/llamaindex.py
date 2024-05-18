from services.document.store import store_results
from services.document.query import query_results


def get_rerank_results(query, search_results):
    try:
        index = store_results(results=search_results)
        rerank_results = query_results(index, query, 0.00, len(search_results))
    except Exception as e:
        print(f"reranking search results failed: {e}")
        raise e
    
    return rerank_results