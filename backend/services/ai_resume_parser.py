"""
AI-Powered Resume Parser - Format-Agnostic!

THE BREAKTHROUGH: Instead of hardcoded patterns, let AI parse the resume!

Benefits:
- Works for ANY format (dates, bullets, sections, layouts)
- Self-adapting (handles edge cases automatically)  
- No maintenance (AI figures it out)
- Industry-standard approach (Jobscan, Affinda use this)

How it works:
1. Extract raw text from PDF
2. Ask AI to structure it into JSON
3. AI understands ANY format!
"""

from typing import Dict
import json
import re
from .llama_optimizer import LlamaOptimizer
import pdfplumber
import PyPDF2
import os


class AIResumeParser:
    """
    Revolutionary AI-powered resume parser.
    
    Works for ANY resume format - no hardcoded patterns!
    This is how Jobscan and professional tools do it.
    """
    
    def __init__(self):
        self.ai = LlamaOptimizer()
        
    def parse(self, file_path: str) -> Dict:
        """
        Parse resume using AI - works for ANY format!
        
        Returns structured data regardless of resume layout.
        """
        print(f"\n🤖 AI-Powered Parsing: {os.path.basename(file_path)}")
        
        # Step 1: Extract raw text
        raw_text = self._extract_text(file_path)
        
        if not raw_text or len(raw_text) < 100:
            raise Exception("Could not extract text from resume")
        
        print(f"✓ Extracted {len(raw_text)} characters")
        
        # Step 2: Let AI parse it!
        try:
            structured_data = self._ai_parse(raw_text)
            print(f"✓ AI parsed: {len(structured_data.get('experience', []))} experiences, {len(structured_data.get('skills', []))} skills")
            
            # Add metadata
            structured_data['raw_text'] = raw_text
            structured_data['file_name'] = os.path.basename(file_path)
            
            return structured_data
            
        except Exception as e:
            print(f"⚠️  AI parsing failed: {e}")
            print("   Falling back to basic extraction...")
            
            # Fallback: Basic extraction
            return self._fallback_parse(raw_text, file_path)
    
    def _extract_text(self, file_path: str) -> str:
        """Extract raw text from PDF/DOCX - same as before"""
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == '.pdf':
            return self._extract_pdf_text(file_path)
        elif file_ext in ['.docx', '.doc']:
            import docx
            doc = docx.Document(file_path)
            return "\n".join([p.text for p in doc.paragraphs])
        else:
            raise ValueError(f"Unsupported file type: {file_ext}")
    
    def _extract_pdf_text(self, file_path: str) -> str:
        """Extract text from PDF"""
        text = ""
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"pdfplumber failed: {e}, trying PyPDF2...")
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        
        return text.strip()
    
    def _ai_parse(self, raw_text: str) -> Dict:
        """
        THE MAGIC: Let AI parse the resume into structured JSON!
        
        This works for ANY format because AI understands context,
        not just patterns. It can handle:
        - Any date format (Month Year, MM/YYYY, etc.)
        - Any bullet style (•, -, *, or none)
        - Any section names (Experience vs Employment vs Work History)
        - Any layout (single column, two column, creative)
        
        This is the industry-standard approach!
        """
        prompt = f"""You are a professional resume parser. Extract structured information from this resume text.

Resume Text:
{raw_text[:4000]}  

Extract and return ONLY valid JSON (no markdown, no explanations) with this structure:
{{
  "contact_info": {{
    "name": "Full Name",
    "email": "email@example.com",
    "phone": "phone number",
    "location": "City, State",
    "linkedin": "linkedin url if present",
    "github": "github url if present"
  }},
  "summary": "professional summary or objective if present, otherwise empty string",
  "experience": [
    {{
      "title": "Job Title",
      "company": "Company Name",
      "location": "City, State",
      "dates": "Start Date - End Date",
      "description": [
        "bullet point 1",
        "bullet point 2"
      ]
    }}
  ],
  "education": [
    {{
      "degree": "Degree Name",
      "field": "Field of Study",
      "school": "School Name",
      "location": "City, State",
      "dates": "Start - End",
      "gpa": "GPA if mentioned"
    }}
  ],
  "skills": ["skill1", "skill2", "skill3"],
  "projects": [
    {{
      "name": "Project Name",
      "description": "Project description",
      "technologies": ["tech1", "tech2"]
    }}
  ],
  "certifications": ["cert1", "cert2"],
  "achievements": ["achievement1", "achievement2"]
}}

CRITICAL RULES:
1. Return ONLY the JSON object, no markdown, no explanations
2. Extract ALL work experiences with complete bullet points
3. Handle ANY date format (convert to readable format)
4. Extract ALL skills mentioned (technical and soft skills)
5. If a section is missing, return empty array/string
6. Be thorough - don't skip content!

Return the JSON now:"""

        system_prompt = "You are a precise resume parsing AI. Return only valid JSON with complete extracted data."
        
        try:
            response = self.ai.optimize_text(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=0.2,  # Low temp for consistent extraction
                max_tokens=2000
            )
            
            # Clean response (remove markdown if present)
            response = response.strip()
            if response.startswith('```'):
                # Extract JSON from markdown code block
                match = re.search(r'```(?:json)?\s*(\{.*\})\s*```', response, re.DOTALL)
                if match:
                    response = match.group(1)
            
            # Parse JSON
            data = json.loads(response)
            
            # Validate structure
            if not isinstance(data, dict):
                raise ValueError("AI returned non-dict")
            
            # Ensure required fields exist
            data.setdefault('contact_info', {})
            data.setdefault('summary', '')
            data.setdefault('experience', [])
            data.setdefault('education', [])
            data.setdefault('skills', [])
            data.setdefault('projects', [])
            data.setdefault('certifications', [])
            data.setdefault('achievements', [])
            
            return data
            
        except json.JSONDecodeError as e:
            raise Exception(f"AI returned invalid JSON: {e}\nResponse: {response[:200]}")
        except Exception as e:
            raise Exception(f"AI parsing error: {e}")
    
    def _fallback_parse(self, raw_text: str, file_path: str) -> Dict:
        """
        Fallback: Basic extraction if AI fails.
        Returns minimal structured data.
        """
        return {
            'contact_info': self._extract_contact_basic(raw_text),
            'summary': '',
            'experience': [],  # AI failed, no experience
            'education': [],
            'skills': self._extract_skills_basic(raw_text),
            'projects': [],
            'certifications': [],
            'achievements': [],
            'raw_text': raw_text,
            'file_name': os.path.basename(file_path),
            'parsing_method': 'fallback'
        }
    
    def _extract_contact_basic(self, text: str) -> Dict:
        """Basic contact extraction"""
        contact = {}
        
        # Email
        email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        if email_match:
            contact['email'] = email_match.group(0)
        
        # Phone  
        phone_match = re.search(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', text)
        if phone_match:
            contact['phone'] = phone_match.group(0)
        
        return contact
    
    def _extract_skills_basic(self, text: str) -> list:
        """Basic skill extraction"""
        common_skills = [
            'python', 'java', 'javascript', 'react', 'node', 'sql', 'aws',
            'docker', 'kubernetes', 'git', 'typescript', 'c++', 'golang'
        ]
        
        text_lower = text.lower()
        found_skills = []
        
        for skill in common_skills:
            if skill in text_lower:
                found_skills.append(skill.title())
        
        return found_skills


# Convenience function
def parse_resume_with_ai(file_path: str) -> Dict:
    """
    Parse any resume with AI - one function call!
    
    Usage:
        data = parse_resume_with_ai('resume.pdf')
    """
    parser = AIResumeParser()
    return parser.parse(file_path)
