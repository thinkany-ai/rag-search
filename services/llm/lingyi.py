import os

from llama_index.core import ServiceContext

from llama_index.core.embeddings import resolve_embed_model

from llama_index.llms.openai.utils import ALL_AVAILABLE_MODELS
from llama_index.llms.openai.utils import CHAT_MODELS
from tiktoken.model import MODEL_TO_ENCODING
from llama_index.llms.openai import OpenAI

CHAT_MODELS["yi-34b-chat-0205"] = 4096
CHAT_MODELS["yi-34b-chat-200k"] = 200 * 1024
ALL_AVAILABLE_MODELS["yi-34b-chat-0205"] = 4096
ALL_AVAILABLE_MODELS["yi-34b-chat-200k"] = 200 * 1024
MODEL_TO_ENCODING['yi-34b-chat-0205'] = 'cl100k_base'
MODEL_TO_ENCODING['yi-34b-chat-200k'] = 'cl100k_base'


def get_service_context():
    api_key = os.getenv("LINGYI_API_KEY")
    api_base = os.getenv("LINGYI_BASE_URL")
    llm_model = os.getenv("LINGYI_MODEL")
    embed_model = os.getenv("LINGYI_EMBED_MODEL")

    llm_engine = OpenAI(model=llm_model, api_key=api_key,
                        api_base=api_base)

    if not embed_model:
        embed_model = "local:BAAI/bge-small-en-v1.5"

    embed_engine = resolve_embed_model(embed_model)

    service_context = ServiceContext.from_defaults(
        llm=llm_engine,
        embed_model=embed_engine,
    )
    # set_global_service_context(service_context)
    print("init service_context with apibase", api_base)

    return service_context
