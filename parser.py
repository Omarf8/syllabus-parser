from dotenv import load_dotenv
import json
import pdfplumber
from google import genai

load_dotenv()

client = genai.Client()
data = ""

with pdfplumber.open("FILEPATH.pdf") as pdf:
    for page in pdf.pages:
        data += f"\n{page.extract_text()}"

response = client.models.generate_content(
    model="gemini-3-flash-preview", 
    contents=f"Using the following data, I want you to give me back the defined (not TBD) important dates listed such as homework, exams, quizzes, and/or any other types of assignments. Return the raw JSON with no markdown. Your response should be a JSON array where we want the title of the assignment, the type (HOMEWORK, EXAM, etc.), date (YYYY-MM-DD), and the course (NAME NUMBER): {data}"
)

json_list_raw_text = response.text
json_list_text = json_list_raw_text.replace("```json", "").replace("```", "") # Potential md stripping
print(json_list_text)