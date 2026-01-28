"""
Tech Ecosystem Graph Validator (Layer 1)
Fast rejection of obviously incompatible tech combinations.
"""

from typing import Dict, List, Optional

class TechEcosystemValidator:
    """
    Validates if keywords belong to compatible tech ecosystems.
    This is Layer 1 - the fastest filter that catches obvious mismatches.
    """
    
    def __init__(self):
        # Define tech ecosystems and their related technologies
        self.ecosystems = {
            'machine_learning': {
                'frameworks': ['pytorch', 'tensorflow', 'scikit-learn', 'keras', 'xgboost', 'lightgbm'],
                'infrastructure': ['tpus', 'gpus', 'cuda', 'mlflow', 'kubeflow', 'sagemaker'],
                'languages': ['python', 'r', 'julia'],
                'tools': ['jupyter', 'pandas', 'numpy', 'matplotlib', 'model training', 'inference'],
                'keywords': ['ml', 'machine learning', 'deep learning', 'neural network', 'model', 'training']
            },
            'devops': {
                'ci_cd': ['azure devops', 'jenkins', 'github actions', 'gitlab ci', 'circleci', 'travis ci'],
                'containers': ['docker', 'kubernetes', 'containerd', 'podman', 'k8s', 'container orchestrator'],
                'infrastructure': ['ansible', 'terraform', 'puppet', 'chef', 'bare metal setup'],
                'cloud': ['aws', 'azure', 'gcp', 'cloud computing'],
                'monitoring': ['prometheus', 'grafana', 'datadog', 'new relic', 'observability'],
                'languages': ['bash', 'python', 'yaml', 'golang', 'shell'],
                'keywords': ['automation', 'deployment', 'ci/cd', 'infrastructure', 'pipeline']
            },
            'backend': {
                'frameworks': ['spring boot', 'flask', 'django', 'express', 'fastapi', 'node.js'],
                'databases': ['postgresql', 'mysql', 'mongodb', 'redis', 'cassandra', 'dynamodb'],
                'languages': ['java', 'python', 'javascript', 'golang', 'c++', 'typescript'],
                'messaging': ['kafka', 'rabbitmq', 'redis', 'sqs'],
                'keywords': ['rest api', 'microservices', 'database design', 'backend services', 'api design']
            },
            'frontend': {
                'frameworks': ['react.js', 'react', 'angular', 'vue', 'next.js', 'svelte'],
                'languages': ['javascript', 'typescript', 'html5', 'css3', 'html', 'css'],
                'tools': ['webpack', 'babel', 'npm', 'yarn', 'vite'],
                'keywords': ['ui/ux', 'responsive', 'web development', 'frontend', 'user interface']
            },
            'data_engineering': {
                'tools': ['hadoop', 'spark', 'airflow', 'kafka', 'flink'],
                'databases': ['postgresql', 'mongodb', 'redis', 'snowflake', 'bigquery'],
                'languages': ['python', 'scala', 'sql', 'java'],
                'keywords': ['data pipeline', 'etl', 'data warehouse', 'big data']
            },
            'systems': {
                'concepts': ['operating systems', 'networking', 'processes', 'file systems', 
                           'virtualization', 'concurrency programming', 'multi-threaded'],
                'tools': ['linux', 'unix', 'windows'],
                'languages': ['c', 'c++', 'rust', 'go', 'golang'],
                'keywords': ['low-level', 'system design', 'performance']
            },
            'testing': {
                'tools': ['jest', 'pytest', 'junit', 'selenium', 'cypress'],
                'types': ['unit testing', 'integration testing', 'qa', 'test automation'],
                'keywords': ['testing', 'quality assurance', 'test cases']
            },
            'general_cs': {
                'concepts': ['object-oriented programming', 'oop', 'data structures', 'algorithms',
                           'design patterns', 'computer science', 'software engineering'],
                'skills': ['problem-solving', 'self-directed learning', 'debugging', 'code review']
            }
        }
        
        # Define which ecosystems can coexist (they're often used together)
        self.compatible_pairs = {
            ('machine_learning', 'backend'),      # ML models in backend services
            ('machine_learning', 'data_engineering'),  # ML data pipelines
            ('devops', 'backend'),                # DevOps for backend deployment
            ('devops', 'frontend'),               # DevOps for frontend deployment
            ('devops', 'machine_learning'),       # MLOps
            ('backend', 'frontend'),              # Full-stack
            ('backend', 'data_engineering'),      # Backend data pipelines
            ('systems', 'backend'),               # Low-level backend work
            ('systems', 'devops'),                # Infrastructure work
            ('testing', 'backend'),               # Backend testing
            ('testing', 'frontend'),              # Frontend testing
            ('general_cs', 'backend'),            # General CS applies to backend
            ('general_cs', 'frontend'),           # General CS applies to frontend
            ('general_cs', 'machine_learning'),   # General CS applies to ML
            ('general_cs', 'devops'),             # General CS applies to DevOps
        }
        
        # Build reverse lookup for fast keyword->ecosystem mapping
        self._build_keyword_lookup()
    
    def _build_keyword_lookup(self):
        """Build a reverse index: keyword -> list of ecosystems it belongs to."""
        self.keyword_to_ecosystems = {}
        
        for ecosystem_name, categories in self.ecosystems.items():
            for category, items in categories.items():
                for item in items:
                    item_lower = item.lower()
                    if item_lower not in self.keyword_to_ecosystems:
                        self.keyword_to_ecosystems[item_lower] = []
                    self.keyword_to_ecosystems[item_lower].append(ecosystem_name)
    
    def find_keyword_ecosystems(self, keyword: str) -> List[str]:
        """Find all ecosystems a keyword belongs to."""
        keyword_lower = keyword.lower().strip()
        
        # Direct match
        if keyword_lower in self.keyword_to_ecosystems:
            return self.keyword_to_ecosystems[keyword_lower]
        
        # Partial match (e.g., "k8s" matches "kubernetes")
        matching_ecosystems = []
        for known_keyword, ecosystems in self.keyword_to_ecosystems.items():
            if keyword_lower in known_keyword or known_keyword in keyword_lower:
                matching_ecosystems.extend(ecosystems)
        
        return list(set(matching_ecosystems))
    
    def extract_context_ecosystems(self, context: str) -> List[str]:
        """Extract all ecosystems mentioned in a context string."""
        context_lower = context.lower()
        found_ecosystems = set()
        
        for keyword, ecosystems in self.keyword_to_ecosystems.items():
            if keyword in context_lower:
                found_ecosystems.update(ecosystems)
        
        return list(found_ecosystems)
    
    def are_ecosystems_compatible(self, eco1: str, eco2: str) -> bool:
        """Check if two ecosystems are compatible."""
        if eco1 == eco2:
            return True
        
        # Check if the pair is in our compatible pairs (in either order)
        return (eco1, eco2) in self.compatible_pairs or (eco2, eco1) in self.compatible_pairs
    
    def validate_keyword_in_context(self, keyword: str, context: str) -> Dict:
        """
        Main validation method: Check if a keyword fits in the given context.
        
        Args:
            keyword: The keyword to insert (e.g., "pytorch")
            context: The bullet point or section text (e.g., "Azure DevOps CI/CD")
        
        Returns:
            {
                'valid': bool,
                'confidence': 'HIGH'/'MEDIUM'/'LOW',
                'reason': str,
                'keyword_ecosystems': list,
                'context_ecosystems': list
            }
        """
        keyword_ecosystems = self.find_keyword_ecosystems(keyword)
        context_ecosystems = self.extract_context_ecosystems(context)
        
        # Unknown keyword - can't validate, allow but with LOW confidence
        if not keyword_ecosystems:
            return {
                'valid': True,
                'confidence': 'LOW',
                'reason': f'"{keyword}" is not in our tech database, allowing with caution',
                'keyword_ecosystems': [],
                'context_ecosystems': context_ecosystems
            }
        
        # Empty context - hard to validate, allow but with MEDIUM confidence
        if not context_ecosystems:
            return {
                'valid': True,
                'confidence': 'MEDIUM',
                'reason': f'Context has no clear tech indicators, allowing "{keyword}"',
                'keyword_ecosystems': keyword_ecosystems,
                'context_ecosystems': []
            }
        
        # Check compatibility between keyword and context ecosystems
        for keyword_eco in keyword_ecosystems:
            for context_eco in context_ecosystems:
                if self.are_ecosystems_compatible(keyword_eco, context_eco):
                    return {
                        'valid': True,
                        'confidence': 'HIGH',
                        'reason': f'"{keyword}" ({keyword_eco}) fits well with {context_eco} context',
                        'keyword_ecosystems': keyword_ecosystems,
                        'context_ecosystems': context_ecosystems
                    }
        
        # No compatible ecosystems found - REJECT
        return {
            'valid': False,
            'confidence': 'HIGH',
            'reason': f'"{keyword}" ({", ".join(keyword_ecosystems)}) does not fit in {", ".join(context_ecosystems)} context',
            'keyword_ecosystems': keyword_ecosystems,
            'context_ecosystems': context_ecosystems
        }
    
    def batch_validate(self, keywords: List[str], context: str) -> List[Dict]:
        """Validate multiple keywords against the same context."""
        results = []
        for keyword in keywords:
            result = self.validate_keyword_in_context(keyword, context)
            result['keyword'] = keyword
            results.append(result)
        return results
