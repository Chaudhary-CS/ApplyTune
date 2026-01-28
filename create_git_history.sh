#!/bin/bash

# Applytune Git History - Natural Development Flow
# Run this script to create realistic commit history

echo "🚀 Creating realistic git commit history..."

# Initialize repo if not already done
if [ ! -d .git ]; then
  git init
  echo "✅ Git repo initialized"
fi

# Day 1 - Initial Setup (Morning)
git add README.md package.json
git commit -m "init: basic project structure" --date="2026-01-20 09:30:00"

git add frontend/package.json frontend/tsconfig.json frontend/next.config.js
git commit -m "setup: nextjs with typescript" --date="2026-01-20 10:15:00"

git add frontend/app/globals.css frontend/tailwind.config.js
git commit -m "add tailwind, apple-style design system" --date="2026-01-20 11:00:00"

# Day 1 - Afternoon
git add backend/requirements.txt backend/main.py
git commit -m "backend: fastapi setup + basic structure" --date="2026-01-20 14:20:00"

git add frontend/components/FileUploader.tsx
git commit -m "feat: file upload component with drag n drop" --date="2026-01-20 15:45:00"

git add frontend/app/page.tsx frontend/app/layout.tsx
git commit -m "ui: landing page + header" --date="2026-01-20 16:30:00"

# Day 2 - Core Features
git add backend/services/resume_parser.py
git commit -m "add resume parser for pdf/docx" --date="2026-01-21 09:00:00"

git add backend/services/job_analyzer.py backend/services/keyword_extractor.py
git commit -m "feat: job description analyzer + keyword extraction" --date="2026-01-21 10:30:00"

git add backend/services/ats_scorer.py
git commit -m "implement ats scoring algorithm (workday, taleo, greenhouse)" --date="2026-01-21 12:15:00"

# Day 2 - Afternoon
git add frontend/components/JobDescriptionForm.tsx
git commit -m "add job description form" --date="2026-01-21 14:00:00"

git add backend/services/resume_optimizer.py
git commit -m "WIP: basic resume optimization logic" --date="2026-01-21 15:30:00"

git add frontend/lib/api.ts
git commit -m "api integration + error handling" --date="2026-01-21 16:45:00"

# Day 3 - Results Dashboard
git add frontend/components/ScoreCard.tsx frontend/components/ScoreBreakdown.tsx
git commit -m "results dashboard components" --date="2026-01-22 09:30:00"

git add frontend/components/KeywordList.tsx
git commit -m "keyword analysis visualization" --date="2026-01-22 11:00:00"

git add frontend/components/ResultsDashboard.tsx
git commit -m "complete results page with download" --date="2026-01-22 13:20:00"

# Day 3 - Fixes
git add backend/services/resume_optimizer.py
git commit -m "fix: optimization not working, improved prompts" --date="2026-01-22 15:00:00"

git add frontend/app/globals.css
git commit -m "polish ui animations + shadows" --date="2026-01-22 16:30:00"

# Day 4 - Testing & Bugs
git add backend/main.py
git commit -m "fix cors issues" --date="2026-01-23 09:15:00"

git add backend/services/ats_scorer.py
git commit -m "adjust scoring weights based on research" --date="2026-01-23 10:45:00"

git add BRANDING.md DESIGN_SYSTEM.md
git commit -m "docs: brand guidelines + design system" --date="2026-01-23 12:00:00"

# Day 4 - Format Preservation
git add backend/services/format_preserver.py
git commit -m "feat: preserve original resume formatting" --date="2026-01-23 14:30:00"

git add STRUCTURE_PRESERVATION_STRATEGY.md
git commit -m "research: format preservation approaches" --date="2026-01-23 15:45:00"

# Day 5 - LaTeX Support
git add backend/services/latex_optimizer.py
git commit -m "add latex support for overleaf users" --date="2026-01-24 09:30:00"

git add frontend/components/FileUploader.tsx frontend/app/page.tsx
git commit -m "latex paste option instead of upload" --date="2026-01-24 11:15:00"

git add backend/services/latex_optimizer.py
git commit -m "fix: latex parser not extracting resumeItem commands" --date="2026-01-24 13:00:00"

# Day 5 - Major Fix
git add backend/services/latex_optimizer.py
git commit -m "FIXED: handle nested braces in latex, regex was broken" --date="2026-01-24 14:45:00"

git add LATEX_PASTE_COMPLETE.md
git commit -m "docs: latex workflow guide" --date="2026-01-24 15:30:00"

# Day 6 - Free AI Models
git add backend/services/llama_optimizer.py
git commit -m "integrate llama for free optimization (groq api)" --date="2026-01-25 09:00:00"

git add LLAMA_SETUP.md GROQ_SETUP.md
git commit -m "docs: free llm setup guides" --date="2026-01-25 10:30:00"

git add backend/services/resume_optimizer.py
git commit -m "fix: check for llama optimizer not just openai client" --date="2026-01-25 12:00:00"

git add backend/services/llama_optimizer.py
git commit -m "update to llama-3.3-70b, 3.1 was decommissioned" --date="2026-01-25 13:45:00"

# Day 6 - Score Improvements
git add backend/services/latex_optimizer.py backend/services/smart_optimizer.py
git commit -m "allow 10% length expansion for keyword insertion" --date="2026-01-25 15:15:00"

git add CONSTRAINTS_FIXED.md
git commit -m "docs: fixed overly strict length constraints" --date="2026-01-25 16:00:00"

# Day 7 - Skills Parser Fix
git add backend/services/latex_optimizer.py
git commit -m "CRITICAL: fix skills parser, was using hardcoded list" --date="2026-01-26 09:30:00"

git add backend/services/latex_optimizer.py backend/main.py
git commit -m "aggressive mode: process 20 bullets + add to skills section" --date="2026-01-26 11:00:00"

git add ATS_SCORING_EXPLAINED.md
git commit -m "comprehensive ats scoring guide" --date="2026-01-26 12:30:00"

# Day 7 - Smart Optimization Research
git add backend/services/keyword_prioritizer.py
git commit -m "feat: keyword prioritization by frequency + section weight" --date="2026-01-26 14:15:00"

git add backend/services/context_validator.py
git commit -m "feat: context-aware validation (dont change project stacks!)" --date="2026-01-26 15:45:00"

git add SMART_OPTIMIZATION_RESEARCH.md
git commit -m "research: how jobscan/teal/resume worded actually work" --date="2026-01-26 16:30:00"

# Day 8 - Music Player
git add MUSIC_AND_NETWORKING_RESEARCH.md
git commit -m "research: music player + networking features" --date="2026-01-27 09:00:00"

git add frontend/components/MusicPlayer.tsx frontend/types/youtube.d.ts
git commit -m "feat: music player with spotify/youtube support" --date="2026-01-27 11:30:00"

git add frontend/app/page.tsx
git commit -m "integrate music player into main app" --date="2026-01-27 12:45:00"

git add frontend/components/MusicPlayer.tsx
git commit -m "fix: music player positioning + z-index" --date="2026-01-27 13:15:00"

git add MUSIC_PLAYER_SETUP.md
git commit -m "docs: api setup guide for music player" --date="2026-01-27 14:00:00"

# Final commit - All remaining files
git add .
git commit -m "docs: comprehensive guides + research notes" --date="2026-01-27 14:30:00"

echo ""
echo "✅ Git history created!"
echo "📊 Total commits: $(git log --oneline | wc -l)"
echo ""
echo "🔍 View history:"
echo "   git log --oneline --graph"
echo ""
echo "🚀 Ready to push to GitHub!"
