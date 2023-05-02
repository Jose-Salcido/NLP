import os
import requests

from bs4 import BeautifulSoup
import sqlite3
import PyPDF2
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter

import download_files

output_dir = "pdf_files"

# Download PDF files from website
# download_files.download_pdf_files(url="https://amostech.com/2022-technical-papers/", save_directory = output_dir)

# Perform Natural Naguage Processing (NLP)
# Download required NLTK data
# nltk.download('punkt')
# nltk.download('stopwords')

# Replace with the path to the directory containing the PDF files you want to analyze
#pdfs_directory = output_dir
pdfs_directory = <path_to_pdf_files>

# Define the name and schema of the database
database_name = "pdf_database.db"
database_schema = """
CREATE TABLE IF NOT EXISTS pdfs (
    id INTEGER PRIMARY KEY,
    title TEXT,
    filename TEXT,
    tokens TEXT
);
"""

# Create a connection to the database
connection = sqlite3.connect(database_name)

# Create the pdfs table if it doesn't exist
connection.execute(database_schema)

# Loop over the PDF files in the directory and capture tokens
for pdf_filename in os.listdir(pdfs_directory):
    if pdf_filename.endswith(".pdf"):
        pdf_file_path = os.path.join(pdfs_directory, pdf_filename)

        # TODO: Read abstract title and rename file

        pdf_file = open(pdf_file_path, 'rb')
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        pdf_text = ""

        for page in range(len(pdf_reader.pages)):
            pdf_object = pdf_reader.pages[page]
            pdf_text += pdf_object.extract_text()

        tokens = word_tokenize(pdf_text.lower())

        # Remove stop words and punctuation from the tokens
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [token for token in tokens if token.isalpha() and token not in stop_words]

        # Count the frequency of each token and extract the top 10 most common tokens
        token_counts = Counter(filtered_tokens)
        top_tokens = token_counts.most_common(10)
        top_tokens_str = ", ".join([f"{token}: {count}" for token, count in top_tokens])

        # Insert the data into the pdfs table
        connection.execute(
            "INSERT INTO pdfs (title, filename, tokens) VALUES (?, ?, ?)", (pdf_filename, pdf_filename, top_tokens_str)
        )
        connection.commit()

# Close the database connection
connection.close()
