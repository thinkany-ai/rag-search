import os
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import ServiceContext


def get_service_context():
    api_key = os.getenv("OPENAI_API_KEY")
    api_base = os.getenv("OPENAI_BASE_URL")
    llm_model = os.getenv("OPENAI_MODEL")
    embed_model = os.getenv("OPENAI_EMBED_MODEL")

    llm_engine = OpenAI(
        model=llm_model,
        api_key=api_key,
        api_base=api_base,
    )

    embed_engine = OpenAIEmbedding(
        model=embed_model,
        api_key=api_key,
        api_base=api_base,
    )

    service_context = ServiceContext.from_defaults(
        llm=llm_engine,
        embed_model=embed_engine,
    )
    # set_global_service_context(service_context)
    print("init service_context with apibase", api_base)

    return service_context
