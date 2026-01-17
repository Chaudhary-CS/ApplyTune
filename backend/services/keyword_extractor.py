import re
from collections import Counter
from typing import List, Dict, Set
import string
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class KeywordExtractor:
    """
    Extract important keywords from job descriptions.
    This is crucial for ATS scoring - we need to catch what the ATS will look for.
    
    I'm using a combination of NLP techniques and some custom rules
    based on what I've learned about how ATS systems work.
    """
    
    def __init__(self):
        # Comprehensive stop words list - common words that ATS doesn't care about
        self.stop_words = {
            # Basic stop words
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
            'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'should', 'could', 'may', 'might', 'must', 'can', 'this', 'that',
            'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
            'what', 'which', 'who', 'when', 'where', 'why', 'how', 'all', 'each',
            'every', 'both', 'few', 'more', 'most', 'other', 'some', 'such',
            
            # Common non-technical words that were getting picked up
            'any', 'about', 'after', 'also', 'back', 'because', 'before', 'being',
            'between', 'during', 'even', 'first', 'get', 'give', 'her', 'here',
            'him', 'his', 'if', 'into', 'its', 'just', 'like', 'make', 'many',
            'me', 'my', 'new', 'no', 'not', 'now', 'off', 'only', 'our', 'out',
            'over', 'part', 'people', 'said', 'see', 'so', 'than', 'their', 'them',
            'then', 'there', 'think', 'too', 'two', 'up', 'us', 'use', 'very',
            'way', 'well', 'work', 'year', 'years',
            
            # Business jargon that's not technical (ATS doesn't care)
            'ability', 'accommodation', 'across', 'apply', 'business', 'candidate',
            'company', 'disability', 'diverse', 'employer', 'employment', 'equal',
            'essential', 'etc', 'experience', 'fast', 'flexible', 'good', 'great',
            'grow', 'growth', 'help', 'including', 'include', 'inclusive', 'individual',
            'information', 'interview', 'job', 'need', 'needs', 'opportunity', 'paid',
            'pay', 'person', 'plan', 'plans', 'please', 'point', 'position', 'preferred',
            'process', 'provide', 'qualified', 'quality', 'regardless', 'related',
            'required', 'requirements', 'role', 'status', 'strong', 'support', 'team',
            'time', 'using', 'various', 'veteran', 'via', 'within', 'without',
            
            # Time/date words
            'day', 'days', 'week', 'weeks', 'month', 'months', 'year', 'years',
            'hour', 'hours', 'minute', 'minutes', 'today', 'tomorrow', 'yesterday',
            
            # Numbers as words (not useful for ATS)
            'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten'
        }
        
        # Action verbs that employers love
        self.action_verbs = {
            'led', 'managed', 'developed', 'created', 'designed', 'implemented',
            'built', 'architected', 'optimized', 'improved', 'increased', 'decreased',
            'achieved', 'delivered', 'launched', 'spearheaded', 'coordinated',
            'executed', 'drove', 'established', 'generated', 'collaborated'
        }
        
        # Common job requirement indicators
        self.requirement_indicators = [
            'required', 'must have', 'essential', 'mandatory',
            'need', 'should have', 'preferred', 'desired'
        ]
    
    def extract_keywords(self, job_description: str, top_n: int = 50) -> Dict:
        """
        Main extraction method. Returns keywords categorized by importance.
        
        NEW ADAPTIVE APPROACH:
        - Uses AI to intelligently extract technical keywords
        - Adapts to ANY domain (ML, Finance, Healthcare, etc.)
        - No hardcoded dictionaries - context-aware!
        
        Returns:
            Dict with 'required', 'technical', 'soft_skills', 'nice_to_have'
        """
        # Clean the text first
        text = self._clean_text(job_description)
        
        # Try AI-powered extraction first (adaptive to any domain!)
        try:
            ai_extracted = self._ai_extract_keywords(job_description)
            if ai_extracted:
                return ai_extracted
        except Exception as e:
            print(f"AI extraction failed, falling back to rule-based: {e}")
        
        # Fallback: Rule-based extraction (if AI unavailable)
        required_keywords = self._extract_required_keywords(job_description)
        technical_skills = self._extract_technical_skills(text)
        soft_skills = self._extract_soft_skills(text)
        action_verbs_found = self._extract_action_verbs(text)
        important_words = self._extract_important_words(text, top_n)
        
        return {
            'required': list(required_keywords),
            'technical_skills': technical_skills,
            'soft_skills': soft_skills,
            'action_verbs': action_verbs_found,
            'important_words': important_words,
            'all_keywords': self._combine_keywords(
                required_keywords, technical_skills, soft_skills, important_words
            )
        }
    
    def _ai_extract_keywords(self, job_description: str) -> Dict:
        """
        AI-POWERED keyword extraction (adaptive to ANY domain!).
        
        Uses Groq/Llama to intelligently identify:
        - Technical skills (languages, frameworks, tools)
        - Required skills vs nice-to-have
        - Domain-specific terminology
        - Action verbs employers want
        
        Benefits:
        - NO hardcoded dictionaries
        - Adapts to new technologies automatically
        - Understands context (e.g., "Go" language vs "go" verb)
        - Works for ANY industry
        """
        from .llama_optimizer import LlamaOptimizer
        
        # Check if we have AI available
        llama = LlamaOptimizer()
        if not llama.is_available():
            return None
        
        prompt = f"""You are an ATS (Applicant Tracking System) keyword analyzer. Extract technical keywords from this job description that an ATS would scan for.

Job Description:
{job_description}

RULES:
1. Extract ONLY technical skills, tools, languages, frameworks, methodologies
2. IGNORE common English words (and, or, the, any, during, our, etc.)
3. IGNORE generic business words (business, process, team, need, etc.)
4. Include abbreviations (API, SQL, ML, AWS, etc.)
5. Include version numbers if mentioned (Python 3, Node 16, etc.)
6. Categorize as: REQUIRED (must-have), TECHNICAL (skills/tools), SOFT_SKILLS (leadership, etc.)

Output as JSON (no markdown, just raw JSON):
{{
  "required": ["skill1", "skill2"],
  "technical_skills": ["python", "kubernetes", "aws"],
  "soft_skills": ["leadership", "communication"],
  "action_verbs": ["developed", "managed", "built"]
}}

Extract now:"""

        try:
            system_prompt = "You are an ATS keyword extraction expert. Extract ONLY technical, job-relevant keywords. Ignore common English words and business jargon."
            
            response = llama.optimize_text(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=0.3,  # Lower temp for more consistent extraction
                max_tokens=1000
            )
            
            # Parse JSON response
            import json
            
            # Clean response (remove markdown if present)
            response = response.strip()
            if response.startswith('```'):
                # Extract JSON from markdown code block
                response = re.search(r'```(?:json)?\s*(\{.*\})\s*```', response, re.DOTALL)
                if response:
                    response = response.group(1)
            
            keywords = json.loads(response)
            
            # Add all_keywords field
            keywords['all_keywords'] = self._combine_keywords(
                keywords.get('required', []),
                keywords.get('technical_skills', []),
                keywords.get('soft_skills', [])
            )
            
            # Add important_words (for backward compatibility)
            keywords['important_words'] = keywords.get('technical_skills', [])[:20]
            
            print(f"✅ AI extracted {len(keywords['all_keywords'])} keywords")
            return keywords
            
        except Exception as e:
            print(f"AI keyword extraction error: {e}")
            return None
    
    def _clean_text(self, text: str) -> str:
        """Basic text cleaning"""
        # Convert to lowercase for processing
        text = text.lower()
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def _extract_required_keywords(self, text: str) -> Set[str]:
        """
        Find keywords that appear near requirement indicators.
        These are HIGH PRIORITY for ATS matching.
        """
        required = set()
        text_lower = text.lower()
        
        # Look for patterns like "required: python, java, aws"
        for indicator in self.requirement_indicators:
            # Find sentences containing requirement indicators
            pattern = f'{indicator}[^.]*?\\.'
            matches = re.finditer(pattern, text_lower, re.IGNORECASE)
            
            for match in matches:
                sentence = match.group(0)
                # Extract potential skills from this sentence
                words = self._tokenize(sentence)
                # Keep words that look like skills (2-20 chars, alphanumeric)
                for word in words:
                    if len(word) > 2 and word not in self.stop_words:
                        required.add(word)
        
        return required
    
    def _extract_technical_skills(self, text: str) -> List[str]:
        """
        Extract technical skills. I'm using a predefined list + pattern matching.
        TODO: maybe integrate with a skills API in the future?
        """
        skills = []
        
        # Comprehensive list of technical skills to look for
        tech_skills_db = [
            # Programming languages
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby',
            'go', 'golang', 'rust', 'php', 'swift', 'kotlin', 'scala', 'r',
            
            # Frontend
            'react', 'angular', 'vue', 'vue.js', 'react.js', 'next.js', 'svelte',
            'html', 'css', 'sass', 'scss', 'tailwind', 'bootstrap', 'jquery',
            'webpack', 'redux', 'mobx', 'html5', 'css3',
            
            # Backend
            'node.js', 'express', 'django', 'flask', 'fastapi', 'spring', 'spring boot',
            'asp.net', '.net', 'laravel', 'rails', 'ruby on rails',
            
            # Databases
            'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'cassandra',
            'dynamodb', 'oracle', 'sql server', 'mariadb', 'sqlite',
            'elasticsearch', 'neo4j',
            
            # Cloud & DevOps
            'aws', 'azure', 'gcp', 'google cloud', 'docker', 'kubernetes', 'k8s',
            'jenkins', 'gitlab ci', 'github actions', 'terraform', 'ansible',
            'ci/cd', 'devops', 'microservices', 'serverless', 'lambda',
            
            # Tools & Platforms
            'git', 'github', 'gitlab', 'bitbucket', 'jira', 'confluence',
            'slack', 'linux', 'unix', 'bash', 'shell scripting',
            
            # Data & ML
            'machine learning', 'deep learning', 'artificial intelligence', 'ai',
            'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'pandas', 'numpy',
            'data analysis', 'data science', 'big data', 'hadoop', 'spark',
            'tableau', 'power bi', 'excel',
            
            # Mobile
            'ios', 'android', 'react native', 'flutter', 'xamarin',
            
            # Methodologies
            'agile', 'scrum', 'kanban', 'waterfall', 'test-driven development',
            'tdd', 'bdd', 'rest', 'restful', 'api', 'graphql', 'soap',
            'object-oriented programming', 'oop', 'functional programming',
            
            # Testing
            'jest', 'mocha', 'pytest', 'junit', 'selenium', 'cypress',
            'unit testing', 'integration testing', 'e2e testing'
        ]
        
        for skill in tech_skills_db:
            # Look for the skill with word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text, re.IGNORECASE):
                skills.append(skill)
        
        return list(set(skills))  # remove dupes
    
    def _extract_soft_skills(self, text: str) -> List[str]:
        """Extract soft skills - also important for many positions"""
        soft_skills_db = [
            'leadership', 'communication', 'teamwork', 'problem solving',
            'critical thinking', 'analytical', 'creative', 'creativity',
            'time management', 'organization', 'organizational',
            'collaboration', 'interpersonal', 'adaptability', 'flexible',
            'attention to detail', 'self-motivated', 'initiative',
            'customer service', 'presentation', 'public speaking',
            'negotiation', 'conflict resolution', 'mentoring', 'coaching',
            'strategic thinking', 'decision making', 'emotional intelligence'
        ]
        
        found_skills = []
        
        for skill in soft_skills_db:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text, re.IGNORECASE):
                found_skills.append(skill)
        
        return found_skills
    
    def _extract_action_verbs(self, text: str) -> List[str]:
        """Find action verbs used in the job description"""
        found_verbs = []
        
        words = self._tokenize(text)
        
        for word in words:
            if word in self.action_verbs:
                found_verbs.append(word)
        
        return list(set(found_verbs))
    
    def _extract_important_words(self, text: str, top_n: int) -> List[str]:
        """
        Extract most frequent TECHNICAL words (frequency-based keyword extraction).
        This catches domain-specific technical terms we might not have in predefined lists.
        
        NOW FILTERS OUT: common English words, business jargon, non-technical terms.
        ONLY KEEPS: technical-sounding words, tools, technologies, frameworks.
        """
        words = self._tokenize(text)
        
        # Filter out stop words and keep only substantial words
        filtered_words = [
            w for w in words 
            if (w not in self.stop_words and 
                len(w) >= 3 and  # At least 3 characters
                not w.isdigit() and  # Not just numbers
                self._is_technical_word(w))  # Must look technical
        ]
        
        # Count frequency
        word_freq = Counter(filtered_words)
        
        # Get top N most common
        top_words = [word for word, count in word_freq.most_common(top_n)]
        
        return top_words
    
    def _is_technical_word(self, word: str) -> bool:
        """
        Check if a word is likely a technical term vs common English.
        
        Technical words typically:
        - Are abbreviations (API, GPU, CPU, AWS, SQL)
        - Contain numbers/versions (python3, node16, v2)
        - Are tech-specific (kubernetes, pytorch, tensorflow)
        - End in common tech suffixes (.js, .py, etc)
        
        NOT technical:
        - Common verbs (go, run, use, make, get)
        - Generic nouns (thing, person, time, way)
        - Generic adjectives (good, bad, fast, slow)
        """
        # Allow if it's an abbreviation or acronym (mostly uppercase or mix)
        if word.isupper() and len(word) <= 6:
            return True
        
        # Allow if it contains numbers (version numbers, etc)
        if any(char.isdigit() for char in word):
            return True
        
        # Allow if it contains special tech chars
        if any(char in word for char in ['.', '+', '#', '-']):
            return True
        
        # Check if it's in our technical skills databases
        # (this catches most real technical terms)
        tech_indicators = [
            'api', 'framework', 'database', 'cloud', 'script', 'dev', 'ops',
            'backend', 'frontend', 'full', 'stack', 'data', 'machine', 'deep',
            'learning', 'neural', 'model', 'algorithm', 'code', 'software',
            'hardware', 'system', 'server', 'client', 'engine', 'compiler',
            'runtime', 'container', 'orchestration', 'deployment', 'pipeline',
            'infrastructure', 'architecture', 'design', 'pattern', 'testing',
            'automation', 'optimization', 'performance', 'scalability', 'security',
            'authentication', 'authorization', 'encryption', 'protocol', 'network',
            'distributed', 'parallel', 'concurrent', 'asynchronous', 'real',
            'batch', 'stream', 'processing', 'analytics', 'visualization',
            'interface', 'integration', 'migration', 'monitoring', 'logging',
            'debugging', 'profiling', 'benchmark', 'metrics', 'telemetry',
            'sdk', 'cli', 'gui', 'ui', 'ux', 'web', 'mobile', 'native', 'hybrid'
        ]
        
        # If word contains any tech indicator, it's probably technical
        word_lower = word.lower()
        if any(indicator in word_lower for indicator in tech_indicators):
            return True
        
        # Blacklist of common non-technical words that might slip through
        non_technical_words = {
            'accommodation', 'across', 'apply', 'business', 'candidate',
            'company', 'during', 'employer', 'employment', 'equal', 'essential',
            'etc', 'fast', 'flexible', 'golang', 'good', 'great', 'grow', 'growth',
            'help', 'including', 'interview', 'job', 'need', 'needs', 'opportunity',
            'person', 'plan', 'plans', 'please', 'point', 'position', 'preferred',
            'process', 'provide', 'qualified', 'quality', 'regardless', 'required',
            'requirements', 'role', 'status', 'strong', 'support', 'team', 'using',
            'various', 'veteran', 'via', 'within', 'without'
        }
        
        if word_lower in non_technical_words:
            return False
        
        # If word is very short and all lowercase, probably not technical
        # (unless it's in our databases above)
        if len(word) < 4 and word.islower():
            # Common short words that aren't technical
            common_short = {'any', 'our', 'get', 'put', 'set', 'add', 'run', 'use'}
            if word in common_short:
                return False
        
        # Default: allow it if it passed all filters
        # (might be a domain-specific term we don't know about)
        return True
    
    def _tokenize(self, text: str) -> List[str]:
        """
        Simple tokenization - split on whitespace and punctuation.
        Not using fancy NLP libs to keep it fast and simple.
        """
        # Replace punctuation with spaces
        text = text.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation)))
        # Split and lowercase
        words = text.lower().split()
        return words
    
    def _combine_keywords(self, *keyword_lists) -> List[str]:
        """Combine all keyword lists into one unique list"""
        combined = set()
        
        for kw_list in keyword_lists:
            if isinstance(kw_list, (list, set)):
                combined.update(kw_list)
        
        return sorted(list(combined))
    
    def calculate_keyword_density(self, keywords: List[str], text: str) -> Dict[str, float]:
        """
        Calculate how often each keyword appears in text.
        Useful for knowing if we're keyword stuffing or not enough.
        """
        text_lower = text.lower()
        total_words = len(self._tokenize(text))
        
        density = {}
        
        for keyword in keywords:
            count = len(re.findall(r'\b' + re.escape(keyword.lower()) + r'\b', text_lower))
            density[keyword] = (count / total_words) * 100 if total_words > 0 else 0
        
        return density
