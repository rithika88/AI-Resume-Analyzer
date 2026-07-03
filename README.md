# AI Resume Analyzer

An AI-powered tool that compares your resume against a job description and gives you an ATS compatibility score, missing skills, strengths, and actionable improvement suggestions.

## Features
- 📄 Upload a resume (PDF) and paste a job description
- 🤖 AI-powered analysis using the Groq API (Llama 3.3 70B)
- 📊 ATS compatibility score (0–100) with visual score ring
- ✅ Highlights your strengths and matched skills
- ⚠️ Flags missing skills relevant to the job description
- ✎ Suggests concrete resume improvements
- 🎯 Estimates interview probability (Low / Medium / High)

## Tech Stack
**Backend:** FastAPI, pypdf, Groq API (via `requests`), python-dotenv
**Frontend:** React 19, Vite, Axios

## Project Structure
```
AI-Resume-Analyzer/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── .env.example
── frontend/
   ├── src/
   │   ├── App.jsx
   │   └── App.css
   ├── package.json
   └── .env.example


```



## Prerequisites
- Python 3.9+
- Node.js 18+
- A free Groq API key — get one at [console.groq.com](https://console.groq.com)

## Setup

### 1. Clone the repo
```bash
git clone <your-repo-url>
cd AI-Resume-Analyzer
```

### 2. Backend setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

Create a `.env` file in `backend/` (copy from `.env.example`):
```
GROQ_API_KEY=your_groq_api_key_here
ALLOWED_ORIGINS=http://localhost:5173

```
Run the backend:
```bash
uvicorn main:app --reload --port 8000
```
The API will be live at `http://127.0.0.1:8000`. Visiting it should show:
```json
{"message": "AI Resume Analyzer Running 🚀"}
```

### 3. Frontend setup
Open a new terminal:
```bash
cd frontend
npm install
```

Create a `.env` file in `frontend/` (copy from `.env.example`):
```
VITE_API_URL=http://127.0.0.1:8000
```
Run the frontend:
```bash
npm run dev
```
The app will be live at `http://localhost:5173`.

## Usage
1. Open `http://localhost:5173` in your browser
2. Drag and drop (or click to browse) a PDF resume — max 10MB
3. Paste the job description into the text box
4. Click **Analyze Resume**
5. Review your ATS score, missing skills, strengths, and improvement suggestions

## Environment Variables

**Backend (`backend/.env`)**
| Variable | Description |
|---|---|
| `GROQ_API_KEY` | Your Groq API key (required) |
| `ALLOWED_ORIGINS` | Comma-separated list of allowed frontend origins for CORS |

**Frontend (`frontend/.env`)**
| Variable | Description |
|---|---|
| `VITE_API_URL` | URL of the backend API |

## Notes
- Resumes are processed in memory and are not stored on disk or in a database.
- Only PDF files are supported.
- The AI analysis quality depends on the Groq model's output; the app expects strict JSON back from the model and will surface a `raw_response` if parsing fails.



