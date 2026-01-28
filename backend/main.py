"""
ApplyTune Backend API
AI-powered resume optimizer for maximum ATS compatibility
"""

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional
import os
from dotenv import load_dotenv

# Import services
from services.resume_parser import ResumeParser
from services.ai_resume_parser import AIResumeParser
from services.job_analyzer import JobAnalyzer
from services.ats_scorer import ATSScorer
from services.resume_optimizer import ResumeOptimizer
from services.latex_optimizer import LaTeXOptimizer
from services.genuinity_analyzer import GenuinityAnalyzer

# Load environment variables
load_dotenv()

app = FastAPI(
    title="ApplyTune API",
    description="AI-Powered ATS Resume Optimization with Authenticity Scoring",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
resume_parser = ResumeParser()
ai_resume_parser = AIResumeParser()
job_analyzer = JobAnalyzer()
ats_scorer = ATSScorer()
resume_optimizer = ResumeOptimizer()
latex_optimizer = LaTeXOptimizer()
genuinity_analyzer = GenuinityAnalyzer()


@app.get("/")
def root():
    """Health check endpoint"""
    return {
        "message": "ApplyTune API is running",
        "version": "2.0.0",
        "features": [
            "ATS Optimization",
            "LaTeX Support",
            "Genuinity Scoring",
            "AI-Powered Parsing"
        ]
    }


@app.post("/api/optimize")
async def optimize_resume(
    file: Optional[UploadFile] = File(None),
    latex_code: Optional[str] = Form(None),
    job_description: str = Form(...),
    job_title: Optional[str] = Form("")
):
    """
    Optimize resume for ATS with genuinity validation.
    
    Supports:
    - PDF/DOCX files
    - LaTeX code (copy/paste)
    
    Returns:
    - ATS scores (before/after)
    - Optimized resume
    - Genuinity score
    - Detailed analysis
    """
    try:
        print(f"\n{'='*60}")
        print(f"🚀 NEW OPTIMIZATION REQUEST")
        print(f"{'='*60}")
        
        is_latex = latex_code is not None
        
        # ========== STEP 1: Parse Resume ==========
        if is_latex:
            print("\n📄 Processing LaTeX resume...")
            latex_content = latex_code.strip()
            parsed_resume = latex_optimizer.parse_latex_resume(latex_content)
            original_content = latex_content
            print(f"✓ LaTeX resume parsed")
        else:
            if not file:
                raise HTTPException(status_code=400, detail="No file or LaTeX code provided")
            
            print(f"\n📄 Processing uploaded file: {file.filename}")
            file_content = await file.read()
            file_extension = file.filename.split('.')[-1].lower()
            
            # Try AI-powered parsing first
            try:
                parsed_resume = ai_resume_parser.parse_resume(file_content, file_extension)
                print(f"✓ Resume parsed with AI")
            except Exception as e:
                print(f"⚠️ AI parsing failed, using traditional parser: {e}")
                parsed_resume = resume_parser.parse_resume(file_content, file_extension)
            
            original_content = parsed_resume.get('raw_text', '')
        
        # ========== STEP 2: Analyze Job Description ==========
        print(f"\n🎯 Analyzing job description...")
        job_analysis = job_analyzer.analyze(
            job_title=job_title or "Position",
            company_name="Company",
            description=job_description
        )
        print(f"✓ Extracted {len(job_analysis.get('keywords', []))} keywords")
        
        # ========== STEP 3: Calculate Original ATS Score ==========
        print(f"\n📊 Calculating original ATS score...")
        original_score = ats_scorer.calculate_score(parsed_resume, job_analysis)
        print(f"✓ Original ATS Score: {original_score:.1f}/100")
        
        # ========== STEP 4: Optimize Resume ==========
        print(f"\n🔧 Optimizing resume...")
        
        change_tracker = None  # Initialize for later use
        
        if is_latex:
            # LaTeX optimization with validation
            keyword_matches, missing_keywords = ats_scorer.get_keyword_matches(
                parsed_resume, job_analysis
            )
            
            print(f"   Missing {len(missing_keywords)} keywords from job description")
            
            # Optimize LaTeX with validation
            optimized_latex, added_keywords, changes_made, change_tracker = latex_optimizer.optimize_latex_resume(
                latex_content=latex_content,
                missing_keywords=missing_keywords[:20],  # Top 20 keywords
                job_description=job_description,
                job_title=job_title
            )
            
            # Re-parse optimized LaTeX
            optimized_resume = latex_optimizer.parse_latex_resume(optimized_latex)
            optimized_content = optimized_latex
            
            print(f"✓ LaTeX optimized: {len(added_keywords)} keywords added")
            print(f"✓ Change tracker: {change_tracker.to_dict()['total_changes']} total changes")
        
        else:
            # Traditional optimization (PDF/DOCX)
            optimized_resume = resume_optimizer.optimize_resume(
                parsed_resume, job_analysis
            )
            optimized_content = optimized_resume.get('raw_text', '')
            changes_made = []  # TODO: Track changes in traditional optimizer
            added_keywords = []
        
        # ========== STEP 5: Calculate New ATS Score ==========
        print(f"\n📈 Calculating optimized ATS score...")
        optimized_score = ats_scorer.calculate_score(optimized_resume, job_analysis)
        improvement = optimized_score - original_score
        print(f"✓ Optimized ATS Score: {optimized_score:.1f}/100 (+{improvement:.1f})")
        
        # ========== STEP 6: Analyze Genuinity ==========
        print(f"\n🔍 Analyzing resume authenticity...")
        
        genuinity_analysis = genuinity_analyzer.analyze_resume_authenticity(
            original_text=original_content,
            optimized_text=optimized_content,
            keywords_added=added_keywords if is_latex else [],
            changes_made=changes_made,
            resume_sections={'experience': optimized_content}  # Simplified
        )
        
        genuinity_score = genuinity_analysis['genuinity_score']
        risk_level = genuinity_analysis['risk_level']
        
        print(f"✓ Genuinity Score: {genuinity_score:.1f}/100 (Risk: {risk_level})")
        
        # Print detailed genuinity report
        if genuinity_score < 80:
            print(genuinity_analyzer.get_authenticity_report(genuinity_analysis))
        
        # ========== STEP 7: Calculate Multi-ATS Scores ==========
        print(f"\n📊 Calculating scores across ATS systems...")
        original_ats_scores = ats_scorer.calculate_multi_ats_scores(parsed_resume, job_analysis)
        optimized_ats_scores = ats_scorer.calculate_multi_ats_scores(optimized_resume, job_analysis)
        print(f"✓ Multi-ATS scores calculated")
        
        # ========== STEP 8: Prepare Response ==========
        keyword_matches_orig, missing_orig = ats_scorer.get_keyword_matches(
            parsed_resume, job_analysis
        )
        keyword_matches_opt, missing_opt = ats_scorer.get_keyword_matches(
            optimized_resume, job_analysis
        )
        
        response = {
            "success": True,
            "scores": {
                "original": {
                    "overall_score": original_score,
                    "ats_specific": original_ats_scores,
                    "breakdown": {}
                },
                "optimized": {
                    "overall_score": optimized_score,
                    "ats_specific": optimized_ats_scores,
                    "breakdown": {}
                },
                "improvement": improvement
            },
            "genuinity": {
                "score": genuinity_score,
                "risk_level": risk_level,
                "issues": genuinity_analysis.get('issues', []),
                "warnings": genuinity_analysis.get('warnings', []),
                "strengths": genuinity_analysis.get('strengths', []),
                "recommendations": genuinity_analysis.get('recommendations', [])
            },
            "keywords": {
                "matched_original": keyword_matches_orig,  # Already a list of strings
                "matched_optimized": keyword_matches_opt,  # Already a list of strings
                "missing_original": missing_orig,
                "missing_optimized": missing_opt,
                "added": added_keywords if is_latex else []
            },
            "optimized_resume": {
                "is_latex": is_latex,
                "content": optimized_content if is_latex else None,
                "format": "latex" if is_latex else "json",
                "data": optimized_resume if not is_latex else None
            },
            "change_preview": change_tracker.to_dict() if is_latex else None  # NEW: Real-time preview data!
        }
        
        print(f"\n{'='*60}")
        print(f"✅ OPTIMIZATION COMPLETE")
        print(f"   ATS Score: {original_score:.1f} → {optimized_score:.1f} (+{improvement:.1f})")
        print(f"   Genuinity: {genuinity_score:.1f}/100 ({risk_level} risk)")
        print(f"   Keywords Added: {len(added_keywords) if is_latex else 'N/A'}")
        print(f"{'='*60}\n")
        
        return JSONResponse(content=response)
    
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
def health_check():
    """Detailed health check with service status"""
    groq_api_key = os.getenv("GROQ_API_KEY", "")
    
    return {
        "status": "healthy",
        "services": {
            "groq_llm": "configured" if groq_api_key else "not_configured",
            "resume_parser": "ready",
            "ats_scorer": "ready",
            "latex_optimizer": "ready",
            "genuinity_analyzer": "ready"
        },
        "features": {
            "ai_optimization": bool(groq_api_key),
            "latex_support": True,
            "genuinity_scoring": True,
            "multi_ats_scoring": True
        }
    }


if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting ApplyTune API...")
    print("📍 API will be available at: http://localhost:8000")
    print("📚 Docs will be available at: http://localhost:8000/docs")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
