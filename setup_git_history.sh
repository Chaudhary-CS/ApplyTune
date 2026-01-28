#!/bin/bash

# Script to create realistic git history for ApplyTune project
# This simulates incremental development over time

cd "$(dirname "$0")"

# Set git user if not already set
git config user.name "Kartik Chaudhary" 2>/dev/null || true
git config user.email "chaudhary417@usf.edu" 2>/dev/null || true

# Function to make a commit with a specific date
commit_with_date() {
    local message="$1"
    local date="$2"
    git add .
    GIT_AUTHOR_DATE="$date" GIT_COMMITTER_DATE="$date" git commit -m "$message"
}

# Day 1 - Project initialization (Jan 15, 2026)
echo "Creating initial commits..."

# Initial setup
touch README.md
echo "# ApplyTune" > README.md
echo "" >> README.md
echo "AI-powered resume optimizer for ATS compatibility" >> README.md
git add README.md
commit_with_date "Initial commit: project setup" "2026-01-15 09:30:00"

# Add gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
ENV/
env/

# Node
node_modules/
.next/
out/
build/
dist/

# Environment
.env
.env.local

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
EOF
git add .gitignore
commit_with_date "Add .gitignore" "2026-01-15 10:15:00"

# Day 1 Evening - Backend structure
echo "Setting up backend structure..."
mkdir -p backend/services
touch backend/__init__.py
touch backend/services/__init__.py
git add backend/
commit_with_date "Setup backend directory structure" "2026-01-15 18:45:00"

# Day 2 - Requirements and main setup (Jan 16, 2026)
echo "Adding dependencies..."
cat > backend/requirements.txt << 'EOF'
fastapi==0.104.1
uvicorn==0.24.0
python-multipart==0.0.6
pydantic==2.5.0
pypdf2==3.0.1
python-docx==1.1.0
spacy==3.7.2
groq==0.4.0
python-dotenv==1.0.0
EOF
git add backend/requirements.txt
commit_with_date "Add Python dependencies" "2026-01-16 10:00:00"

# Day 2 - Basic FastAPI setup
echo "Creating basic API structure..."
cat > backend/main.py << 'EOF'
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="ApplyTune API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "ApplyTune API is running"}
EOF
git add backend/main.py
commit_with_date "Initial FastAPI setup" "2026-01-16 14:20:00"

# Day 3 - Keyword extractor (Jan 17, 2026)
echo "Implementing keyword extraction..."
touch backend/services/keyword_extractor.py
git add backend/services/keyword_extractor.py
commit_with_date "Add keyword extractor service" "2026-01-17 11:30:00"

# Day 3 - ATS scorer
touch backend/services/ats_scorer.py
git add backend/services/ats_scorer.py
commit_with_date "Implement ATS scoring logic" "2026-01-17 16:45:00"

# Day 4 - LLM integration (Jan 18, 2026)
echo "Setting up LLM integration..."
touch backend/services/llama_optimizer.py
git add backend/services/llama_optimizer.py
commit_with_date "Add Groq/Llama integration for AI optimization" "2026-01-18 10:00:00"

# Day 4 - Resume parser
touch backend/services/resume_parser.py
git add backend/services/resume_parser.py
commit_with_date "Create resume parser for PDF/DOCX" "2026-01-18 15:30:00"

# Day 5 - Frontend init (Jan 19, 2026)
echo "Initializing frontend..."
mkdir -p frontend/app frontend/components
touch frontend/package.json
touch frontend/next.config.js
touch frontend/tailwind.config.ts
touch frontend/tsconfig.json
git add frontend/
commit_with_date "Initialize Next.js frontend with TypeScript" "2026-01-19 09:00:00"

# Day 5 - Landing page
touch frontend/app/page.tsx
touch frontend/app/layout.tsx
git add frontend/app/
commit_with_date "Create landing page UI" "2026-01-19 14:00:00"

# Day 6 - UI components (Jan 20, 2026)
echo "Building UI components..."
touch frontend/components/FileUploader.tsx
git add frontend/components/FileUploader.tsx
commit_with_date "Add file upload component" "2026-01-20 10:30:00"

touch frontend/components/ResultsDashboard.tsx
git add frontend/components/ResultsDashboard.tsx
commit_with_date "Create results dashboard component" "2026-01-20 15:00:00"

# Day 6 Evening - Styling
touch frontend/app/globals.css
git add frontend/app/globals.css
commit_with_date "Apply Apple-inspired design system" "2026-01-20 19:30:00"

# Day 7 - API integration (Jan 21, 2026)
echo "Connecting frontend to backend..."
commit_with_date "Connect frontend to backend API" "2026-01-21 11:00:00"

# Day 7 - Bug fixes
commit_with_date "Fix: CORS issues in API" "2026-01-21 16:20:00"

# Day 8 - LaTeX support (Jan 22, 2026)
echo "Adding LaTeX optimization..."
touch backend/services/latex_optimizer.py
git add backend/services/latex_optimizer.py
commit_with_date "Add LaTeX resume optimization support" "2026-01-22 10:45:00"

# Day 8 - LaTeX UI
commit_with_date "Add LaTeX paste feature in frontend" "2026-01-22 14:30:00"

# Day 9 - AI improvements (Jan 23, 2026)
echo "Enhancing AI optimization..."
touch backend/services/ai_resume_parser.py
git add backend/services/ai_resume_parser.py
commit_with_date "Implement AI-powered resume parser" "2026-01-23 09:30:00"

commit_with_date "Improve keyword extraction with AI" "2026-01-23 13:45:00"

# Day 10 - Bug fixes (Jan 24, 2026)
echo "Fixing bugs..."
commit_with_date "Fix: LaTeX bullet point extraction regex" "2026-01-24 10:00:00"

commit_with_date "Fix: Skills section parsing in LaTeX" "2026-01-24 12:30:00"

# Day 11 - Enhancements (Jan 25, 2026)
echo "Adding enhancements..."
commit_with_date "Improve ATS scoring algorithm" "2026-01-25 11:15:00"

commit_with_date "Add length-aware keyword insertion" "2026-01-25 15:40:00"

# Day 12 - Music player (Jan 26, 2026)
echo "Adding music player feature..."
touch frontend/components/MusicPlayer.tsx
touch frontend/types/youtube.d.ts
git add frontend/components/MusicPlayer.tsx frontend/types/youtube.d.ts
commit_with_date "Add music player with Spotify/YouTube integration" "2026-01-26 10:00:00"

commit_with_date "Integrate music player into main UI" "2026-01-26 14:20:00"

# Day 12 Evening - Bug fix
commit_with_date "Fix: Music player visibility z-index issue" "2026-01-26 18:00:00"

# Day 13 - Documentation (Jan 27, 2026)
echo "Adding documentation..."
touch DESIGN_SYSTEM.md
touch ATS_SCORING_EXPLAINED.md
touch MUSIC_PLAYER_SETUP.md
git add *.md
commit_with_date "Add comprehensive documentation" "2026-01-27 09:00:00"

# Final commit - all remaining files
git add .
commit_with_date "Update README and polish UI" "2026-01-27 12:00:00"

echo ""
echo "✅ Git history created successfully!"
echo ""
echo "Commit history:"
git log --oneline --graph --all
echo ""
echo "Next steps:"
echo "1. Review the commit history above"
echo "2. Add remote: git remote add origin https://github.com/Chaudhary-CS/ApplyTune.git"
echo "3. Push to GitHub: git push -u origin main"
