"""
Context Validator Service
Validates whether keyword insertions make sense in context.
Prevents fabrication and maintains resume authenticity.
"""

from typing import Dict, List
import re


class ContextValidator:
    """
    Validates keyword insertions to prevent:
    - Fabricating project tech stacks
    - Changing verifiable information
    - Adding unrelated keywords
    - Creating inconsistent claims
    """
    
    def __init__(self):
        # Define tech stack categories and related technologies
        self.tech_ecosystems = {
            'python': {
                'core': ['python'],
                'related': ['django', 'flask', 'fastapi', 'pandas', 'numpy', 
                           'pytorch', 'tensorflow', 'scikit-learn', 'jupyter']
            },
            'javascript': {
                'core': ['javascript', 'typescript', 'node.js', 'node'],
                'related': ['react', 'angular', 'vue', 'express', 'next.js', 
                           'webpack', 'npm', 'yarn', 'jest']
            },
            'java': {
                'core': ['java'],
                'related': ['spring', 'spring boot', 'maven', 'gradle', 
                           'hibernate', 'junit']
            },
            'devops': {
                'core': ['docker', 'kubernetes', 'ci/cd', 'devops'],
                'related': ['jenkins', 'gitlab ci', 'github actions', 'ansible', 
                           'terraform', 'aws', 'azure', 'gcp']
            },
            'databases': {
                'core': ['sql', 'database'],
                'related': ['postgresql', 'mysql', 'mongodb', 'redis', 
                           'elasticsearch', 'dynamodb']
            },
            'ml_ai': {
                'core': ['machine learning', 'ml', 'ai', 'artificial intelligence'],
                'related': ['pytorch', 'tensorflow', 'scikit-learn', 'keras', 
                           'transformers', 'neural network', 'deep learning']
            }
        }
        
        # Risky sections where changes are often verifiable
        self.risky_sections = ['project', 'education', 'certification', 'publication']
        
        # Safe sections where additions are generally acceptable
        self.safe_sections = ['experience', 'skill', 'summary', 'objective']
    
    def validate_keyword_insertion(
        self,
        keyword: str,
        context: str,
        section_type: str,
        existing_tech_stack: List[str] = None
    ) -> Dict:
        """
        Validate if a keyword can be safely added to a specific context.
        
        Args:
            keyword: The keyword to add
            context: The surrounding text where keyword would be added
            section_type: Type of section (project, experience, skills, etc.)
            existing_tech_stack: Technologies already mentioned in the context
            
        Returns:
            Dict with validation result
        """
        keyword_lower = keyword.lower()
        context_lower = context.lower()
        section_lower = section_type.lower()
        
        validation_result = {
            'allowed': True,
            'risk_level': 'SAFE',
            'confidence': 1.0,
            'reason': '',
            'suggestion': ''
        }
        
        # Check if it's a risky section
        is_risky = any(risky in section_lower for risky in self.risky_sections)
        
        if is_risky:
            # For projects, validate tech stack compatibility
            if 'project' in section_lower:
                validation_result = self._validate_project_tech(
                    keyword, context, existing_tech_stack
                )
            # For education/certifications, be very conservative
            elif any(section in section_lower for section in ['education', 'certification']):
                validation_result['allowed'] = False
                validation_result['risk_level'] = 'HIGH_RISK'
                validation_result['confidence'] = 0.0
                validation_result['reason'] = f"Cannot add keywords to {section_type} - this is verifiable information"
                validation_result['suggestion'] = "Add this keyword to Skills or Experience sections instead"
        
        else:
            # Safe sections - check for logical consistency
            validation_result = self._validate_safe_section(keyword, context, section_type)
        
        return validation_result
    
    def _validate_project_tech(
        self, 
        keyword: str, 
        context: str,
        existing_tech_stack: List[str] = None
    ) -> Dict:
        """Validate if a tech keyword fits the project's existing stack."""
        keyword_lower = keyword.lower()
        context_lower = context.lower()
        
        # Identify the tech ecosystem of the project
        project_ecosystem = None
        
        if existing_tech_stack:
            for tech in existing_tech_stack:
                ecosystem = self._identify_ecosystem(tech.lower())
                if ecosystem:
                    project_ecosystem = ecosystem
                    break
        
        # If no existing stack identified, look in context
        if not project_ecosystem:
            for ecosystem_name, ecosystem_data in self.tech_ecosystems.items():
                for tech in ecosystem_data['core'] + ecosystem_data['related']:
                    if tech in context_lower:
                        project_ecosystem = ecosystem_name
                        break
                if project_ecosystem:
                    break
        
        # Now validate the keyword against the ecosystem
        if project_ecosystem:
            keyword_ecosystem = self._identify_ecosystem(keyword_lower)
            
            # Check if keyword belongs to the same or compatible ecosystem
            if keyword_ecosystem == project_ecosystem:
                return {
                    'allowed': True,
                    'risk_level': 'SAFE',
                    'confidence': 0.9,
                    'reason': f"Keyword '{keyword}' is compatible with project's {project_ecosystem} stack",
                    'suggestion': 'Safe to add'
                }
            
            # Check if it's a related technology
            if keyword_lower in self.tech_ecosystems[project_ecosystem]['related']:
                return {
                    'allowed': True,
                    'risk_level': 'LOW_RISK',
                    'confidence': 0.7,
                    'reason': f"Keyword '{keyword}' is related to {project_ecosystem} ecosystem",
                    'suggestion': 'Can be added if it genuinely fits the project'
                }
            
            # Incompatible tech stack
            return {
                'allowed': False,
                'risk_level': 'FABRICATION',
                'confidence': 0.1,
                'reason': f"Keyword '{keyword}' ({keyword_ecosystem}) doesn't fit project's {project_ecosystem} stack",
                'suggestion': 'Do NOT add - this would look fake. Projects are often verifiable on GitHub.'
            }
        
        # Unknown ecosystem - be cautious
        return {
            'allowed': True,
            'risk_level': 'MEDIUM_RISK',
            'confidence': 0.5,
            'reason': "Unable to determine project's tech stack",
            'suggestion': 'Add with caution - ensure it genuinely fits'
        }
    
    def _validate_safe_section(
        self, 
        keyword: str, 
        context: str,
        section_type: str
    ) -> Dict:
        """Validate keyword insertion in safe sections like experience or skills."""
        keyword_lower = keyword.lower()
        context_lower = context.lower()
        
        # For skills section, almost anything goes
        if 'skill' in section_type.lower():
            return {
                'allowed': True,
                'risk_level': 'SAFE',
                'confidence': 0.95,
                'reason': 'Skills section is a safe place for keyword additions',
                'suggestion': 'Add naturally to relevant skill category'
            }
        
        # For experience, check if it makes contextual sense
        if 'experience' in section_type.lower():
            # Check if keyword is already somewhat related to context
            keyword_ecosystem = self._identify_ecosystem(keyword_lower)
            
            if keyword_ecosystem:
                # Check if context has related technologies
                for tech in self.tech_ecosystems[keyword_ecosystem]['related']:
                    if tech in context_lower:
                        return {
                            'allowed': True,
                            'risk_level': 'SAFE',
                            'confidence': 0.85,
                            'reason': f"Keyword fits the technical context of this experience",
                            'suggestion': 'Integrate naturally into a bullet point'
                        }
            
            # Generic approval for experience
            return {
                'allowed': True,
                'risk_level': 'LOW_RISK',
                'confidence': 0.7,
                'reason': 'Experience descriptions can be enhanced with relevant keywords',
                'suggestion': 'Add in a way that describes actual work, not fabricated claims'
            }
        
        # Default for other safe sections
        return {
            'allowed': True,
            'risk_level': 'SAFE',
            'confidence': 0.8,
            'reason': f'{section_type} is generally safe for keyword additions',
            'suggestion': 'Add naturally and contextually'
        }
    
    def _identify_ecosystem(self, keyword: str) -> str:
        """Identify which tech ecosystem a keyword belongs to."""
        for ecosystem_name, ecosystem_data in self.tech_ecosystems.items():
            if keyword in ecosystem_data['core'] or keyword in ecosystem_data['related']:
                return ecosystem_name
        return None
    
    def batch_validate(
        self,
        keywords: List[str],
        resume_sections: Dict[str, str]
    ) -> Dict[str, List[Dict]]:
        """
        Validate multiple keywords against resume sections.
        
        Args:
            keywords: List of keywords to validate
            resume_sections: Dict of section_name: section_content
            
        Returns:
            Dict mapping section names to validation results
        """
        results = {}
        
        for section_name, section_content in resume_sections.items():
            section_results = []
            
            for keyword in keywords:
                validation = self.validate_keyword_insertion(
                    keyword=keyword,
                    context=section_content,
                    section_type=section_name
                )
                
                if validation['allowed']:
                    section_results.append({
                        'keyword': keyword,
                        'validation': validation
                    })
            
            if section_results:
                results[section_name] = section_results
        
        return results
