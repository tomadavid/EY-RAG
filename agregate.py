import pandas as pd
import os
import fitz 

data = pd.read_excel("Data/EY AI Challenge_Estrutura SLs_Partners.xlsx")

roles = ""
for i in range(len(data)):
    role = data.iloc[i][data.columns[0]]
    worker = data.iloc[i][data.columns[1]]
    roles += f"{worker} é o {role}\n"

with open("data.txt", "w", encoding="utf-8") as cv:  # open once

    cv.write("===== TRABALHADORES \n")
    cv.write(roles + "\n")

    for filename in os.listdir("Data/workers"):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join("Data/workers", filename)
            doc = fitz.open(pdf_path)

            cv.write(f"===== {filename}\n")  # file header
            for page_num, page in enumerate(doc, start=1):
                text = page.get_text()
                if text:
                    cv.write(f"[Page {page_num}]\n{text}\n")
            doc.close()

    for filename in os.listdir("Data/about"):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join("Data/about", filename)
            doc = fitz.open(pdf_path)

            cv.write(f"===== {filename}\n")
            for page_num, page in enumerate(doc, start=1):
                text = page.get_text()
                if text:
                    cv.write(f"[Page {page_num}]\n{text}\n")
            doc.close()

        elif filename.endswith(".txt"):
            txt_path = os.path.join("Data/about", filename)
            cv.write(f"--- {filename} ---\n")
            with open(txt_path, "r", encoding="utf-8") as txt_file:
                cv.write(txt_file.read() + "\n")
