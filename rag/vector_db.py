from langchain_community.vectorstores import (
    FAISS
)

from rag.embeddings import (
    get_embeddings
)


VECTOR_DB_PATH = "data/vectorstore"


def create_vector_store(chunks):

    embeddings = get_embeddings()

    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )

    vectorstore.save_local(
        VECTOR_DB_PATH
    )

    return vectorstore


def load_vector_store():

    embeddings = get_embeddings()

    vectorstore = FAISS.load_local(
        VECTOR_DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vectorstore


def retrieve_documents(
    query,
    k=5
):

    vectorstore = load_vector_store()

    docs = vectorstore.similarity_search(
        query,
        k=k
    )

    return docs