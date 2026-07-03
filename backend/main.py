# from fastapi import FastAPI, UploadFile, File, Form
# from fastapi.middleware.cors import CORSMiddleware
# from pypdf import PdfReader
# from dotenv import load_dotenv
# import requests
# import os
# import json
# import io

# # Load env variables
# load_dotenv()

# app = FastAPI()

# # Enable frontend access
# allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# MAX_FILE_SIZE_MB = 10
# MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

# # Home route
# @app.get("/")
# def home():
#     return {"message": "AI Resume Analyzer Running 🚀"}


# @app.post("/analyze")
# async def analyze(
#     file: UploadFile = File(...),
#     job_description: str = Form(...)
# ):

#     if not GROQ_API_KEY:
#         return {"error": "Server is missing GROQ_API_KEY. Set it in backend/.env"}

#     if not job_description or not job_description.strip():
#         return {"error": "Job description is required"}

#     if not file.filename.lower().endswith(".pdf"):
#         return {"error": "Only PDF files are supported"}

#     # Validate file size (read once, reuse the bytes)
#     file_bytes = await file.read()
#     if len(file_bytes) == 0:
#         return {"error": "Uploaded file is empty"}
#     if len(file_bytes) > MAX_FILE_SIZE_BYTES:
#         return {"error": f"File too large. Max size is {MAX_FILE_SIZE_MB}MB"}

#     try:
#         # Read PDF
#         pdf = PdfReader(io.BytesIO(file_bytes))

#         resume_text = ""

#         for page in pdf.pages:
#             resume_text += page.extract_text() or ""

#         if not resume_text.strip():
#             return {
#                 "error": "Could not extract text from PDF"
#             }

#         prompt = f"""
#         You are an expert ATS Resume Analyzer.

#         Compare Resume with Job Description.

#         Resume:
#         {resume_text}

#         Job Description:
#         {job_description}

#         Rules:
#         - Score MUST be integer from 0–100
#         - Return ONLY JSON
#         - No markdown
#         - No explanation text
#         - Mention a skill as missing ONLY if absent from resume
#         - Do not invent resume content
#         - Compare resume strictly against job description
#         - Score realistically


#         Output format:

#         {{
#         "score": <integer 0-100>,
#         "strengths": [],
#         "missing_skills": [],
#         "resume_improvements": [],
#         "suggested_projects": [],
#         "interview_probability":"Low/Medium/High"
#         }}
#         """
# try:
#             response = requests.post(
#                 "https://api.groq.com/openai/v1/chat/completions",
#                 headers={
#                     "Authorization": f"Bearer {GROQ_API_KEY}",
#                     "Content-Type": "application/json"
#                 },
#                 json={
#                     "model": "llama-3.3-70b-versatile",
#                     "messages": [
#                         {
#                             "role": "user",
#                             "content": prompt
#                         }
#                     ],
#                     "temperature": 0.3
#                 },
#                 timeout=30
#             )
#         except requests.exceptions.Timeout:
#             return {"error": "The AI service took too long to respond. Please try again."}
#         except requests.exceptions.RequestException as e:
#             return {"error": f"Could not reach the AI service: {str(e)}"}

#         result = response.json()

#         if "error" in result:
#             return {"error": f"AI service error: {result['error']}"}

#         content = (
#             result["choices"][0]
#             ["message"]
#             ["content"]
#         )

#         try:
#             parsed = json.loads(content)
#             return parsed

#         except:
#             return {
#                 "raw_response": content
#             }

#     except Exception as e:
#         return {
#             "error": str(e)
#         }




from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader
from dotenv import load_dotenv
import requests
import os
import json
import io

# Load env variables
load_dotenv()

app = FastAPI()

# Enable frontend access
# Set ALLOWED_ORIGINS in .env as a comma-separated list for production,
# e.g. ALLOWED_ORIGINS=https://your-frontend.com,http://localhost:5173
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MAX_FILE_SIZE_MB = 10
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024


# Home route
@app.get("/")
def home():
    return {"message": "AI Resume Analyzer Running 🚀"}


@app.post("/analyze")
async def analyze(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):

    if not GROQ_API_KEY:
        return {"error": "Server is missing GROQ_API_KEY. Set it in backend/.env"}

    if not job_description or not job_description.strip():
        return {"error": "Job description is required"}

    if not file.filename.lower().endswith(".pdf"):
        return {"error": "Only PDF files are supported"}

    # Validate file size (read once, reuse the bytes)
    file_bytes = await file.read()
    if len(file_bytes) == 0:
        return {"error": "Uploaded file is empty"}
    if len(file_bytes) > MAX_FILE_SIZE_BYTES:
        return {"error": f"File too large. Max size is {MAX_FILE_SIZE_MB}MB"}

    try:
        # Read PDF
        pdf = PdfReader(io.BytesIO(file_bytes))

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

        try:
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
                },
                timeout=30
            )
        except requests.exceptions.Timeout:
            return {"error": "The AI service took too long to respond. Please try again."}
        except requests.exceptions.RequestException as e:
            return {"error": f"Could not reach the AI service: {str(e)}"}

        result = response.json()

        if "error" in result:
            return {"error": f"AI service error: {result['error']}"}

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