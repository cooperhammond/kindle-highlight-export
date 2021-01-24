import os
import shutil

from .gmail_dl import retrieve_kindle_highlight_files
from .kindle_export_scraper import format_highlight_export, get_parsed_highlight_export

dl_directory = "notebook-downloads/"


def get_formatted_exports(gmail_username, gmail_password, clearTemp=True):
    exports = {} # book title -> formatted export

    file_locs = retrieve_kindle_highlight_files(gmail_username, gmail_password, dl_directory)

    for file_loc in file_locs:
        title = os.path.splitext(os.path.basename(file_loc))[0].split(" - Notebook")[0]
        raw_exports = get_parsed_highlight_export(file_loc)
        exports[title] = format_highlight_export(*raw_exports)

    if clearTemp:
        shutil.rmtree(dl_directory)

    return exports
