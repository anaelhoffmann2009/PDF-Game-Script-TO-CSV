import re
import pdfplumber
import pandas as pd
from langdetect import detect

def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def extract_dialogues(text, characters):
    character_pattern = re.compile(r'^(' + '|'.join(characters) + r'):\s*(.*)')
    dialogues = []

    for line in text.split("\n"):
        match = character_pattern.match(line)
        if match:
            character = match.group(1)
            dialogue = match.group(2)
            if "(" in dialogue and ")" in dialogue:
                language = "es"
            else:
                language = "en"
            dialogues.append({"Character": character, "Dialogue": dialogue, "Language": language})
    
    return pd.DataFrame(dialogues)

if __name__ == "__main__":
    pdf_file = "Dianokroft - A Space Odissey - Script.pdf"
    characters = ["AIDA", "MARKUS", "DR. TYLER", "MRS. ARLENE"]
    text = extract_text_from_pdf(pdf_file)
    dialogues_df = extract_dialogues(text, characters)
    character_dialogues = dialogues_df[dialogues_df["Character"] == "Nombre del Personaje"]
    dialogues_count = dialogues_df["Character"].value_counts()
    dialogues_to_csv = dialogues_df.to_csv("dianokroft_dialogs.csv", index=False)

    print(f"CSV file created from PDF file, CSV file name: {dialogues_to_csv}")

    print(dialogues_count)