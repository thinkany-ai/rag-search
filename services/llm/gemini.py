import os
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.core import ServiceContext


def get_service_context():
    api_key = os.getenv("GOOGLE_API_KEY")
    api_base = os.getenv("GOOGLE_BASE_URL")
    llm_model = os.getenv("GOOGLE_MODEL")
    embed_model = os.getenv("GOOGLE_EMBED_MODEL")

    llm_engine = Gemini(
        model_name=llm_model, 
        api_key=api_key, 
        api_base=api_base
    )

    embed_engine = GeminiEmbedding(
        model_name=embed_model, 
        api_key=api_key, 
        api_base=api_base
    )

    service_context = ServiceContext.from_defaults(
        llm=llm_engine,
        embed_model=embed_engine,
    )
    # set_global_service_context(service_context)
    print("init service_context with apibase", api_base)

    return service_context
