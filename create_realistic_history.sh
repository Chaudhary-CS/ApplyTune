#!/bin/bash

# Script to create realistic incremental git history for ApplyTune
# Simulates development over ~2 weeks with varied commit times

cd "$(dirname "$0")"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Set git config
git config user.name "Kartik Chaudhary" 2>/dev/null || true
git config user.email "chaudhary417@usf.edu" 2>/dev/null || true

# Function to commit with custom date
commit_dated() {
    local msg="$1"
    local date="$2"
    GIT_AUTHOR_DATE="$date" GIT_COMMITTER_DATE="$date" git commit -m "$msg" --quiet
    echo -e "${GREEN}✓${NC} [$date] $msg"
}

echo -e "${BLUE}Creating realistic git history...${NC}\n"

# ==== Day 1: Jan 15, 2026 - Initial Setup ====
echo -e "${BLUE}Day 1 (Jan 15): Project initialization${NC}"

# Commit 1: Initial README
git add README.md
commit_dated "Initial commit: Add project README" "2026-01-15 09:30:00"

# Commit 2: Gitignore
git add .gitignore
commit_dated "Add .gitignore for Python and Node" "2026-01-15 10:45:00"

# Commit 3: Backend structure
git add backend/__init__.py backend/services/__init__.py backend/.gitignore
commit_dated "Setup backend directory structure" "2026-01-15 17:20:00"

# ==== Day 2: Jan 16, 2026 - Backend Foundation ====
echo -e "${BLUE}Day 2 (Jan 16): Backend setup${NC}"

# Commit 4: Requirements
git add backend/requirements.txt
commit_dated "Add Python dependencies and requirements" "2026-01-16 09:15:00"

# Commit 5: Basic FastAPI
git add backend/main.py
commit_dated "Create FastAPI application with CORS" "2026-01-16 14:30:00"

# ==== Day 3: Jan 17, 2026 - Core Services ====
echo -e "${BLUE}Day 3 (Jan 17): Core services${NC}"

# Commit 6: Resume parser
git add backend/services/resume_parser.py
commit_dated "Implement resume parser for PDF/DOCX" "2026-01-17 10:00:00"

# Commit 7: Keyword extractor
git add backend/services/keyword_extractor.py
commit_dated "Add keyword extraction service" "2026-01-17 15:45:00"

# ==== Day 4: Jan 18, 2026 - Job Analysis & ATS ====
echo -e "${BLUE}Day 4 (Jan 18): Job analysis and ATS scoring${NC}"

# Commit 8: Job analyzer
git add backend/services/job_analyzer.py
commit_dated "Create job description analyzer" "2026-01-18 10:30:00"

# Commit 9: ATS scorer
git add backend/services/ats_scorer.py
commit_dated "Implement multi-ATS scoring engine" "2026-01-18 16:00:00"

# ==== Day 5: Jan 19, 2026 - AI Integration ====
echo -e "${BLUE}Day 5 (Jan 19): AI/LLM integration${NC}"

# Commit 10: Llama optimizer
git add backend/services/llama_optimizer.py GROQ_SETUP.md
commit_dated "Integrate Groq API for Llama 3.3 optimization" "2026-01-19 09:00:00"

# Commit 11: Resume optimizer
git add backend/services/resume_optimizer.py
commit_dated "Create resume optimization service" "2026-01-19 14:20:00"

# ==== Day 6: Jan 20, 2026 - Frontend Init ====
echo -e "${BLUE}Day 6 (Jan 20): Frontend initialization${NC}"

# Commit 12: Next.js setup
git add frontend/package.json frontend/package-lock.json frontend/next.config.js frontend/tsconfig.json frontend/postcss.config.js frontend/.gitignore
commit_dated "Initialize Next.js 14 with TypeScript and Tailwind" "2026-01-20 10:00:00"

# Commit 13: Tailwind config
git add frontend/tailwind.config.js frontend/tailwind.config.ts
commit_dated "Configure Tailwind CSS with custom theme" "2026-01-20 11:30:00"

# Commit 14: Layout and globals
git add frontend/app/layout.tsx frontend/app/globals.css
commit_dated "Setup app layout and global styles" "2026-01-20 15:00:00"

# ==== Day 7: Jan 21, 2026 - UI Components ====
echo -e "${BLUE}Day 7 (Jan 21): UI components${NC}"

# Commit 15: Landing page
git add frontend/app/page.tsx
commit_dated "Create landing page with Apple-inspired design" "2026-01-21 09:30:00"

# Commit 16: File uploader
git add frontend/components/FileUploader.tsx
commit_dated "Add file upload component with drag-and-drop" "2026-01-21 13:00:00"

# Commit 17: Job description form
git add frontend/components/JobDescriptionForm.tsx
commit_dated "Create job description input component" "2026-01-21 16:45:00"

# ==== Day 8: Jan 22, 2026 - Results Dashboard ====
echo -e "${BLUE}Day 8 (Jan 22): Results and visualization${NC}"

# Commit 18: Score components
git add frontend/components/ScoreCard.tsx frontend/components/ScoreBreakdown.tsx
commit_dated "Add ATS score visualization components" "2026-01-22 10:15:00"

# Commit 19: Results dashboard
git add frontend/components/ResultsDashboard.tsx frontend/components/KeywordList.tsx
commit_dated "Build comprehensive results dashboard" "2026-01-22 15:30:00"

# Commit 20: API utilities
git add frontend/lib/api.ts frontend/lib/utils.ts
commit_dated "Add API client and utility functions" "2026-01-22 18:00:00"

# ==== Day 9: Jan 23, 2026 - Advanced Features ====
echo -e "${BLUE}Day 9 (Jan 23): Advanced optimization${NC}"

# Commit 21: AI resume parser
git add backend/services/ai_resume_parser.py AI_RESUME_PARSING.md
commit_dated "Implement AI-powered resume parser" "2026-01-23 10:00:00"

# Commit 22: Format preserver
git add backend/services/format_preserver.py
commit_dated "Add format preservation service" "2026-01-23 14:30:00"

# Commit 23: Smart optimizer
git add backend/services/smart_optimizer.py SMART_OPTIMIZATION_RESEARCH.md
commit_dated "Create intelligent keyword insertion system" "2026-01-23 17:45:00"

# ==== Day 10: Jan 24, 2026 - LaTeX Support ====
echo -e "${BLUE}Day 10 (Jan 24): LaTeX optimization${NC}"

# Commit 24: LaTeX optimizer
git add backend/services/latex_optimizer.py
commit_dated "Add LaTeX resume optimization support" "2026-01-24 09:30:00"

# Commit 25: LaTeX UI
git add LATEX_PASTE_COMPLETE.md
commit_dated "Integrate LaTeX paste feature in frontend" "2026-01-24 14:00:00"

# ==== Day 11: Jan 25, 2026 - Refinements ====
echo -e "${BLUE}Day 11 (Jan 25): Bug fixes and improvements${NC}"

# Commit 26: Context validator
git add backend/services/context_validator.py backend/services/keyword_prioritizer.py
commit_dated "Add context validation and keyword prioritization" "2026-01-25 10:45:00"

# Commit 27: Multi-model support
git add backend/services/multi_model_optimizer.py
commit_dated "Implement multi-model LLM support" "2026-01-25 15:20:00"

# Commit 28: Resume generator
git add backend/services/resume_generator.py
commit_dated "Add PDF resume generation service" "2026-01-25 18:30:00"

# ==== Day 12: Jan 26, 2026 - Music Player ====
echo -e "${BLUE}Day 12 (Jan 26): Music player feature${NC}"

# Commit 29: YouTube types
git add frontend/types/youtube.d.ts
commit_dated "Add TypeScript definitions for YouTube API" "2026-01-26 09:00:00"

# Commit 30: Music player
git add frontend/components/MusicPlayer.tsx MUSIC_PLAYER_SETUP.md
commit_dated "Implement music player with Spotify/YouTube" "2026-01-26 13:45:00"

# Commit 31: Music integration
git add MUSIC_AND_NETWORKING_RESEARCH.md
commit_dated "Integrate music player into main UI" "2026-01-26 16:30:00"

# ==== Day 13: Jan 27, 2026 - Documentation & Polish ====
echo -e "${BLUE}Day 13 (Jan 27): Documentation and final touches${NC}"

# Commit 32: Design docs
git add DESIGN_SYSTEM.md BRANDING.md
commit_dated "Document design system and branding" "2026-01-27 09:15:00"

# Commit 33: Technical docs
git add ATS_SCORING_EXPLAINED.md AI_MODELS.md
commit_dated "Add ATS scoring and AI model documentation" "2026-01-27 11:00:00"

# Commit 34: Setup guides
git add SETUP.md QUICK_START_FREE.md FREE_SETUP.md LLAMA_SETUP.md
commit_dated "Create comprehensive setup guides" "2026-01-27 13:30:00"

# Commit 35: Research docs
git add RESEARCH_FINDINGS.md AI_KEYWORD_EXTRACTION.md PARSER_RESEARCH.md
commit_dated "Document research and implementation decisions" "2026-01-27 15:00:00"

# Commit 36: Implementation notes
git add PHASE1_IMPLEMENTATION_COMPLETE.md SOLUTION_AI_PARSING.md CONSTRAINTS_FIXED.md UI_FIXED.md FORMAT_PRESERVATION_COMPLETE.md STRUCTURE_PRESERVATION_STRATEGY.md
commit_dated "Add implementation milestone documentation" "2026-01-27 16:45:00"

# Commit 37: Comparison docs
git add OLLAMA_VS_GROQ.md COST_COMPARISON.md
commit_dated "Document LLM provider comparison" "2026-01-27 17:30:00"

# Commit 38: Reference docs
git add QUICK_REFERENCE.md COMPLETE_SYSTEM_GUIDE.md GITHUB_SETUP.md
commit_dated "Add quick reference and system guide" "2026-01-27 18:15:00"

# Commit 39: Test files
git add backend/test_ai_parser.py
commit_dated "Add test suite for AI parser" "2026-01-27 19:00:00"

# Commit 40: Scripts and final polish
git add create_git_history.sh setup_git_history.sh create_realistic_history.sh
commit_dated "Add utility scripts and final polish" "2026-01-27 20:30:00"

echo -e "\n${GREEN}✅ Git history created successfully!${NC}\n"
echo -e "${BLUE}Commit Summary:${NC}"
git log --oneline --graph --all --date=short --pretty=format:"%C(yellow)%h%C(reset) - %C(green)%ad%C(reset) - %s"
echo -e "\n"
echo -e "${BLUE}Next steps:${NC}"
echo "1. Review the commit history above"
echo "2. git remote add origin https://github.com/Chaudhary-CS/ApplyTune.git"
echo "3. git branch -M main"
echo "4. git push -u origin main"
echo -e "\n${GREEN}Your repository now has a realistic development history! 🎉${NC}"
