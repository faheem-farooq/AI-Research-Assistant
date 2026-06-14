import arxiv


def search_papers(
    query: str,
    max_results: int = 10
):
    """
    Search ArXiv for papers.
    """

    client = arxiv.Client()

    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )

    papers = []

    for result in client.results(search):

        papers.append(
            {
                "title": result.title,
                "authors": [
                    author.name
                    for author in result.authors
                ],
                "summary": result.summary,
                "pdf_url": result.pdf_url,
                "published": str(
                    result.published.date()
                )
            }
        )

    return papers