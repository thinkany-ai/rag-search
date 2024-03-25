import os
from llama_index.legacy.vector_stores import MilvusVectorStore
from llama_index.legacy.storage import StorageContext


def get_vector_store():
    uri = os.getenv("ZILLIZ_URI")
    token = os.getenv("ZILLIZ_TOKEN")
    dim = os.getenv("ZILLIZ_DIM")
    collection = os.getenv("ZILLIZ_COLLECTION")

    vector_store = MilvusVectorStore(
        uri=uri, token=token, collection_name=collection, dim=dim, overwrite=False
    )

    return vector_store


def get_storage_context():
    vector_store = get_vector_store()
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    return storage_context
