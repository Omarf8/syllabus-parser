from dotenv import load_dotenv
import pdfplumber
from google import genai

load_dotenv()

client = genai.Client()
data = ""

with pdfplumber.open("FILEPATH") as pdf:
    for page in pdf.pages:
        data += f"\n{page.extract_text()}"

response = client.models.generate_content(
    model="gemini-3-flash-preview", 
    contents=f"Using the following data, I want you to give me back the defined (not TBD) important dates listed such as homework, exams, and/or quizzes. Your response should be formatted as 'COURSE - TYPE DATE': \n{data}"
)

print(response.text)