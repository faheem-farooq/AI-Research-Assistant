import requests
import os


PAPER_DIR = "data/papers"




def download_paper(
    pdf_url: str,
    filename: str
):

    response = requests.get(pdf_url)

    file_path = os.path.join(
        PAPER_DIR,
        filename
    )

    with open(
        file_path,
        "wb"
    ) as f:

        f.write(response.content)

    return file_path