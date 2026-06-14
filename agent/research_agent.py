from tools.paper_search import search_papers
from tools.retriever import retrieve_context
from tools.summarizer import summarize_documents
from services.llm import get_llm

from functools import lru_cache


@lru_cache(maxsize=1)
def _get_llm():
    return get_llm()


def ask_research_agent(query: str):

    # Search papers
    papers = search_papers(
        query=query,
        max_results=5
    )

    # Retrieve context
    docs = retrieve_context(
        query=query,
        k=5
    )

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = f"""
You are an AI Research Assistant.

Question:
{query}

Context:
{context}

Provide:
1. Direct answer
2. Key findings
3. Future research directions
4. Sources used
"""

    response = _get_llm().invoke(prompt)

    return {
        "answer": response.content,
        "papers": papers,
        "sources": [
            paper["title"] for paper in papers
        ]
    }