from typing import Dict, List
import os
from openai import OpenAI
import json
import re
from .format_preserver import FormatPreserver
from .llama_optimizer import LlamaOptimizer

class ResumeOptimizer:
    """
    The magic happens here! This uses AI to rewrite resume content
    to better match job descriptions while keeping everything truthful.
    
    I'm using OpenAI's GPT-4 for this. It's really good at:
    - Understanding context
    - Rewriting text naturally
    - Incorporating keywords without being obvious
    
    The key is giving it the right prompts so it optimizes
    without making stuff up or keyword stuffing.
    """
    
    def __init__(self):
        # Applytune is 100% FREE - we use Ollama by default!
        # No API keys needed, no costs, complete privacy
        
        ai_provider = os.getenv('AI_PROVIDER', 'llama')  # Default to FREE Llama!
        
        self.provider = ai_provider
        self.client = None
        self.llama_optimizer = None
        
        if ai_provider == 'llama':
            # Use FREE Llama models (via Ollama or Groq)
            print("🦙 Using 100% FREE Llama models")
            self.llama_optimizer = LlamaOptimizer()
            self.model = 'llama'
            
            # Check if Ollama is available
            if self.llama_optimizer.provider == 'ollama':
                if self.llama_optimizer.is_available():
                    print(f"✓ Ollama running with model: {self.llama_optimizer.ollama_model}")
                else:
                    print("⚠️  Ollama not running!")
                    print("   Install: brew install ollama")
                    print("   Then run: ollama pull llama3.1:70b")
            
        else:
            # OpenAI fallback (if someone really wants to pay)
            api_key = os.getenv('OPENAI_API_KEY')
            if api_key and api_key != 'your_openai_api_key_here':
                self.client = OpenAI(api_key=api_key)
                self.model = os.getenv('AI_MODEL', 'gpt-4o')
                print(f"🤖 Using paid model: {self.model}")
            else:
                # Auto-fallback to FREE Llama
                print("⚠️  OpenAI selected but no API key. Switching to FREE Llama!")
                self.provider = 'llama'
                self.llama_optimizer = LlamaOptimizer()
                self.model = 'llama'
        
        # Initialize format preserver to maintain user's style
        self.format_preserver = FormatPreserver()
    
    def optimize(self, resume_data: Dict, job_analysis: Dict, 
                 job_title: str, company_name: str) -> Dict:
        """
        Main optimization function. Takes resume and job analysis,
        returns ATS-enhanced resume while preserving user's style.
        
        Philosophy: We enhance, not rewrite. The resume should still
        feel like THEIR resume, just optimized for the job.
        """
        # Check if we have any AI available
        if not self.client and not self.llama_optimizer:
            return {
                **resume_data,
                'optimized': False,
                'suggestions': ['No AI provider configured - AI optimization unavailable']
            }
        
        # If using Llama, check if it's available
        if self.provider == 'llama' and not self.llama_optimizer.is_available():
            return {
                **resume_data,
                'optimized': False,
                'suggestions': [
                    'Llama not available. Install Ollama from: https://ollama.ai',
                    'Or get free Groq API key from: https://console.groq.com',
                    'Or add OpenAI API key to use GPT models'
                ]
            }
        
        # Get keywords we need to target
        target_keywords = self._get_target_keywords(job_analysis)
        
        # Create a copy to preserve original
        optimized_resume = resume_data.copy()
        suggestions = []
        
        # Optimize professional summary if exists (preserve style!)
        if resume_data.get('summary'):
            optimized_resume['summary'] = self._optimize_summary(
                resume_data['summary'], job_title, target_keywords
            )
            suggestions.append("Enhanced summary with relevant keywords while preserving your style")
        else:
            # Create a new summary based on their actual background
            generated_summary = self._generate_summary(
                resume_data, job_title, target_keywords
            )
            if generated_summary:
                optimized_resume['summary'] = generated_summary
                suggestions.append("Added professional summary based on your experience")
        
        # Optimize experience bullets - preserve their format!
        if resume_data.get('experience'):
            optimized_resume['experience'] = self._optimize_experience(
                resume_data['experience'], job_analysis, target_keywords
            )
            suggestions.append("Enhanced bullet points with job-relevant keywords")
        
        # Reorder skills to prioritize job-relevant ones
        optimized_resume['skills'] = self._optimize_skills(
            resume_data.get('skills', []), job_analysis
        )
        suggestions.append("Reordered skills to highlight job-relevant expertise")
        
        # Add metadata
        optimized_resume['optimized'] = True
        optimized_resume['optimized_for'] = {
            'job_title': job_title,
            'company': company_name
        }
        optimized_resume['suggestions'] = suggestions
        optimized_resume['target_keywords_used'] = target_keywords[:20]  # Top 20
        
        return optimized_resume
    
    def _get_target_keywords(self, job_analysis: Dict) -> List[str]:
        """
        Extract the most important keywords to target.
        Prioritize required skills and technical skills.
        """
        keywords = []
        job_keywords = job_analysis.get('keywords', {})
        
        # Priority 1: Required keywords
        keywords.extend(job_keywords.get('required', []))
        
        # Priority 2: Technical skills
        keywords.extend(job_keywords.get('technical_skills', []))
        
        # Priority 3: Soft skills
        keywords.extend(job_keywords.get('soft_skills', []))
        
        # Priority 4: Important words (top 15)
        keywords.extend(job_keywords.get('important_words', [])[:15])
        
        # Remove duplicates, keep order
        seen = set()
        unique_keywords = []
        for kw in keywords:
            kw_lower = kw.lower()
            if kw_lower not in seen:
                seen.add(kw_lower)
                unique_keywords.append(kw)
        
        return unique_keywords
    
    def _optimize_summary(self, original_summary: str, job_title: str, 
                         keywords: List[str]) -> str:
        """
        Enhance professional summary by adding relevant keywords while
        preserving the user's voice and style.
        """
        # Check if we have any AI available (OpenAI OR Llama)
        if not self.client and not self.llama_optimizer:
            return original_summary
        
        # Build prompt for GPT-4
        prompt = f"""You are an expert resume optimizer. Enhance this professional summary for a {job_title} position while preserving the user's voice.

Original summary:
{original_summary}

Relevant keywords to incorporate naturally:
{', '.join(keywords[:12])}

RULES:
- PRESERVE the user's writing style and tone
- PRESERVE the approximate length (don't make it significantly longer/shorter)
- Keep all facts accurate
- Only add keywords that genuinely fit
- Make minimal changes - just strategic enhancements
- Don't rewrite their personality away
- If it's already strong, only add missing keywords

Return the enhanced summary, maintaining their voice."""

        try:
            # Use Llama if that's our provider
            if self.provider == 'llama':
                system_prompt = "You are a professional resume writer who creates ATS-optimized content while preserving the user's authentic voice and style."
                optimized = self.llama_optimizer.optimize_text(
                    prompt=prompt,
                    system_prompt=system_prompt,
                    temperature=0.5,
                    max_tokens=400
                )
                return optimized if optimized else original_summary
            
            # Otherwise use OpenAI
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional resume writer who creates ATS-optimized content while preserving the user's authentic voice and style."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=400,
                top_p=0.9
            )
            
            optimized = response.choices[0].message.content.strip()
            return optimized if optimized else original_summary
            
        except Exception as e:
            print(f"Error optimizing summary: {e}")
            return original_summary
    
    def _generate_summary(self, resume_data: Dict, job_title: str, 
                         keywords: List[str]) -> str:
        """
        Generate a professional summary if resume doesn't have one.
        Based on their actual experience - keeping it authentic.
        """
        # Check if we have any AI available (OpenAI OR Llama)
        if not self.client and not self.llama_optimizer:
            return ""
        
        # Extract key info from resume
        skills = ', '.join(resume_data.get('skills', [])[:10])
        experience_count = len(resume_data.get('experience', []))
        
        # Get their first job title to understand their level
        first_job = ""
        if resume_data.get('experience'):
            first_job = resume_data['experience'][0].get('title', '')
        
        prompt = f"""Create a professional summary for a {job_title} resume based on this candidate's background.

Their background:
- Current/recent role: {first_job}
- Key skills: {skills}
- Experience level: ~{experience_count * 2} years
- Target role keywords: {', '.join(keywords[:10])}

Write a 2-3 sentence summary that:
- Reflects their actual background
- Naturally includes relevant keywords
- Sounds professional but authentic
- Is optimized for ATS

Keep it concise and genuine. Return only the summary."""

        try:
            # Use Llama if that's our provider
            if self.provider == 'llama':
                system_prompt = "You are a professional resume writer who creates authentic, ATS-optimized content."
                return self.llama_optimizer.optimize_text(
                    prompt=prompt,
                    system_prompt=system_prompt,
                    temperature=0.5,
                    max_tokens=300
                )
            
            # Otherwise use OpenAI
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional resume writer who creates authentic, ATS-optimized content."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=300,
                top_p=0.9
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating summary: {e}")
            return ""
    
    def _optimize_experience(self, experience_list: List[Dict], 
                            job_analysis: Dict, keywords: List[str]) -> List[Dict]:
        """
        Optimize experience bullet points. This is where most of the
        ATS optimization happens - rewriting bullets to include keywords
        while keeping them truthful and impactful.
        """
        # Check if we have any AI available (OpenAI OR Llama)
        if not self.client and not self.llama_optimizer:
            return experience_list
        
        optimized_exp = []
        
        for exp in experience_list:
            optimized_entry = exp.copy()
            
            # Only optimize if there are descriptions
            if exp.get('description') and len(exp['description']) > 0:
                original_bullets = exp['description']
                
                # Optimize the bullets
                optimized_bullets = self._optimize_bullets(
                    original_bullets, keywords, job_analysis
                )
                
                optimized_entry['description'] = optimized_bullets
            
            optimized_exp.append(optimized_entry)
        
        return optimized_exp
    
    def _optimize_bullets(self, bullets: List[str], keywords: List[str], 
                         job_analysis: Dict) -> List[str]:
        """
        Enhance bullet points by adding relevant keywords while preserving
        the user's original style, format, and length.
        
        We're NOT rewriting their resume - just making it more ATS-friendly
        by strategically incorporating job keywords where they naturally fit.
        """
        # Check if we have any AI available (OpenAI OR Llama)
        if (not self.client and not self.llama_optimizer) or not bullets:
            return bullets
        
        # Prepare bullets for optimization
        bullets_text = '\n'.join([f"- {b}" for b in bullets])
        
        action_verbs = job_analysis.get('keywords', {}).get('action_verbs', [])
        
        prompt = f"""You are an expert resume optimizer. Your job is to ENHANCE these bullet points for ATS compatibility while preserving the user's original style and format.

Original bullets:
{bullets_text}

Target keywords to add: {', '.join(keywords[:12])}
Preferred action verbs: {', '.join(action_verbs[:8])}

CRITICAL RULES:
1. PRESERVE the user's formatting - if they have one-line bullets, keep them one line
2. PRESERVE their writing style and tone
3. PRESERVE the number of bullets (don't add or remove bullets)
4. ONLY add relevant keywords that genuinely fit the context
5. Keep their original structure - just enhance with keywords
6. If a bullet is already good, keep it mostly the same
7. Don't change bullet length significantly
8. Don't fabricate accomplishments - only enhance what's there
9. Maintain their personal voice

Your task: Subtly integrate relevant keywords into their existing bullets WITHOUT changing the overall format or feel.

Return the enhanced bullets in the same format:
- Enhanced bullet one
- Enhanced bullet two
etc."""

        try:
            # Use Llama if that's our provider
            if self.provider == 'llama':
                system_prompt = "You are a professional resume writer specializing in ATS optimization while preserving authentic voice."
                optimized_text = self.llama_optimizer.optimize_text(
                    prompt=prompt,
                    system_prompt=system_prompt,
                    temperature=0.5,
                    max_tokens=600
                )
            else:
                # Use OpenAI
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a professional resume writer specializing in ATS optimization while preserving authentic voice."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.5,
                    max_tokens=600,
                    top_p=0.9
                )
                optimized_text = response.choices[0].message.content.strip()
            
            # Parse bullets from response
            optimized_bullets = []
            for line in optimized_text.split('\n'):
                line = line.strip()
                if line.startswith(('- ', '• ', '* ')):
                    bullet = line[2:].strip()
                    if bullet:
                        optimized_bullets.append(bullet)
            
            # Return optimized bullets if we got good results, otherwise original
            return optimized_bullets if len(optimized_bullets) >= 2 else bullets
            
        except Exception as e:
            print(f"Error optimizing bullets: {e}")
            return bullets
    
    def _optimize_skills(self, current_skills: List[str], 
                        job_analysis: Dict) -> List[str]:
        """
        Reorder and enhance skills section to prioritize job-relevant skills.
        Put the most relevant skills first - that's what ATS looks at!
        """
        job_keywords = job_analysis.get('keywords', {})
        job_tech_skills = set(s.lower() for s in job_keywords.get('technical_skills', []))
        job_soft_skills = set(s.lower() for s in job_keywords.get('soft_skills', []))
        
        # Categorize existing skills
        matched_skills = []
        other_skills = []
        
        for skill in current_skills:
            skill_lower = skill.lower()
            if skill_lower in job_tech_skills or skill_lower in job_soft_skills:
                matched_skills.append(skill)
            else:
                other_skills.append(skill)
        
        # Add job skills that aren't in resume yet (if relevant)
        # Only add skills that might be implied by their experience
        skills_to_consider = list(job_tech_skills)[:10]  # Top 10 job skills
        
        for skill in skills_to_consider:
            # Check if skill is already listed (case-insensitive)
            if not any(skill.lower() == s.lower() for s in current_skills):
                # TODO: In a real version, we'd check if they actually have this skill
                # For now, we'll suggest it but not add automatically
                pass
        
        # Combine: matched skills first, then others
        optimized_skills = matched_skills + other_skills
        
        return optimized_skills
    
    def get_optimization_suggestions(self, resume_data: Dict, 
                                    job_analysis: Dict) -> List[str]:
        """
        Generate specific suggestions for manual improvements.
        Even with AI optimization, some things are better done by the user.
        """
        suggestions = []
        
        job_keywords = job_analysis.get('keywords', {})
        resume_text = resume_data.get('raw_text', '').lower()
        
        # Check for missing required keywords
        required_keywords = job_keywords.get('required', [])
        missing_required = [kw for kw in required_keywords 
                           if kw.lower() not in resume_text]
        
        if missing_required:
            suggestions.append(
                f"Consider adding these required skills if you have them: {', '.join(missing_required[:5])}"
            )
        
        # Check for action verbs
        action_verbs = job_keywords.get('action_verbs', [])
        if action_verbs and resume_data.get('experience'):
            suggestions.append(
                f"Use strong action verbs like: {', '.join(action_verbs[:5])}"
            )
        
        # Check for quantifiable achievements
        has_numbers = bool(re.search(r'\d+%|\d+x|\$\d+', resume_text))
        if not has_numbers:
            suggestions.append(
                "Add quantifiable achievements (e.g., 'Increased sales by 30%', 'Led team of 5')"
            )
        
        # Check for education requirements
        education_req = job_analysis.get('education', {})
        if education_req.get('degree_required') and not resume_data.get('education'):
            suggestions.append(
                "Job requires a degree - make sure education section is visible"
            )
        
        # Generic suggestions
        suggestions.append("Tailor your resume file name (e.g., 'YourName_SoftwareEngineer.pdf')")
        suggestions.append("Keep resume to 1-2 pages for optimal ATS parsing")
        
        return suggestions[:8]  # Return top 8 suggestions
