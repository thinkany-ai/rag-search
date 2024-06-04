import os
from typing import Optional
from pydantic import BaseModel
from fastapi import APIRouter, Header
from services.search.serper import get_search_results
from services.rerank.llamaindex import get_rerank_results as get_rerank_llamaindex
from services.rerank.flashrank import get_rerank_results as get_rerank_flashrank
from services.document.store import store_results
from services.document.query import query_results
from services.web import batch_fetch_urls
from utils.resp import resp_err, resp_data


rag_router = APIRouter()


class RagSearchReq(BaseModel):
    query: str
    locale: Optional[str] = ''
    search_n: Optional[int] = 10
    search_provider: Optional[str] = 'google'
    is_reranking: Optional[bool] = False
    is_detail: Optional[bool] = False
    detail_top_k: Optional[int] = 6
    detail_min_score: Optional[float] = 0.70
    is_filter: Optional[bool] = False
    filter_min_score: Optional[float] = 0.80
    filter_top_k: Optional[int] = 6


@rag_router.post("/rag-search")
async def rag_search(req: RagSearchReq, authorization: str = Header(None)):
    authApiKey = os.getenv("AUTH_API_KEY")
    apiKey = ""
    if authorization:
        apiKey = authorization.replace("Bearer ", "")
    if apiKey != authApiKey:
        return resp_err("Access Denied")

    if req.query == "":
        return resp_err("invalid params")

    try:
        search_results = []
        # 1. get search results
        try:
            search_results = search(req.query, req.search_n, req.locale)
        except Exception as e:
            return resp_err(f"get search results failed: {e}")

        # 2. reranking
        if req.is_reranking:
            try:
                search_results = reranking(search_results, req.query)
            except Exception as e:
                print(f"reranking search results failed: {e}")

        # 3. fetch details
        if req.is_detail:
            try:
                search_results = await fetch_details(search_results, req.detail_min_score, req.detail_top_k)
            except Exception as e:
                print(f"fetch search details failed: {e}")

        # 4. filter content
        if req.is_filter:
            try:
                search_results = filter_content(search_results, req.query, req.filter_min_score, req.filter_top_k)
            except Exception as e:
                print(f"filter content failed: {e}")

        return resp_data({
            "search_results": search_results,
        })
    except Exception as e:
        return resp_err(f"rag search failed: {e}")


def search(query, num, locale=''):
    params = {
        "q": query,
        "num": num
    }

    if locale:
        params["hl"] = locale

    try:
        search_results = get_search_results(params=params)

        return search_results
    except Exception as e:
        print(f"search failed: {e}")
        raise e


def reranking(search_results, query):
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


async def fetch_details(search_results, min_score=0.00, top_k=6):
    urls = []
    for res in search_results:
        if len(urls) > top_k:
            break
        if res["score"] >= min_score:
            urls.append(res["link"])

    try:
        details = await batch_fetch_urls(urls)
    except Exception as e:
        print(f"fetch details failed: {e}")
        raise e

    content_maps = {}
    for url, content in details:
        content_maps[url] = content

    for result in search_results:
        if result["link"] in content_maps:
            result["content"] = content_maps[result["link"]]

    return search_results


def filter_content(search_results, query, filter_min_score=0.8, filter_top_k=10):
    try:
        results_with_content = []
        for result in search_results:
            if "content" in result and len(result["content"]) > len(result["snippet"]):
                results_with_content.append(result)

        index = store_results(results=results_with_content)
        match_results = query_results(index, query, filter_min_score, filter_top_k)

    except Exception as e:
        print(f"filter content failed: {e}")
        raise e

    content_maps = {}
    for result in match_results:
        if result["uuid"] not in content_maps:
            content_maps[result["uuid"]] = ""
        else:
            content_maps[result["uuid"]] += result["content"]

    for result in search_results:
        if result["uuid"] in content_maps:
            result["content"] = content_maps[result["uuid"]]

    return search_results
