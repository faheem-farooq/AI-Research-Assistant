from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse

from agent.research_agent import ask_research_agent
from tools.paper_search import search_papers


app = FastAPI(
    title="Autonomous AI Research Assistant",
    version="1.0.0"
)


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
      <head>
        <title>Autonomous AI Research Assistant</title>
        <style>
          body { font-family: system-ui, sans-serif; max-width: 760px; margin: 48px auto; padding: 0 20px; line-height: 1.6; }
          code { background: #f4f4f4; padding: 2px 6px; border-radius: 4px; }
          a { color: #0b5fff; }
        </style>
      </head>
      <body>
        <h1>Autonomous AI Research Assistant</h1>
        <p>This deployment exposes API endpoints for search and research reports.</p>
        <ul>
          <li><a href="/api/health">/api/health</a></li>
          <li><a href="/api/search?q=diffusion%20speech%20synthesis">/api/search</a></li>
          <li><a href="/api/report?q=Compare%20diffusion-based%20speech%20synthesis%20with%20VITS">/api/report</a></li>
        </ul>
        <p>For the Streamlit UI, run <code>streamlit run app.py</code> locally.</p>
      </body>
    </html>
    """


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/search")
def api_search(
    q: str = Query(..., min_length=1),
    max_results: int = Query(10, ge=1, le=25)
):
    return {
        "query": q,
        "papers": search_papers(q, max_results=max_results)
    }


@app.get("/api/report")
def api_report(
    q: str = Query(..., min_length=1)
):
    try:
        return ask_research_agent(q)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        ) from exc


def _run_streamlit_ui():
    import streamlit as st

    from langchain_community.document_loaders import (
        PyPDFLoader
    )

    from rag.chunker import (
        chunk_documents
    )

    from rag.vector_db import (
        create_vector_store
    )

    from tools.paper_loader import (
        download_paper
    )

    st.set_page_config(
        page_title="Autonomous AI Research Assistant",
        page_icon="📚",
        layout="wide"
    )

    st.title(
        "📚 Autonomous AI Research Assistant"
    )

    st.markdown(
        """
Search research papers, build a knowledge base,
and generate AI-powered research reports.
"""
    )

    st.header(
        "🔍 Search Research Papers"
    )

    search_query = st.text_input(
        "Research Topic",
        placeholder="Arabic speech synthesis"
    )

    if st.button("Search Papers"):

        with st.spinner(
            "Searching ArXiv..."
        ):

            papers = search_papers(
                search_query
            )

            st.session_state["papers"] = (
                papers
            )

    if "papers" in st.session_state:

        papers = st.session_state[
            "papers"
        ]

        for idx, paper in enumerate(
            papers
        ):

            with st.expander(
                paper["title"]
            ):

                st.write(
                    f"Published: {paper['published']}"
                )

                st.write(
                    paper["summary"]
                )

                if st.button(
                    f"Download Paper {idx}"
                ):

                    filename = (
                        f"paper_{idx}.pdf"
                    )

                    file_path = (
                        download_paper(
                            paper["pdf_url"],
                            filename
                        )
                    )

                    loader = (
                        PyPDFLoader(
                            file_path
                        )
                    )

                    docs = (
                        loader.load()
                    )

                    chunks = (
                        chunk_documents(
                            docs
                        )
                    )

                    create_vector_store(
                        chunks
                    )

                    st.success(
                        "Paper indexed successfully."
                    )

    st.header(
        "🤖 Ask Research Questions"
    )

    research_question = st.text_area(
        "Question",
        placeholder="""
Compare diffusion-based speech synthesis
with VITS architectures.
"""
    )

    if st.button(
        "Generate Research Report"
    ):

        if not research_question:

            st.warning(
                "Please enter a question."
            )

        else:

            with st.spinner(
                "Analyzing papers..."
            ):

                try:

                    result = (
                        ask_research_agent(
                            research_question
                        )
                    )

                    st.subheader(
                        "Research Report"
                    )

                    st.markdown(
                        result["answer"]
                    )

                    st.subheader(
                        "Sources"
                    )

                    for source in result.get(
                        "sources",
                        []
                    ):

                        st.write(source)

                except Exception as e:

                    st.error(
                        f"Error: {e}"
                    )


if __name__ == "__main__":
    _run_streamlit_ui()