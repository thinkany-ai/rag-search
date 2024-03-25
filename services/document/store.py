from llama_index.legacy import Document, VectorStoreIndex
from llama_index.legacy.node_parser import SimpleNodeParser
from services.vdb.zilliz import get_storage_context
from services.llm.openai import get_service_context
from utils.hash import md5


def store_results(results):
    documents = []
    for result in results:
        document = build_document(result=result)
        documents.append(document)

        print(
            "build index for result: ",
            result["title"],
            result["link"],
            len(documents),
        )

    nodes = build_nodes(documents=documents)
    print("nodes count", len(nodes), len(documents))

    # index = VectorStoreIndex(nodes)
    # index.storage_context.persist(persist_dir="./storage")

    storage_context = get_storage_context()
    service_context = get_service_context()

    index = VectorStoreIndex(nodes=nodes,
                             storage_context=storage_context,
                             service_context=service_context)

    print("build index ok", storage_context)

    return index


def build_document(result):
    if not result["link"] or not result["snippet"]:
        return

    uuid = ""
    if "uuid" in result:
        uuid = result["uuid"]
    else:
        uuid = md5(result["link"])

    text = result["snippet"]
    if "content" in result and len(result["content"]) > len(result["snippet"]):
        text = result["content"]

    document = Document(
        text=text,
        metadata={
            "uuid": uuid,
            "title": result["title"],
            "snippet": result["snippet"],
            "link": result["link"],
        },
        metadata_template="{key}: {value}",
        text_template="{metadata_str}\n\n{content}",
    )
    document.doc_id = uuid
    document.excluded_llm_metadata_keys = ["link", "score"]
    document.excluded_embed_metadata_keys = ["link", "score"]

    return document


def build_nodes(documents):
    parser = SimpleNodeParser.from_defaults(chunk_size=1024, chunk_overlap=20)

    nodes = parser.get_nodes_from_documents(documents=documents, show_progress=True)

    return nodes
