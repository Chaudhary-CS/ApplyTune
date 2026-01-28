# ApplyTune 🎯

A Python-powered resume optimization pipeline that scores resumes against job descriptions
and rewrites them for ATS compatibility. The core problem: most resume optimizers either
keyword-stuff blindly or require manual editing. ApplyTune uses a 3-layer AI validation
system to insert keywords authentically, preserving the original structure and tone while
improving pass rates.

## 🏗️ Pipeline Architecture

```
Input: raw resume (PDF/text) + job description
  │
  ├── Layer 1: AI resume parser        extracts structured data from unformatted text
  ├── Layer 2: JD keyword extractor    identifies required skills, tools, and phrases
  ├── Layer 3: ATS scoring engine      scores match, flags gaps, ranks by weight
  │
  └── Output: optimized resume + diff view showing every change made
```

The pipeline supports multiple AI backends: Groq (cloud, fast), Llama via Ollama (local,
private), with automatic fallback if the primary model is unavailable. This was a deliberate
reliability decision — the tool should work regardless of whether the user has API credits
or an internet connection.

## 🚀 Features

- **AI resume parsing** - extracts structured fields from unformatted PDF or plain text input
- **Keyword extraction** - uses LLMs to identify JD requirements, not hardcoded dictionaries
- **ATS scoring** - real-time match percentage with weighted gap analysis
- **Split-screen preview** - live diff view showing original vs. optimized side by side
- **Genuinity scoring** - flags over-optimized sections that read as keyword-stuffed
- **Multi-model support** - Groq, Llama, Ollama backends with automatic fallback
- **Format preservation** - rewrites content without breaking PDF structure or LaTeX formatting

## 🛠️ Tech Stack

### Backend
- **Python** - core pipeline logic
- **FastAPI** - REST API layer
- **Groq API / Ollama** - LLM backends for parsing and optimization
- **PyMuPDF / pdfplumber** - PDF parsing and text extraction

### Frontend
- **React** - UI framework
- **Split-screen diff viewer** - real-time comparison with toggle controls

## 📦 Setup

```bash
# Backend
cd backend
pip install -r requirements.txt
cp .env.example .env
# set GROQ_API_KEY (optional if using Ollama)
python main.py

# Frontend
cd frontend
npm install
npm start
```

To use local models instead of Groq:
```bash
ollama pull llama3
# set OLLAMA_MODEL=llama3 in .env
```

## 🧪 Testing

```bash
cd backend
pytest tests/
```

Test suite covers the AI parser, keyword extraction accuracy, ATS scoring logic, and
fallback behavior when the primary model is unavailable.

## 📊 Observability

The pipeline logs token usage, model response time, and scoring deltas on every run.
This makes it straightforward to compare model performance and catch regressions when
switching between Groq and Ollama backends.

## 🔧 What I'd Change

The current ATS scoring runs sequentially: parse, extract, score. For longer resumes
this adds noticeable latency. The right approach is to parallelize keyword extraction
and initial parsing since they don't depend on each other, then merge results before
scoring. I'd also replace the file-based logging with structured JSON logs that can
feed into a proper monitoring dashboard, making model performance trends visible over time.

## 👨‍💻 Developer

**Kartik Chaudhary**
- Email: chaudhary417@usf.edu
- GitHub: [@Chaudhary-CS](https://github.com/Chaudhary-CS)
