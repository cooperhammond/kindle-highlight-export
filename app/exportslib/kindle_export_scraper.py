from bs4 import BeautifulSoup

def get_parsed_highlight_export(file_loc):
    file = open(file_loc, 'r')
    html = file.read()

    soup = BeautifulSoup(html, 'html.parser')

    notes = {}
    highlight_headings = []
    highlight_texts = []

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
                highlight_texts.append(text)
            highlightIndex += 1
    
    return notes, highlight_headings, highlight_texts

def format_highlight_export(notes, highlight_headings, highlight_texts):

    string = ""

    for i in range(0, len(highlight_texts)):
        string += highlight_texts[i]
        string += " ("
        string += highlight_headings[i]
        string += ")\n"
        if i in notes:
            string += "\t"
            string += notes[i]
            string += "\n"

    return string