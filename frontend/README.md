# AI Resume Analyzer

An AI-powered web application that analyzes a resume against a job description and provides ATS-style insights.

Upload a resume PDF, paste a job description, and receive:
- ATS compatibility score
- Missing skills
- Resume strengths
- Improvement suggestions
- Interview probability

Built with React, FastAPI, Groq API, and PDF text extraction.

---

## Preview

Analyze resumes in seconds with:
- Resume upload
- Job description matching
- AI-generated recommendations
- Modern dashboard UI

---

## Features

- Resume PDF upload
- Job description input
- ATS score generation
- Missing skills detection
- Resume strengths analysis
- Resume improvement recommendations
- Interview probability estimation
- Responsive frontend dashboard

---

## Tech Stack

### Frontend
- React
- Vite
- CSS
- Axios

### Backend
- FastAPI
- Python
- PyPDF

### AI Integration
- Groq API
- Llama model

---

## Project Structure

```plaintext
AI-Resume-Analyzer/

├── backend/
│   ├── main.py
│   ├── .env
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   │
│   ├── package.json
│   └── vite.config.js
│
├── .gitignore
└── README.md
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/rithika88/AI-Resume-Analyzer.git
```

```bash
cd AI-Resume-Analyzer
```

---

## Backend Setup

Open terminal:

```bash
cd backend
```

Install dependencies:

```bash
pip install fastapi uvicorn python-multipart pypdf requests python-dotenv
```

Create `.env`

```env
GROQ_API_KEY=your_groq_api_key
```

Run backend:

```bash
python -m uvicorn main:app --reload
```

Backend:

```plaintext
http://127.0.0.1:8000
```

---

## Frontend Setup

Open another terminal:

```bash
cd frontend
```

Install packages:

```bash
npm install
```

Start frontend:

```bash
npm run dev
```

Frontend:

```plaintext
http://localhost:5173
```

---

## Usage

1. Upload resume PDF
2. Paste job description
3. Click **Analyze Resume**
4. View:
   - ATS Score
   - Missing Skills
   - Strengths
   - Resume Improvements
   - Interview Probability

---

## Example Output

```plaintext
ATS Score → 80/100

Missing Skills
- Cloud Platforms
- Docker

Strengths
- React
- Python
- Databricks

Interview Probability
- High
```

---

## Future Improvements

- Resume history
- Export analysis
- Authentication
- Multiple resume support
- Deployment

---

## Author

Rithika

GitHub:
https://github.com/rithika88
