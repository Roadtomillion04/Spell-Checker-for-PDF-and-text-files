"""
Multiline sentence probably won't because the offset(starting pos) of the error returned by the api wll not match the sentence in the new line. Perhaps appending all lines process it and then restoring to their original position may work.
"""

import requests

import json
from tkinter.filedialog import askopenfilename
from pdf import extract_pdf_data, create_new_pdf_content

def word_correction(contents):
    grammar_api_url = "https://api.languagetool.org/v2/check"
    data = {  # refer api to see what parameters to pass
        "text": contents,
        "language": "en"
    }

    # unlike the get request we have to pass additional data parameter a value
    response = requests.post(url=grammar_api_url, data=data)

    # print(type(response.text)) # it returns a string

    # we can convert to dict by using json
    result = json.loads(response.text)

    # Suggestions
    print("Suggestions")
    error_message = result["matches"][0]["message"]
    correction_suggestion = result["matches"][0]["shortMessage"]

    file_contents_copy = contents[:]

    # The way I came up with context offset(starting pos of that letter includes spaces)
    for each_error in result['matches']:
        error_word_loc = each_error["offset"]
        error_word_length = each_error["length"]
        error_word = file_contents[error_word_loc: error_word_loc + error_word_length]
        correct_word = each_error["replacements"][0]["value"]

        # only one time don't collapse other collisions
        # As again never mess up with list/string in loops
        file_contents_copy = file_contents_copy.replace(error_word, correct_word, 1)

        # Suggestion in CLI
        print(error_message)
        print(correction_suggestion)

    return file_contents_copy

def create_new_txt_file(correct_words):
    desktop_path = "/Users/nirmalkumar/Desktop"
    with open(file= f"{desktop_path}/corrected.txt", mode= "w") as new_file:
        new_file.write(correct_words)

filename = askopenfilename()
assert filename.endswith(".txt") or filename.endswith(".pdf"), "Unsupported Format"

file_contents = ''

if filename.endswith(".txt"):
    with open(file= filename, mode= 'r') as file:
        file_contents += file.read()
        corrected_words = word_correction(contents= file_contents)
        create_new_txt_file(correct_words= corrected_words)
elif filename.endswith(".pdf"):
    text_data = extract_pdf_data(filepath= filename)
    file_contents += text_data
    corrected_words = word_correction(contents= file_contents)
    create_new_pdf_content(content= corrected_words)

