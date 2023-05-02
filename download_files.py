import os
import requests

from bs4 import BeautifulSoup


def download_pdf_files(url: str, save_directory: str) -> None:
    if not os.path.exists(save_directory):
        os.mkdir(save_directory)

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    for link in soup.find_all("a"):
        href = link.get("href")
        if href is not None:
            if href.endswith(".pdf"):
                pdf_url = href
                pdf_filename = pdf_url.rsplit('/', 1)[1]
                output_path = os.path.join(save_directory, pdf_filename)
                # print(pdf_url)
                # print(output_path)
                with open(output_path, "wb") as f:
                    f.write(requests.get(pdf_url).content)
                    f.close()
                print(f"Downloaded {pdf_filename}")

    print("All PDF files downloaded")


if __name__ == "__main__":
    download_pdf_files(url="https://amostech.com/2022-technical-papers/", save_directory="pdf_files")
