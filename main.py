import os

from dotenv import load_dotenv

from src.highlights.gmail_dl import retrieve_kindle_highlights_files
from src.highlights.kindle_export_scraper import get_formatted_highlights



def main():
    load_dotenv()

    dl_directory = "notebook-downloads/"
    gmail_username = os.getenv("GMAIL_USERNAME")
    gmail_password = os.getenv("GMAIL_PASSWORD")

    # download emailed files
    file_locs = retrieve_kindle_highlights_files(gmail_username, gmail_password, dl_directory)

    formatted_highlights = []

    for file_loc in file_locs:
        formatted_highlights.append(get_formatted_highlights(file_loc))


if __name__ == "__main__":
    main()