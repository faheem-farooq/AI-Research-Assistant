import os

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

    if not os.path.isdir(VECTOR_DB_PATH):
        return None

    required_files = (
        "index.faiss",
        "index.pkl"
    )

    if not all(
        os.path.exists(
            os.path.join(
                VECTOR_DB_PATH,
                filename
            )
        ) for filename in required_files
    ):
        return None

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