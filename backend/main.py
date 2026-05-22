from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader
from dotenv import load_dotenv
import requests
import os
import json

# Load env variables
load_dotenv()

app = FastAPI()

# Enable frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Home route
@app.get("/")
def home():
    return {"message": "AI Resume Analyzer Running 🚀"}


@app.post("/analyze")
async def analyze(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):

    try:

        # Read PDF
        pdf = PdfReader(file.file)

        resume_text = ""

        for page in pdf.pages:
            resume_text += page.extract_text() or ""

        if not resume_text.strip():
            return {
                "error": "Could not extract text from PDF"
            }

        prompt = f"""
        You are an expert ATS Resume Analyzer.

        Compare Resume with Job Description.

        Resume:
        {resume_text}

        Job Description:
        {job_description}

        Rules:
        - Score MUST be integer from 0–100
        - Return ONLY JSON
        - No markdown
        - No explanation text
        - Mention a skill as missing ONLY if absent from resume
        - Do not invent resume content
        - Compare resume strictly against job description
        - Score realistically


        Output format:

        {{
        "score": <integer 0-100>,
        "strengths": [],
        "missing_skills": [],
        "resume_improvements": [],
        "suggested_projects": [],
        "interview_probability":"Low/Medium/High"
        }}
        """

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.3
            }
        )

        result = response.json()

        if "error" in result:
            return result

        content = (
            result["choices"][0]
            ["message"]
            ["content"]
        )

        try:
            parsed = json.loads(content)
            return parsed

        except:
            return {
                "raw_response": content
            }

    except Exception as e:
        return {
            "error": str(e)
        }