import PyPDF2
import docx
import pdfplumber
import re
from typing import Dict, List, Optional
import os

class ResumeParser:
    """
    Parse resumes from PDF and DOCX files.
    I tried multiple libraries - pdfplumber works best for most resumes
    but PyPDF2 is good as fallback for simpler PDFs
    """
    
    def __init__(self):
        # Common section headers I've seen in resumes
        self.section_patterns = {
            'contact': r'(contact|email|phone|address)',
            'summary': r'(summary|profile|objective|about)',
            'experience': r'(experience|work history|employment|professional)',
            'education': r'(education|academic|qualifications)',
            'skills': r'(skills|technical skills|competencies|expertise)',
            'projects': r'(projects|portfolio)',
            'certifications': r'(certifications|certificates|licenses)',
            'achievements': r'(achievements|awards|accomplishments)',
        }
        
        # Skills patterns - need to catch these wherever they appear
        self.tech_keywords = [
            'python', 'java', 'javascript', 'react', 'node', 'sql', 'aws',
            'docker', 'kubernetes', 'git', 'agile', 'scrum', 'api', 'rest'
        ]
    
    def parse(self, file_path: str) -> Dict:
        """
        Main parsing function. Returns structured resume data.
        TODO: might want to add error recovery for corrupted files
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Resume file not found: {file_path}")
        
        # Figure out file type
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == '.pdf':
            text = self._parse_pdf(file_path)
        elif file_ext in ['.docx', '.doc']:
            text = self._parse_docx(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_ext}")
        
        # Extract structured data from raw text
        structured_data = self._extract_sections(text)
        structured_data['raw_text'] = text
        structured_data['file_name'] = os.path.basename(file_path)
        
        return structured_data
    
    def _parse_pdf(self, file_path: str) -> str:
        """
        Parse PDF resume. I'm using pdfplumber first cause it handles
        formatting better, but will fallback to PyPDF2 if needed
        """
        text = ""
        
        try:
            # Try pdfplumber first - works better with formatted resumes
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"pdfplumber failed, trying PyPDF2... Error: {e}")
            
            # Fallback to PyPDF2
            try:
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
            except Exception as e2:
                raise Exception(f"Could not parse PDF with either library: {e2}")
        
        return text.strip()
    
    def _parse_docx(self, file_path: str) -> str:
        """Simple DOCX parsing - pretty straightforward"""
        try:
            doc = docx.Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text.strip()
        except Exception as e:
            raise Exception(f"Error parsing DOCX: {e}")
    
    def _extract_sections(self, text: str) -> Dict:
        """
        Break resume into sections. This is tricky cause everyone
        formats their resume differently... doing my best here
        """
        sections = {
            'contact_info': self._extract_contact_info(text),
            'summary': '',
            'experience': [],
            'education': [],
            'skills': [],
            'projects': [],
            'certifications': [],
            'achievements': []
        }
        
        # Split text into lines for processing
        lines = text.split('\n')
        current_section = None
        section_content = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if this line is a section header
            detected_section = self._detect_section_header(line)
            
            if detected_section:
                # Save previous section content
                if current_section and section_content:
                    sections[current_section] = '\n'.join(section_content)
                
                current_section = detected_section
                section_content = []
            elif current_section:
                section_content.append(line)
        
        # Don't forget the last section!
        if current_section and section_content:
            sections[current_section] = '\n'.join(section_content)
        
        # Parse specific sections into structured data
        sections['skills'] = self._extract_skills(text)
        sections['experience'] = self._parse_experience_section(sections.get('experience', ''))
        sections['education'] = self._parse_education_section(sections.get('education', ''))
        
        return sections
    
    def _detect_section_header(self, line: str) -> Optional[str]:
        """
        Check if a line is a section header.
        Headers are usually short, might be all caps, etc.
        """
        if len(line) > 50:  # Headers are usually short
            return None
        
        line_lower = line.lower()
        
        for section_name, pattern in self.section_patterns.items():
            if re.search(pattern, line_lower, re.IGNORECASE):
                return section_name
        
        return None
    
    def _extract_contact_info(self, text: str) -> Dict:
        """
        Extract email, phone, LinkedIn etc. Usually at the top of resume
        """
        contact = {
            'email': '',
            'phone': '',
            'linkedin': '',
            'github': '',
            'location': ''
        }
        
        # Email pattern
        email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        if email_match:
            contact['email'] = email_match.group(0)
        
        # Phone pattern - handles various formats
        phone_match = re.search(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
        if phone_match:
            contact['phone'] = phone_match.group(0)
        
        # LinkedIn
        linkedin_match = re.search(r'linkedin\.com/in/[\w-]+', text, re.IGNORECASE)
        if linkedin_match:
            contact['linkedin'] = linkedin_match.group(0)
        
        # GitHub
        github_match = re.search(r'github\.com/[\w-]+', text, re.IGNORECASE)
        if github_match:
            contact['github'] = github_match.group(0)
        
        return contact
    
    def _extract_skills(self, text: str) -> List[str]:
        """
        Extract skills from entire resume. Skills can appear anywhere,
        not just in skills section, so I'm scanning the whole thing
        """
        skills = []
        text_lower = text.lower()
        
        # Look for common tech skills
        # TODO: expand this list, maybe load from a file?
        common_skills = [
            'python', 'java', 'javascript', 'typescript', 'react', 'angular', 'vue',
            'node.js', 'express', 'django', 'flask', 'fastapi', 'spring boot',
            'sql', 'mysql', 'postgresql', 'mongodb', 'redis',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins',
            'git', 'github', 'gitlab', 'ci/cd',
            'agile', 'scrum', 'jira', 'rest api', 'graphql',
            'html', 'css', 'sass', 'tailwind',
            'machine learning', 'deep learning', 'tensorflow', 'pytorch',
            'data analysis', 'pandas', 'numpy', 'scikit-learn',
            'leadership', 'communication', 'problem solving', 'teamwork'
        ]
        
        for skill in common_skills:
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                skills.append(skill.title())
        
        return list(set(skills))  # Remove duplicates
    
    def _parse_experience_section(self, experience_text: str) -> List[Dict]:
        """
        Parse work experience into structured format.
        This is rough - experience sections vary A LOT between resumes
        """
        experiences = []
        
        if not experience_text:
            return experiences
        
        # Split by common job entry patterns
        # Usually job title, company, dates on separate lines or same line
        lines = experience_text.split('\n')
        
        current_job = None
        
        for line in lines:
            line = line.strip()
            if not line:
                if current_job and current_job.get('description'):
                    experiences.append(current_job)
                    current_job = None
                continue
            
            # Check if line contains a date range (indicates job entry)
            # Support formats: "2024 - 2025", "June 2024 - Aug 2025", "2024-Present"
            date_pattern = r'(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|\d{4})\s*[-–—]\s*(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|\d{4}|present|current)'
            if re.search(date_pattern, line, re.IGNORECASE):
                if current_job:
                    experiences.append(current_job)
                
                current_job = {
                    'title': '',
                    'company': '',
                    'dates': line,
                    'description': []
                }
            elif current_job:
                # Check if it's a bullet point
                if line.startswith(('•', '-', '*', '○')):
                    current_job['description'].append(line[1:].strip())
                else:
                    # Probably title or company
                    if not current_job['title']:
                        current_job['title'] = line
                    elif not current_job['company']:
                        current_job['company'] = line
        
        # Add last job
        if current_job and current_job.get('description'):
            experiences.append(current_job)
        
        return experiences
    
    def _parse_education_section(self, education_text: str) -> List[Dict]:
        """Parse education entries"""
        education = []
        
        if not education_text:
            return education
        
        lines = education_text.split('\n')
        current_edu = None
        
        for line in lines:
            line = line.strip()
            if not line:
                if current_edu:
                    education.append(current_edu)
                    current_edu = None
                continue
            
            # Look for degree keywords
            degree_keywords = ['bachelor', 'master', 'phd', 'b.s.', 'm.s.', 'b.a.', 'm.a.']
            
            if any(keyword in line.lower() for keyword in degree_keywords):
                if current_edu:
                    education.append(current_edu)
                
                current_edu = {
                    'degree': line,
                    'institution': '',
                    'year': ''
                }
            elif current_edu:
                # Look for graduation year
                year_match = re.search(r'20\d{2}', line)
                if year_match and not current_edu['year']:
                    current_edu['year'] = year_match.group(0)
                
                if not current_edu['institution']:
                    current_edu['institution'] = line
        
        if current_edu:
            education.append(current_edu)
        
        return education
