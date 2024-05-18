import os
from flashrank import Ranker, RerankRequest
from services.document.store import store_results
from services.document.query import query_results


flashrank_model_name = os.getenv("FLASHRANK_MODEL_NAME", "ms-marco-MultiBERT-L-12")
ranker = Ranker(model_name=flashrank_model_name)


def get_rerank_results(query, search_results):
    try:
        passages = []
        for i, result in enumerate(search_results):
            text = result["snippet"]
            if "content" in result and len(result["content"]) > len(result["snippet"]):
                text = result["content"]

            passages.append(
                {
                    "id": i,
                    "text": text,
                    "meta": {}
                }
            )

        flash_req = RerankRequest(query=query, passages=passages)
        flash_results = ranker.rerank(flash_req)

        rerank_results = []
        for i, flash_result in enumerate(flash_results):
            rerank_result = search_results[flash_result["id"]]
            rerank_result["score"] = flash_result["score"]
            rerank_results.append(rerank_result)
    except Exception as e:
        print(f"reranking search results failed: {e}")
        raise e

    return rerank_results