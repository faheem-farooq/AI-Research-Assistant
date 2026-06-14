from services.llm import (
    get_llm
)


def summarize_documents(
    documents
):

    llm = get_llm()

    context = "\n\n".join(
        [
            doc.page_content
            for doc in documents
        ]
    )

    prompt = f"""
You are an expert research assistant.

Summarize the following
research papers.

Context:

{context}

Provide:

1. Main Findings
2. Key Methods
3. Important Results
4. Limitations
5. Future Directions
"""

    response = llm.invoke(
        prompt
    )

    return response.content