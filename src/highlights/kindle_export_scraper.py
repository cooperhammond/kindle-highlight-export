from bs4 import BeautifulSoup

def get_formatted_highlights(file_loc):

    file = open(file_loc, 'r')
    html = file.read()

    soup = BeautifulSoup(html, 'html.parser')

    string = ""

    notes = {}
    highlight_headings = []
    hightlight_texts = []

    highlightIndex = 0
    for div in soup.find_all('div'):
        text = div.get_text().strip("\n")
        if div['class'][0] == 'noteHeading':

            # if a reader's note is found
            if text.split(" ")[0] == "Note":
                notes[highlightIndex-1] = "_" # attaches to the previously indexed highlight
            else:
                highlight_headings.append(text.split(" -  ")[-1])
        elif div['class'][0] == 'noteText':
            if highlightIndex-1 in notes:
                notes[highlightIndex-1] = text
            else:
                hightlight_texts.append(text)
            highlightIndex += 1
        
    string = ''

    for i in range(0, len(hightlight_texts)):
        string += hightlight_texts[i]
        string += " ("
        string += highlight_headings[i]
        string += ")\n"
        if i in notes:
            string += "\t"
            string += notes[i]
            string += "\n"

    return string

import pyperclip
pyperclip.copy(get_formatted_highlights("notebook-downloads/Unsong - Notebook.html"))