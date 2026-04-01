from dotenv import load_dotenv
import json
import pdfplumber
import io
from google import genai
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from google_auth_oauthlib.flow import Flow

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/calendar.events"] # Google Calendar Scope

app = FastAPI()
oauth_states = set()

origins = [
    "http://localhost:5173",
    "http://localhost:5174"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)

client = genai.Client()

@app.post("/uploadfile/")
async def parse_syllabus(file: UploadFile):
    rawBytes = await file.read()
    syllabus = io.BytesIO(rawBytes)

    data = ""
    with pdfplumber.open(syllabus) as pdf:
        for page in pdf.pages:
            data += f"\n{page.extract_text()}"

    response = client.models.generate_content(
        model="gemini-3-flash-preview", 
        contents=f"Using the following data, I want you to give me back the defined (not TBD) important dates listed such as homework, exams, quizzes, and/or any other types of assignments. Return the raw JSON with no markdown. Your response should be a JSON array where we want the title of the assignment, the type (HOMEWORK, EXAM, etc.), date (YYYY-MM-DD), and the course (NAME NUMBER): {data}"
    )

    gemini_text = response.text
    json_text = gemini_text.replace("```json", "").replace("```", "") # Potential md stripping
    return json.loads(json_text)

@app.get("/auth/login/")
def login_auth():
    flow = Flow.from_client_secrets_file("credentials.json", scopes=SCOPES, redirect_uri="http://localhost:8000/auth/callback")
    url, state = flow.authorization_url()
    oauth_states.add(state)
    return {"url": url}
