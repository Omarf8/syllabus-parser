import pdfplumber

data = ""

with pdfplumber.open("Math_218_Syllabus_Spring_2026.pdf") as pdf:
    for page in pdf.pages:
        data += f"\n{page.extract_text()}"