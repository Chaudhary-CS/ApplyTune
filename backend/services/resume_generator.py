from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from typing import Dict
import os
from datetime import datetime

class ResumeGenerator:
    """
    Generate clean, ATS-friendly PDF resumes.
    
    Important: ATS systems are picky about PDF formatting!
    What to avoid:
    - Tables (many ATS can't parse them)
    - Images and graphics (they ignore them)
    - Multiple columns (confuses the parser)
    - Headers/footers (sometimes ignored)
    - Fancy fonts (stick to standard ones)
    
    I'm using ReportLab to create simple, clean PDFs that any ATS can read.
    """
    
    def __init__(self):
        self.output_dir = "outputs"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Define styles - keeping it simple for ATS compatibility
        self.styles = getSampleStyleSheet()
        
        # Custom styles for different sections
        self.name_style = ParagraphStyle(
            'CustomName',
            parent=self.styles['Heading1'],
            fontSize=18,
            textColor='#1a1a1a',
            spaceAfter=6,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        self.contact_style = ParagraphStyle(
            'CustomContact',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor='#4a4a4a',
            alignment=TA_CENTER,
            spaceAfter=12
        )
        
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=13,
            textColor='#1a1a1a',
            spaceAfter=8,
            spaceBefore=12,
            fontName='Helvetica-Bold',
            borderWidth=1,
            borderColor='#cccccc',
            borderPadding=3,
            backColor='#f5f5f5'
        )
        
        self.normal_style = ParagraphStyle(
            'CustomNormal',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor='#2a2a2a',
            spaceAfter=6,
            leading=14
        )
        
        self.bullet_style = ParagraphStyle(
            'CustomBullet',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor='#2a2a2a',
            spaceAfter=4,
            leftIndent=20,
            bulletIndent=10,
            leading=13
        )
    
    def generate_pdf(self, resume_data: Dict, custom_filename: str = None) -> str:
        """
        Generate a PDF resume from structured resume data.
        Returns path to generated file.
        """
        # Create filename
        if custom_filename:
            filename = f"{custom_filename}.pdf"
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"resume_optimized_{timestamp}.pdf"
        
        filepath = os.path.join(self.output_dir, filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(
            filepath,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        # Build content
        story = []
        
        # Add header (name and contact)
        story.extend(self._build_header(resume_data))
        
        # Add summary if exists
        if resume_data.get('summary'):
            story.extend(self._build_summary(resume_data['summary']))
        
        # Add skills
        if resume_data.get('skills'):
            story.extend(self._build_skills(resume_data['skills']))
        
        # Add experience
        if resume_data.get('experience'):
            story.extend(self._build_experience(resume_data['experience']))
        
        # Add education
        if resume_data.get('education'):
            story.extend(self._build_education(resume_data['education']))
        
        # Add projects if any
        if resume_data.get('projects'):
            story.extend(self._build_projects(resume_data['projects']))
        
        # Add certifications if any
        if resume_data.get('certifications'):
            story.extend(self._build_certifications(resume_data['certifications']))
        
        # Build PDF
        doc.build(story)
        
        return filepath
    
    def _build_header(self, resume_data: Dict) -> list:
        """Build the header with name and contact info"""
        elements = []
        
        contact_info = resume_data.get('contact_info', {})
        
        # Name - try to extract from contact or use a default
        # In real scenario, we'd ask user for their name
        name = contact_info.get('name', 'Your Name')
        if name == 'Your Name' and contact_info.get('email'):
            # Try to get name from email
            email = contact_info['email']
            name_part = email.split('@')[0]
            name = name_part.replace('.', ' ').replace('_', ' ').title()
        
        elements.append(Paragraph(name, self.name_style))
        
        # Contact info on one line
        contact_parts = []
        
        if contact_info.get('email'):
            contact_parts.append(contact_info['email'])
        
        if contact_info.get('phone'):
            contact_parts.append(contact_info['phone'])
        
        if contact_info.get('linkedin'):
            linkedin = contact_info['linkedin']
            if not linkedin.startswith('http'):
                linkedin = f"linkedin.com/in/{linkedin}"
            contact_parts.append(linkedin)
        
        if contact_info.get('github'):
            github = contact_info['github']
            if not github.startswith('http'):
                github = f"github.com/{github}"
            contact_parts.append(github)
        
        if contact_info.get('location'):
            contact_parts.append(contact_info['location'])
        
        if contact_parts:
            contact_line = ' | '.join(contact_parts)
            elements.append(Paragraph(contact_line, self.contact_style))
        
        elements.append(Spacer(1, 0.1*inch))
        
        return elements
    
    def _build_summary(self, summary: str) -> list:
        """Build professional summary section"""
        elements = []
        
        elements.append(Paragraph("PROFESSIONAL SUMMARY", self.heading_style))
        elements.append(Paragraph(summary, self.normal_style))
        elements.append(Spacer(1, 0.15*inch))
        
        return elements
    
    def _build_skills(self, skills: list) -> list:
        """Build skills section"""
        elements = []
        
        elements.append(Paragraph("SKILLS", self.heading_style))
        
        # Group skills into a readable format
        # ATS systems parse this better as a paragraph than a list
        skills_text = ' • '.join(skills[:25])  # Limit to 25 skills
        elements.append(Paragraph(skills_text, self.normal_style))
        elements.append(Spacer(1, 0.15*inch))
        
        return elements
    
    def _build_experience(self, experience: list) -> list:
        """Build work experience section"""
        elements = []
        
        elements.append(Paragraph("PROFESSIONAL EXPERIENCE", self.heading_style))
        
        for exp in experience:
            # Job title and company
            title = exp.get('title', 'Position')
            company = exp.get('company', 'Company')
            dates = exp.get('dates', '')
            
            # Format: Job Title | Company (if we have it)
            if company and company.strip():
                job_line = f"<b>{title}</b> | {company}"
            else:
                job_line = f"<b>{title}</b>"
            
            if dates:
                job_line += f" | {dates}"
            
            elements.append(Paragraph(job_line, self.normal_style))
            elements.append(Spacer(1, 0.05*inch))
            
            # Bullet points
            description = exp.get('description', [])
            if isinstance(description, str):
                description = [description]
            
            for bullet in description:
                bullet_text = f"• {bullet}"
                elements.append(Paragraph(bullet_text, self.bullet_style))
            
            elements.append(Spacer(1, 0.1*inch))
        
        return elements
    
    def _build_education(self, education: list) -> list:
        """Build education section"""
        elements = []
        
        elements.append(Paragraph("EDUCATION", self.heading_style))
        
        for edu in education:
            if isinstance(edu, dict):
                degree = edu.get('degree', 'Degree')
                institution = edu.get('institution', '')
                year = edu.get('year', '')
                
                edu_line = f"<b>{degree}</b>"
                if institution:
                    edu_line += f" | {institution}"
                if year:
                    edu_line += f" | {year}"
                
                elements.append(Paragraph(edu_line, self.normal_style))
            else:
                # If education is just a string
                elements.append(Paragraph(str(edu), self.normal_style))
        
        elements.append(Spacer(1, 0.1*inch))
        
        return elements
    
    def _build_projects(self, projects: list) -> list:
        """Build projects section"""
        elements = []
        
        elements.append(Paragraph("PROJECTS", self.heading_style))
        
        # Handle different project formats
        if isinstance(projects, str):
            elements.append(Paragraph(projects, self.normal_style))
        elif isinstance(projects, list):
            for project in projects:
                if isinstance(project, dict):
                    name = project.get('name', 'Project')
                    description = project.get('description', '')
                    elements.append(Paragraph(f"<b>{name}</b>", self.normal_style))
                    if description:
                        elements.append(Paragraph(f"• {description}", self.bullet_style))
                else:
                    elements.append(Paragraph(f"• {project}", self.bullet_style))
        
        elements.append(Spacer(1, 0.1*inch))
        
        return elements
    
    def _build_certifications(self, certifications: list) -> list:
        """Build certifications section"""
        elements = []
        
        elements.append(Paragraph("CERTIFICATIONS", self.heading_style))
        
        if isinstance(certifications, str):
            elements.append(Paragraph(certifications, self.normal_style))
        elif isinstance(certifications, list):
            for cert in certifications:
                if isinstance(cert, dict):
                    name = cert.get('name', '')
                    issuer = cert.get('issuer', '')
                    cert_line = f"• {name}"
                    if issuer:
                        cert_line += f" - {issuer}"
                    elements.append(Paragraph(cert_line, self.bullet_style))
                else:
                    elements.append(Paragraph(f"• {cert}", self.bullet_style))
        
        return elements
