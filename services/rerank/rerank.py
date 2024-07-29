import os 
from services.rerank.llamaindex import get_rerank_results as get_rerank_llamaindex
from services.rerank.flashrank import get_rerank_results as get_rerank_flashrank


def rerank(search_results, query):
    rerank_method = os.getenv("RERANK_METHOD")
    if not rerank_method or rerank_method == "flash_rank":
        rerank_results = get_rerank_flashrank(query, search_results)
    elif rerank_method == "llama_index":
        rerank_results = get_rerank_llamaindex(query, search_results)
    else:
        print(f"rerank failed: unknown rerank_method: {rerank_method}")
        return search_results

    score_maps = {}
    for result in rerank_results:
        score_maps[result["uuid"]] = result["score"]

    for result in search_results:
        if result["uuid"] in score_maps:
            result["score"] = score_maps[result["uuid"]]

    sorted_search_results = sorted(search_results,
                                   key=lambda x: (x['score']),
                                   reverse=True)

    return sorted_search_results