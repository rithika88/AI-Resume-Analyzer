import { useState, useRef } from "react";
import axios from "axios";
import "./App.css";

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

function ScoreRing({ score }) {
  const radius = 54;
  const circumference = 2 * Math.PI * radius;
  const filled = (score / 100) * circumference;
  const color =
    score >= 75 ? "#16a34a" : score >= 50 ? "#d97706" : "#dc2626";

  return (
    <div className="score-ring-wrapper">
      <svg width="140" height="140" viewBox="0 0 140 140">
        <circle
          cx="70" cy="70" r={radius}
          fill="none" stroke="#f1f5f9" strokeWidth="10"
        />
        <circle
          cx="70" cy="70" r={radius}
          fill="none"
          stroke={color}
          strokeWidth="10"
          strokeDasharray={`${filled} ${circumference}`}
          strokeDashoffset="0"
          strokeLinecap="round"
          transform="rotate(-90 70 70)"
          className="score-arc"
        />
      </svg>
      <div className="score-center">
        <span className="score-number" style={{ color }}>{score}</span>
        <span className="score-label">/ 100</span>
      </div>
    </div>
  );
}

function Tag({ children, variant = "default" }) {
  return <span className={`tag tag--${variant}`}>{children}</span>;
}

function ResultCard({ title, icon, items, variant }) {
  return (
    <div className={`result-card result-card--${variant}`}>
      <div className="result-card__header">
        <span className="result-card__icon">{icon}</span>
        <h3 className="result-card__title">{title}</h3>
      </div>
      <ul className="result-list">
        {items?.map((item, i) => (
          <li key={i} className="result-list__item">
            <span className="result-list__dot" />
            {item}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default function App() {
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [dragging, setDragging] = useState(false);
  const fileInputRef = useRef();

  const handleAnalyze = async () => {
    if (!file) { alert("Please upload a resume"); return; }
    if (!jobDescription.trim()) { alert("Please paste a job description"); return; }

    setLoading(true);
    setResult(null);
    try {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("job_description", jobDescription);
      const res = await axios.post(`${API_URL}/analyze`, formData);

      if (res.data.error) {
        alert(res.data.error);
        return;
      }

      setResult(res.data);
    } catch (error) {
      console.error(error);
      alert(error.response?.data?.error || "Analysis failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragging(false);
    const dropped = e.dataTransfer.files[0];
    if (dropped && dropped.type === "application/pdf") setFile(dropped);
  };

  const scoreLabel = result
    ? result.score >= 75 ? "Strong Match" : result.score >= 50 ? "Moderate Match" : "Needs Work"
    : "";

  return (
    <div className="app">
      {/* Nav */}
      <header className="nav">
        <div className="nav__inner">
          {/* <div className="nav__logo">
            <span className="nav__logo-mark"></span>
            <span className="nav__logo-text">Resume Analyzer</span> */}
          {/* </div> */}
          
        </div>
      </header>

      {/* Hero */}
      {!result && (
        <section className="hero">
          <h1 className="hero__heading-title">Resume Analyzer</h1>
          <div className="hero__eyebrow">
            <span className="eyebrow-badge">AI-Powered · Free to try</span>
          </div>
          <h1 className="hero__heading">
            Know exactly how your<br />
            <span className="hero__heading-accent">resume performs</span>
          </h1>
          <p className="hero__sub">
            Upload your resume and a job description. Get an ATS score, missing skills,
            strengths, and actionable improvements — in seconds.
          </p>
        </section>
      )}

      {/* Upload Card */}
      {!result && (
        <main className="upload-section">
          <div className="upload-card">
            <div
              className={`dropzone ${dragging ? "dropzone--active" : ""} ${file ? "dropzone--filled" : ""}`}
              onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
              onDragLeave={() => setDragging(false)}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current.click()}
            >
              <input
                ref={fileInputRef}
                type="file"
                accept=".pdf"
                style={{ display: "none" }}
                onChange={(e) => setFile(e.target.files[0])}
              />
              {file ? (
                <>
                  <span className="dropzone__icon dropzone__icon--file">📄</span>
                  <p className="dropzone__filename">{file.name}</p>
                  <p className="dropzone__hint">Click to replace</p>
                </>
              ) : (
                <>
                  <span className="dropzone__icon">↑</span>
                  <p className="dropzone__text">Drop your resume here</p>
                  <p className="dropzone__hint">PDF only · Max 10MB · Click to browse</p>
                </>
              )}
            </div>

            <div className="field">
              <label className="field__label">Job Description</label>
              <textarea
                className="field__textarea"
                placeholder="Paste the full job description here…"
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
              />
            </div>

            <button
              className={`analyze-btn ${loading ? "analyze-btn--loading" : ""}`}
              onClick={handleAnalyze}
              disabled={loading}
            >
              {loading ? (
                <span className="analyze-btn__inner">
                  <span className="spinner" />
                  Analyzing resume…
                </span>
              ) : (
                <span className="analyze-btn__inner">
                  Analyze Resume
                  <span className="analyze-btn__arrow">→</span>
                </span>
              )}
            </button>

            <p className="upload-disclaimer">
              Your resume is processed securely and never stored.
            </p>
          </div>
        </main>
      )}

      {/* Results Dashboard */}
      {result && (
        <main className="results-section">
          <div className="results-header">
            <div>
              <h2 className="results-title">Analysis Complete</h2>
              <p className="results-subtitle">
                Here's how your resume matches the job description.
              </p>
            </div>
            <button className="reset-btn" onClick={() => setResult(null)}>
              ← Analyze another
            </button>
          </div>

          {/* Score Banner */}
          <div className="score-banner">
            <div className="score-banner__left">
              <ScoreRing score={result.score} />
              <div className="score-banner__info">
                <p className="score-banner__label">ATS Compatibility Score</p>
                <p className="score-banner__verdict">{scoreLabel}</p>
                <p className="score-banner__desc">
                  Based on keyword matching, structure, and alignment with the job description.
                </p>
              </div>
            </div>
            <div className="score-tags">
              {result.score >= 75 && <Tag variant="green">High ATS Match</Tag>}
              {result.score >= 50 && result.score < 75 && <Tag variant="amber">Medium ATS Match</Tag>}
              {result.score < 50 && <Tag variant="red">Low ATS Match</Tag>}
              {result.missing_skills?.length === 0 && <Tag variant="green">All Skills Present</Tag>}
              {result.strengths?.length > 0 && <Tag variant="blue">{result.strengths.length} Strengths Found</Tag>}
            </div>
          </div>

          {/* Result Grid */}
          <div className="result-grid">
            <ResultCard
              title="Missing Skills"
              icon="⚠"
              items={result.missing_skills}
              variant="red"
            />
            <ResultCard
              title="Your Strengths"
              icon="✦"
              items={result.strengths}
              variant="green"
            />
            <ResultCard
              title="Resume Improvements"
              icon="✎"
              items={result.resume_improvements}
              variant="blue"
            />
            <ResultCard
              title="Interview Probability"
              icon="◎"
              items={result.interview_probability
                ? (Array.isArray(result.interview_probability)
                    ? result.interview_probability
                    : [result.interview_probability])
                : ["No data available"]}
              variant="purple"
            />
          </div>
        </main>
      )}

    </div>
  );
}