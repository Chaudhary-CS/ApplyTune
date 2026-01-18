from typing import Dict, List
import re
from .keyword_extractor import KeywordExtractor

class JobAnalyzer:
    """
    Analyze job descriptions to understand what the employer wants.
    This feeds into our ATS scoring and resume optimization.
    
    I'm trying to extract everything an ATS system would care about:
    - Keywords and skills
    - Experience level
    - Education requirements
    - Must-haves vs nice-to-haves
    """
    
    def __init__(self):
        self.keyword_extractor = KeywordExtractor()
        
        # Experience level indicators
        self.experience_patterns = {
            'entry': r'\b(entry.?level|junior|0-2 years|recent grad|graduate)\b',
            'mid': r'\b(mid.?level|intermediate|2-5 years|3-7 years)\b',
            'senior': r'\b(senior|sr\.|5\+ years|7\+ years|expert|lead)\b',
            'principal': r'\b(principal|staff|architect|10\+ years)\b'
        }
        
        # Common job categories - helps contextualize requirements
        self.job_categories = {
            'engineering': ['engineer', 'developer', 'programmer', 'software'],
            'data': ['data scientist', 'analyst', 'data engineer', 'ml engineer'],
            'product': ['product manager', 'product owner', 'pm'],
            'design': ['designer', 'ux', 'ui', 'user experience'],
            'marketing': ['marketing', 'growth', 'seo', 'content'],
            'sales': ['sales', 'account executive', 'business development']
        }
    
    def analyze(self, job_title: str, company_name: str, description: str) -> Dict:
        """
        Main analysis function. Returns comprehensive job analysis.
        
        This is what we use to score resumes against.
        """
        # Extract keywords first - this is the foundation
        keywords = self.keyword_extractor.extract_keywords(description)
        
        # Determine experience level
        experience_level = self._detect_experience_level(job_title, description)
        
        # Figure out job category
        category = self._categorize_job(job_title)
        
        # Extract specific requirements
        requirements = self._extract_requirements(description)
        
        # Find education requirements
        education = self._extract_education_requirements(description)
        
        # Extract company culture indicators (nice bonus for resume tailoring)
        culture_keywords = self._extract_culture_keywords(description)
        
        return {
            'job_title': job_title,
            'company_name': company_name,
            'category': category,
            'experience_level': experience_level,
            'keywords': keywords,
            'requirements': requirements,
            'education': education,
            'culture_keywords': culture_keywords,
            'word_count': len(description.split()),
            'summary': self._generate_summary(job_title, category, experience_level, keywords)
        }
    
    def _detect_experience_level(self, job_title: str, description: str) -> str:
        """
        Figure out if this is entry, mid, senior, etc.
        Helps us tailor the resume appropriately.
        """
        combined_text = f"{job_title} {description}".lower()
        
        # Check patterns in order of seniority (highest first)
        for level, pattern in sorted(self.experience_patterns.items(), 
                                     key=lambda x: ['entry', 'mid', 'senior', 'principal'].index(x[0]), 
                                     reverse=True):
            if re.search(pattern, combined_text, re.IGNORECASE):
                return level
        
        # Default to mid if we can't tell
        return 'mid'
    
    def _categorize_job(self, job_title: str) -> str:
        """What type of job is this?"""
        title_lower = job_title.lower()
        
        for category, keywords in self.job_categories.items():
            if any(keyword in title_lower for keyword in keywords):
                return category
        
        return 'general'
    
    def _extract_requirements(self, description: str) -> Dict[str, List[str]]:
        """
        Separate required vs preferred requirements.
        ATS systems weight required skills more heavily.
        """
        requirements = {
            'required': [],
            'preferred': [],
            'responsibilities': []
        }
        
        # Split into sentences
        sentences = re.split(r'[.!?\n]', description)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            s_lower = sentence.lower()
            
            # Check if it's a requirement
            if any(word in s_lower for word in ['required', 'must have', 'must be', 'need to have']):
                requirements['required'].append(sentence)
            
            # Check if it's preferred
            elif any(word in s_lower for word in ['preferred', 'nice to have', 'bonus', 'plus']):
                requirements['preferred'].append(sentence)
            
            # Check if it's a responsibility
            elif any(word in s_lower for word in ['will', 'responsible for', 'you will', 'responsibilities']):
                requirements['responsibilities'].append(sentence)
        
        return requirements
    
    def _extract_education_requirements(self, description: str) -> Dict:
        """
        Find education requirements. Some jobs are strict about this,
        others just put it as a formality.
        """
        education = {
            'degree_required': False,
            'degree_level': None,
            'field_of_study': [],
            'can_substitute_experience': False
        }
        
        desc_lower = description.lower()
        
        # Check for degree requirements
        degree_patterns = {
            'bachelors': r"\b(bachelor'?s?|b\.s\.|b\.a\.|undergraduate degree)\b",
            'masters': r"\b(master'?s?|m\.s\.|m\.a\.|graduate degree)\b",
            'phd': r"\b(ph\.?d\.?|doctorate|doctoral)\b"
        }
        
        for level, pattern in degree_patterns.items():
            if re.search(pattern, desc_lower):
                education['degree_required'] = True
                education['degree_level'] = level
                break
        
        # Check if experience can substitute
        if re.search(r'(equivalent experience|or equivalent|in lieu of)', desc_lower):
            education['can_substitute_experience'] = True
        
        # Try to find field of study
        field_keywords = ['computer science', 'engineering', 'business', 'mathematics', 
                         'statistics', 'related field']
        
        for field in field_keywords:
            if field in desc_lower:
                education['field_of_study'].append(field)
        
        return education
    
    def _extract_culture_keywords(self, description: str) -> List[str]:
        """
        Find culture/company value keywords. These can be good to mention
        in a resume/cover letter for extra points.
        
        Not all ATS systems check for this, but some do!
        """
        culture_terms = [
            'fast-paced', 'innovative', 'collaborative', 'team player',
            'startup', 'dynamic', 'flexible', 'remote', 'hybrid',
            'work-life balance', 'diversity', 'inclusive', 'mission-driven',
            'customer-focused', 'data-driven', 'results-oriented',
            'entrepreneurial', 'self-starter', 'ownership'
        ]
        
        found_terms = []
        desc_lower = description.lower()
        
        for term in culture_terms:
            if term in desc_lower:
                found_terms.append(term)
        
        return found_terms
    
    def _generate_summary(self, job_title: str, category: str, 
                         experience_level: str, keywords: Dict) -> str:
        """
        Generate a human-readable summary of the job analysis.
        Useful for showing users what we detected.
        """
        tech_skills_count = len(keywords.get('technical_skills', []))
        required_count = len(keywords.get('required', []))
        
        summary = f"This is a {experience_level}-level {category} position "
        summary += f"({job_title}). "
        summary += f"Found {tech_skills_count} technical skills and "
        summary += f"{required_count} required keywords. "
        
        # Add advice based on what we found
        if experience_level == 'senior':
            summary += "Focus on leadership and impact in your resume."
        elif experience_level == 'entry':
            summary += "Emphasize relevant projects and eagerness to learn."
        
        return summary
