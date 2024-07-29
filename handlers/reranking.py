import os
from typing import Optional, Any, Dict, List
from pydantic import BaseModel
from fastapi import APIRouter, Header
from utils.resp import resp_err, resp_data
from services.rerank.rerank import rerank

reranking_router = APIRouter()


class RerankReq(BaseModel):
    query: str 
    search_results: List[Dict[str, Any]]


@reranking_router.post("/reranking")
async def reranking(req: RerankReq, authorization: str = Header(None)):
    authApiKey = os.getenv("AUTH_API_KEY")
    apiKey = ""
    if authorization:
        apiKey = authorization.replace("Bearer ", "")
    if apiKey != authApiKey:
        return resp_err("Access Denied")

    if req.query == "" or len(req.search_results) == 0:
        return resp_err("invalid params")

    try:
        search_results = rerank(req.search_results, req.query)

        return resp_data({
            "reranking_results": search_results,
        })
    except Exception as e:
         return resp_err(f"reranking failed: {e}") 