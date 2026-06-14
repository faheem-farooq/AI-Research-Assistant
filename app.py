import streamlit as st

from tools.paper_search import (
    search_papers
)

from tools.paper_loader import (
    download_paper
)

from tools.retriever import (
    retrieve_context
)

from agent.research_agent import ask_research_agent

from langchain_community.document_loaders import (
    PyPDFLoader
)

from rag.chunker import (
    chunk_documents
)

from rag.vector_db import (
    create_vector_store
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

# -------------------------
# Paper Search Section
# -------------------------

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

# -------------------------
# Research Assistant
# -------------------------

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

                for source in result[
                    "sources"
                ]:

                    st.write(source)

            except Exception as e:

                st.error(
                    f"Error: {e}"
                )