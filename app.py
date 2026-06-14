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
                <meta name="viewport" content="width=device-width, initial-scale=1" />
                <style>
                    :root {
                        color-scheme: dark;
                        --bg: #07111f;
                        --panel: rgba(11, 20, 35, 0.78);
                        --panel-border: rgba(148, 163, 184, 0.18);
                        --text: #e5eefc;
                        --muted: #97a6ba;
                        --accent: #7dd3fc;
                        --accent-strong: #38bdf8;
                        --accent-soft: rgba(56, 189, 248, 0.14);
                        --success: #4ade80;
                        --danger: #fb7185;
                        --shadow: 0 24px 80px rgba(2, 8, 23, 0.4);
                    }

                    * { box-sizing: border-box; }

                    body {
                        margin: 0;
                        min-height: 100vh;
                        font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
                        color: var(--text);
                        background:
                            radial-gradient(circle at top left, rgba(56, 189, 248, 0.16), transparent 28%),
                            radial-gradient(circle at top right, rgba(168, 85, 247, 0.14), transparent 24%),
                            linear-gradient(180deg, #030712 0%, var(--bg) 100%);
                    }

                    .wrap {
                        max-width: 1180px;
                        margin: 0 auto;
                        padding: 40px 20px 56px;
                    }

                    .card {
                        background: var(--panel);
                        border: 1px solid var(--panel-border);
                        border-radius: 24px;
                        box-shadow: var(--shadow);
                        backdrop-filter: blur(18px);
                    }

                    .grid {
                        display: grid;
                        grid-template-columns: 1fr 1fr;
                        gap: 24px;
                    }

                    .section {
                        padding: 24px;
                    }

                    .section h2 {
                        margin: 0 0 8px;
                        font-size: 22px;
                        letter-spacing: -0.03em;
                    }

                    .section p.sub {
                        margin: 0 0 18px;
                        color: var(--muted);
                        line-height: 1.7;
                    }

                    label {
                        display: block;
                        font-size: 13px;
                        color: var(--muted);
                        margin: 0 0 8px;
                    }

                    input, textarea {
                        width: 100%;
                        border: 1px solid rgba(148, 163, 184, 0.18);
                        background: rgba(2, 6, 23, 0.72);
                        color: var(--text);
                        border-radius: 16px;
                        padding: 14px 16px;
                        outline: none;
                        transition: border-color 0.15s ease, transform 0.15s ease, box-shadow 0.15s ease;
                    }

                    textarea { min-height: 140px; resize: vertical; }

                    input:focus, textarea:focus {
                        border-color: rgba(125, 211, 252, 0.55);
                        box-shadow: 0 0 0 4px rgba(56, 189, 248, 0.12);
                    }

                    .controls {
                        display: flex;
                        gap: 12px;
                        flex-wrap: wrap;
                        margin-top: 12px;
                    }

                    button {
                        appearance: none;
                        border: 0;
                        border-radius: 14px;
                        padding: 12px 18px;
                        font-size: 14px;
                        font-weight: 700;
                        cursor: pointer;
                        color: #00111f;
                        background: linear-gradient(135deg, #7dd3fc 0%, #38bdf8 100%);
                        box-shadow: 0 12px 30px rgba(56, 189, 248, 0.25);
                    }

                    button.secondary {
                        background: rgba(15, 23, 42, 0.8);
                        color: var(--text);
                        border: 1px solid rgba(148, 163, 184, 0.18);
                        box-shadow: none;
                    }

                    button:disabled {
                        opacity: 0.6;
                        cursor: progress;
                    }

                    .results {
                        display: grid;
                        gap: 14px;
                        margin-top: 18px;
                    }

                    .result-card {
                        padding: 18px;
                        border-radius: 18px;
                        background: rgba(15, 23, 42, 0.58);
                        border: 1px solid rgba(148, 163, 184, 0.14);
                    }

                    .result-card h3 {
                        margin: 0 0 8px;
                        font-size: 16px;
                    }

                    .result-card p {
                        margin: 0;
                        color: var(--muted);
                        line-height: 1.7;
                    }

                    .sources {
                        margin: 12px 0 0;
                        padding-left: 18px;
                        color: var(--text);
                    }

                    .sources li { margin: 8px 0; color: var(--muted); }

                    pre {
                        margin: 0;
                        padding: 16px;
                        border-radius: 16px;
                        overflow: auto;
                        background: rgba(2, 6, 23, 0.85);
                        border: 1px solid rgba(148, 163, 184, 0.14);
                        color: #dbeafe;
                        font-size: 13px;
                        line-height: 1.7;
                    }

                    a { color: var(--accent); }

                    @media (max-width: 960px) {
                        .hero, .grid { grid-template-columns: 1fr; }
                    }
                </style>
      </head>
      <body>
                <div class="wrap">
                    <div class="grid">
                        <section class="card section">
                            <h2>Search papers</h2>
                            <p class="sub">Query arXiv and render the top matches without leaving the page.</p>
                            <label for="searchQuery">Research topic</label>
                            <input id="searchQuery" type="text" placeholder="Arabic speech synthesis" />
                            <div class="controls">
                                <button id="searchBtn">Search papers</button>
                                <button id="exampleSearchBtn" class="secondary">Load example</button>
                            </div>
                            <div id="searchStatus" class="status"></div>
                            <div id="searchResults" class="results"></div>
                        </section>

                        <section class="card section">
                            <h2>Generate report</h2>
                            <p class="sub">Ask a research question and get a synthesized answer plus sources.</p>
                            <label for="reportQuery">Question</label>
                            <textarea id="reportQuery" placeholder="Compare diffusion-based speech synthesis with VITS architectures."></textarea>
                            <div class="controls">
                                <button id="reportBtn">Generate report</button>
                                <button id="exampleReportBtn" class="secondary">Load example</button>
                            </div>
                            <div id="reportStatus" class="status"></div>
                            <div id="reportResults" class="results"></div>
                        </section>
                    </div>
                </div>

                <script>
                    const searchBtn = document.getElementById('searchBtn');
                    const reportBtn = document.getElementById('reportBtn');
                    const searchQuery = document.getElementById('searchQuery');
                    const reportQuery = document.getElementById('reportQuery');
                    const searchStatus = document.getElementById('searchStatus');
                    const reportStatus = document.getElementById('reportStatus');
                    const searchResults = document.getElementById('searchResults');
                    const reportResults = document.getElementById('reportResults');

                    document.getElementById('exampleSearchBtn').addEventListener('click', () => {
                        searchQuery.value = 'diffusion speech synthesis';
                    });

                    document.getElementById('exampleReportBtn').addEventListener('click', () => {
                        reportQuery.value = 'Compare diffusion-based speech synthesis with VITS architectures.';
                    });

                    function setStatus(el, message, kind = '') {
                        el.textContent = message;
                        el.className = 'status' + (kind ? ' ' + kind : '');
                    }

                    function escapeHtml(value) {
                        return String(value)
                            .replaceAll('&', '&amp;')
                            .replaceAll('<', '&lt;')
                            .replaceAll('>', '&gt;')
                            .replaceAll('"', '&quot;')
                            .replaceAll("'", '&#39;');
                    }

                    function renderPaperCard(paper) {
                        const authors = (paper.authors || []).slice(0, 4).join(', ');
                        return `
                            <article class="result-card">
                                <h3>${escapeHtml(paper.title)}</h3>
                                <p><strong>Published:</strong> ${escapeHtml(paper.published || 'Unknown')}</p>
                                <p><strong>Authors:</strong> ${escapeHtml(authors || 'Unknown')}</p>
                                <p>${escapeHtml(paper.summary || '').slice(0, 420)}${(paper.summary || '').length > 420 ? '…' : ''}</p>
                            </article>
                        `;
                    }

                    async function fetchJson(url, options = {}) {
                        const response = await fetch(url, {
                            headers: { 'Accept': 'application/json' },
                            ...options,
                        });
                        const data = await response.json().catch(() => ({}));
                        if (!response.ok) {
                            const message = data.detail || data.error || response.statusText;
                            throw new Error(message);
                        }
                        return data;
                    }

                    searchBtn.addEventListener('click', async () => {
                        const query = searchQuery.value.trim();
                        if (!query) {
                            setStatus(searchStatus, 'Enter a research topic first.', 'error');
                            return;
                        }

                        searchBtn.disabled = true;
                        setStatus(searchStatus, 'Searching arXiv...', '');
                        searchResults.innerHTML = '';

                        try {
                            const data = await fetchJson(`/api/search?q=${encodeURIComponent(query)}&max_results=5`);
                            const papers = data.papers || [];
                            setStatus(searchStatus, `${papers.length} paper(s) found for “${query}”.`, 'success');
                            searchResults.innerHTML = papers.length
                                ? papers.map(renderPaperCard).join('')
                                : '<div class="result-card"><p>No papers found.</p></div>';
                        } catch (error) {
                            setStatus(searchStatus, error.message, 'error');
                        } finally {
                            searchBtn.disabled = false;
                        }
                    });

                    reportBtn.addEventListener('click', async () => {
                        const query = reportQuery.value.trim();
                        if (!query) {
                            setStatus(reportStatus, 'Enter a research question first.', 'error');
                            return;
                        }

                        reportBtn.disabled = true;
                        setStatus(reportStatus, 'Generating report...', '');
                        reportResults.innerHTML = '';

                        try {
                            const data = await fetchJson(`/api/report?q=${encodeURIComponent(query)}`);
                            const sources = (data.sources || []).map((source) => `<li>${escapeHtml(source)}</li>`).join('');
                            reportResults.innerHTML = `
                                <article class="result-card">
                                    <h3>Research report</h3>
                                    <pre>${escapeHtml(data.answer || '')}</pre>
                                    <h3 style="margin-top:18px;">Sources</h3>
                                    <ul class="sources">${sources || '<li>No sources returned.</li>'}</ul>
                                </article>
                            `;
                            setStatus(reportStatus, 'Report generated successfully.', 'success');
                        } catch (error) {
                            setStatus(reportStatus, error.message, 'error');
                        } finally {
                            reportBtn.disabled = false;
                        }
                    });

          
                </script>
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