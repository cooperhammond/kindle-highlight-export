import os

from dotenv import load_dotenv
from livereload import Server #==2.5.1

from app.exportslib.gmail_dl import retrieve_kindle_highlight_files
from app.exportslib.kindle_export_scraper import get_parsed_highlight_export, format_highlight_export

from app import create_app


def main():
    # load_dotenv()

    # dl_directory = "notebook-downloads/"
    # gmail_username = os.getenv("GMAIL_USERNAME")
    # gmail_password = os.getenv("GMAIL_PASSWORD")

    # # download emailed files
    # file_locs = retrieve_kindle_highlights_files(gmail_username, gmail_password, dl_directory)

    # formatted_highlights = []

    # for file_loc in file_locs:
    #     formatted_highlights.append(get_formatted_highlights(file_loc))

    app = create_app()
    app.debug = True
    server = Server(app.wsgi_app)
    server.watch('app/templates/*.html')
    server.watch('app/static/css/*.css')
    server.serve()


if __name__ == "__main__":
    main()