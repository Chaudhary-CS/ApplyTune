"""
Context-Aware Validator - Know what's SAFE vs FAKE to change

Based on research: Projects tech stacks are VERIFIABLE (GitHub) = Don't change!
Experience descriptions are NOT verifiable = Safe to enhance
"""

from typing import List, Dict
import re


class ContextValidator:
    """
    Validates if adding a keyword is realistic or fabrication.
    
    Key Principle: Enhancement is OK, Fabrication is NOT.
    
    SAFE: "Built REST APIs" → "Built scalable REST APIs using Node.js"
    FAKE: "Built REST APIs" → "Built ML models using PyTorch"
    """
    
    # Technology families - adjacent techs are SAFE to add
    TECH_FAMILIES = {
        'python': {
            'ecosystem': ['pandas', 'numpy', 'flask', 'django', 'fastapi', 'pytest', 'python'],
            'adjacent_ml': ['pytorch', 'tensorflow', 'scikit-learn', 'machine learning', 'ml'],
            'adjacent_data': ['data analysis', 'data science', 'jupyter']
        },
        'javascript': {
            'ecosystem': ['react', 'node.js', 'typescript', 'vue', 'angular', 'next.js', 'express'],
            'adjacent_frontend': ['html', 'css', 'ui/ux', 'responsive design'],
            'adjacent_backend': ['rest api', 'graphql', 'websockets']
        },
        'java': {
            'ecosystem': ['spring', 'spring boot', 'maven', 'gradle', 'junit'],
            'adjacent_backend': ['rest api', 'microservices', 'jpa', 'hibernate']
        },
        'containerization': {
            'ecosystem': ['docker', 'kubernetes', 'podman', 'container orchestration', 'helm'],
            'adjacent_devops': ['ci/cd', 'jenkins', 'gitlab ci', 'github actions']
        },
        'cloud': {
            'ecosystem': ['aws', 'azure', 'gcp', 'cloud computing', 'serverless'],
            'adjacent_devops': ['terraform', 'cloudformation', 'infrastructure as code']
        },
        'databases': {
            'sql': ['postgresql', 'mysql', 'sql', 'database design'],
            'nosql': ['mongodb', 'redis', 'dynamodb', 'nosql'],
            'orm': ['sequelize', 'mongoose', 'sqlalchemy']
        },
        'ml_ai': {
            'frameworks': ['pytorch', 'tensorflow', 'scikit-learn', 'keras'],
            'concepts': ['machine learning', 'deep learning', 'neural networks', 'ml'],
            'tools': ['jupyter', 'pandas', 'numpy', 'matplotlib']
        }
    }
    
    # Risk levels for different resume sections
    SECTION_RISK = {
        'projects': 'HIGH',           # GitHub is public - easily verified
        'experience': 'LOW',          # Day-to-day tasks hard to verify  
        'skills': 'VERY_LOW',         # Just listing capabilities
        'certifications': 'EXTREME',  # Certificates are checked
        'education': 'EXTREME'        # Transcripts exist
    }
    
    def can_add_keyword(
        self, 
        keyword: str, 
        section: str, 
        existing_content: str
    ) -> Dict:
        """
        Determine if adding this keyword is SAFE or RISKY.
        
        Returns:
            {
                'allowed': bool,
                'risk_level': 'SAFE' | 'QUESTIONABLE' | 'FABRICATION',
                'reason': str,
                'suggestion': str (alternative approach)
            }
        """
        keyword_lower = keyword.lower()
        content_lower = existing_content.lower()
        
        # Check section risk level
        section_risk = self._get_section_risk(section)
        
        if section_risk == 'EXTREME':
            return {
                'allowed': False,
                'risk_level': 'EXTREME_RISK',
                'reason': f"{section} section is easily verified. DO NOT fabricate.",
                'suggestion': f"Don't add {keyword} to {section} unless you actually have it."
            }
        
        # For high-risk sections (Projects), check if keyword is adjacent technology
        if section_risk == 'HIGH':
            is_adjacent = self._is_adjacent_technology(keyword_lower, content_lower)
            
            if is_adjacent:
                return {
                    'allowed': True,
                    'risk_level': 'SAFE',
                    'reason': f"{keyword} is in the same tech ecosystem as existing project technologies.",
                    'suggestion': f"Add {keyword} to project description if you actually used it."
                }
            else:
                return {
                    'allowed': False,
                    'risk_level': 'FABRICATION',
                    'reason': f"{keyword} is unrelated to project's tech stack. Adding would be fabrication.",
                    'suggestion': f"DON'T add {keyword} to projects. Consider adding to Skills section instead if you have general familiarity."
                }
        
        # For low-risk sections (Experience), more flexible
        if section_risk == 'LOW':
            is_same_domain = self._is_same_domain(keyword_lower, content_lower)
            
            if is_same_domain:
                return {
                    'allowed': True,
                    'risk_level': 'SAFE',
                    'reason': f"{keyword} fits the domain of this experience.",
                    'suggestion': f"Enhance existing descriptions to naturally include {keyword}."
                }
            else:
                return {
                    'allowed': True,
                    'risk_level': 'QUESTIONABLE',
                    'reason': f"{keyword} is somewhat unrelated, but experience descriptions are flexible.",
                    'suggestion': f"Only add {keyword} if you genuinely used it in this role, even peripherally."
                }
        
        # For very-low-risk sections (Skills), very flexible
        if section_risk == 'VERY_LOW':
            return {
                'allowed': True,
                'risk_level': 'SAFE',
                'reason': "Skills section is just listing capabilities. Safe to add if you have any familiarity.",
                'suggestion': f"Add {keyword} to Skills section."
            }
        
        # Default: allow but flag as questionable
        return {
            'allowed': True,
            'risk_level': 'QUESTIONABLE',
            'reason': "Unable to determine context. Use caution.",
            'suggestion': f"Only add {keyword} if truthful."
        }
    
    def _get_section_risk(self, section: str) -> str:
        """Map section name to risk level."""
        section_lower = section.lower()
        
        if 'project' in section_lower:
            return 'HIGH'
        elif 'experience' in section_lower or 'work' in section_lower:
            return 'LOW'
        elif 'skill' in section_lower:
            return 'VERY_LOW'
        elif 'certification' in section_lower or 'education' in section_lower:
            return 'EXTREME'
        else:
            return 'LOW'  # Default to conservative
    
    def _is_adjacent_technology(self, keyword: str, existing_content: str) -> bool:
        """
        Check if keyword is in the same technology family as existing content.
        
        Example:
        - existing_content has "Python, Flask"
        - keyword = "pandas" → TRUE (Python ecosystem)
        - keyword = "Java" → FALSE (different language)
        """
        # Check each tech family
        for family_name, family_data in self.TECH_FAMILIES.items():
            # Check if existing content has any tech from this family
            family_techs = []
            for category, techs in family_data.items():
                family_techs.extend(techs)
            
            has_family_tech = any(tech in existing_content for tech in family_techs)
            
            if has_family_tech:
                # Check if keyword is also in this family
                if keyword in [t.lower() for t in family_techs]:
                    return True
        
        return False
    
    def _is_same_domain(self, keyword: str, existing_content: str) -> bool:
        """
        Check if keyword fits the general domain of the content.
        
        More relaxed than _is_adjacent_technology - used for Experience section.
        """
        # If keyword is mentioned anywhere in existing content, it's same domain
        if keyword in existing_content:
            return True
        
        # Check for semantic relatedness
        # Backend keywords
        backend_keywords = ['api', 'backend', 'server', 'database', 'microservices']
        # Frontend keywords
        frontend_keywords = ['frontend', 'ui', 'react', 'html', 'css', 'design']
        # DevOps keywords
        devops_keywords = ['devops', 'ci/cd', 'docker', 'kubernetes', 'deployment']
        # Data/ML keywords
        data_ml_keywords = ['data', 'machine learning', 'ml', 'analytics', 'ai']
        
        domains = [
            ('backend', backend_keywords),
            ('frontend', frontend_keywords),
            ('devops', devops_keywords),
            ('data_ml', data_ml_keywords)
        ]
        
        for domain_name, domain_keywords in domains:
            has_domain = any(kw in existing_content for kw in domain_keywords)
            keyword_in_domain = any(kw in keyword or keyword in kw for kw in domain_keywords)
            
            if has_domain and keyword_in_domain:
                return True
        
        return False
    
    def filter_keywords_by_context(
        self, 
        keywords: List[str], 
        section: str, 
        existing_content: str
    ) -> Dict[str, List[str]]:
        """
        Filter keywords into SAFE, QUESTIONABLE, and RISKY buckets.
        
        Returns:
            {
                'safe': [...],           # Green light - add these
                'questionable': [...],   # Yellow - use caution  
                'risky': [...]          # Red - don't add
            }
        """
        safe = []
        questionable = []
        risky = []
        
        for keyword in keywords:
            result = self.can_add_keyword(keyword, section, existing_content)
            
            if result['risk_level'] in ['SAFE']:
                safe.append(keyword)
            elif result['risk_level'] in ['QUESTIONABLE']:
                questionable.append(keyword)
            else:
                risky.append(keyword)
        
        return {
            'safe': safe,
            'questionable': questionable,
            'risky': risky
        }
