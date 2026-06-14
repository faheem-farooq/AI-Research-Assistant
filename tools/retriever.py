from rag.vector_db import (
    load_vector_store
)


def retrieve_context(
    query: str,
    k: int = 5
):

    vectorstore = (
        load_vector_store()
    )

    docs = (
        vectorstore.similarity_search(
            query,
            k=k
        )
    )

    return docs