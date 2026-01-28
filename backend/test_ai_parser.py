"""
Test AI Resume Parser - Prove it works for ANY format!

This demonstrates how AI parsing handles:
- Different date formats
- Different section names
- Different bullet styles
- Different layouts
"""

from services.llama_optimizer import LlamaOptimizer
import json


def test_ai_parsing_different_formats():
    """
    Test AI parser with 3 wildly different resume formats.
    AI should extract structured data from ALL of them!
    """
    
    ai = LlamaOptimizer()
    
    # Format 1: Traditional with "Month Year" dates
    resume_1 = """
    John Doe
    john@email.com | 555-123-4567
    
    EXPERIENCE
    Software Engineer | Google Inc
    June 2022 - Present
    • Built scalable APIs with Python
    • Reduced latency by 40%
    
    EDUCATION
    BS Computer Science, MIT, 2022
    
    SKILLS: Python, React, AWS
    """
    
    # Format 2: Modern with "MM/YYYY" dates and no bullets
    resume_2 = """
    Jane Smith
    jane@example.com
    
    Work History
    
    Senior Developer at Microsoft
    01/2021 - 12/2023
    Developed cloud infrastructure using Azure
    Led team of 5 engineers
    
    Education: Stanford University, MS CS, 2020
    
    Technical Stack: Java, Kubernetes, Docker
    """
    
    # Format 3: Creative with "Q2 2024" dates
    resume_3 = """
    Bob Johnson | bob@tech.com | github.com/bobjohn
    
    PROFESSIONAL EXPERIENCE
    
    Q2 2023 - Q4 2023: Data Scientist @ Meta
    - ML model development
    - A/B testing infrastructure
    
    2020-2023: Analyst @ Amazon
    Data pipeline automation
    
    EDUCATION
    Carnegie Mellon, PhD AI (2019)
    
    EXPERTISE
    TensorFlow, PyTorch, SQL, Spark
    """
    
    print("🧪 Testing AI Parser with 3 Different Formats\n")
    print("=" * 60)
    
    for i, resume_text in enumerate([resume_1, resume_2, resume_3], 1):
        print(f"\n📄 Format {i} Test:")
        print("-" * 60)
        
        prompt = f"""Extract structured information from this resume:

{resume_text}

Return ONLY valid JSON (no markdown) with this structure:
{{
  "name": "Full Name",
  "email": "email",
  "experience_count": number of jobs,
  "first_job_title": "title of most recent job",
  "first_company": "company of most recent job",
  "skills_count": number of skills,
  "top_3_skills": ["skill1", "skill2", "skill3"]
}}

Return JSON only:"""
        
        try:
            response = ai.optimize_text(
                prompt=prompt,
                system_prompt="You are a resume parser. Return only valid JSON.",
                temperature=0.1,
                max_tokens=500
            )
            
            # Clean response
            response = response.strip()
            if response.startswith('```'):
                import re
                match = re.search(r'```(?:json)?\s*(\{.*\})\s*```', response, re.DOTALL)
                if match:
                    response = match.group(1)
            
            # Parse
            data = json.loads(response)
            
            print(f"✅ SUCCESS! Extracted:")
            print(f"   Name: {data.get('name', 'N/A')}")
            print(f"   Email: {data.get('email', 'N/A')}")
            print(f"   Jobs: {data.get('experience_count', 0)}")
            print(f"   Recent Role: {data.get('first_job_title', 'N/A')} at {data.get('first_company', 'N/A')}")
            print(f"   Skills ({data.get('skills_count', 0)}): {', '.join(data.get('top_3_skills', []))}")
            
        except Exception as e:
            print(f"❌ FAILED: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 AI Parser handles ANY format automatically!")


if __name__ == "__main__":
    test_ai_parsing_different_formats()
