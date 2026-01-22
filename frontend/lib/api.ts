import axios from 'axios'

// Get API URL from env or default to localhost
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

// Create axios instance with default config
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 120000, // AI optimization can take a minute or so
})

// Types
export interface JobData {
  job_title: string
  company_name: string
  description: string
}

export interface OptimizationResult {
  original_score: number
  optimized_score: number
  ats_scores: {
    original: Record<string, number>
    optimized: Record<string, number>
  }
  matched_keywords: string[]
  missing_keywords: string[]
  suggestions: string[]
  score_breakdown: Record<string, any>
  improvement_percentage: number
  optimized_resume: any
}

/**
 * Upload and parse a resume
 */
export async function uploadResume(file: File) {
  const formData = new FormData()
  formData.append('file', file)

  const response = await api.post('/upload-resume', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })

  return response.data
}

/**
 * Analyze a job description
 */
export async function analyzeJob(jobData: JobData) {
  const response = await api.post('/analyze-job', jobData)
  return response.data
}

/**
 * The big one - optimize resume for job
 * Supports both file upload and LaTeX text paste
 */
export async function optimizeResume(
  file: File | null,
  jobData: JobData,
  latexCode?: string
): Promise<OptimizationResult> {
  const formData = new FormData()
  
  // Add file OR LaTeX code
  if (file) {
    formData.append('file', file)
  } else if (latexCode) {
    // Create a virtual .tex file from the LaTeX code
    const latexBlob = new Blob([latexCode], { type: 'application/x-tex' })
    const latexFile = new File([latexBlob], 'resume.tex', { type: 'application/x-tex' })
    formData.append('file', latexFile)
  } else {
    throw new Error('Either file or LaTeX code must be provided')
  }
  
  formData.append('job_title', jobData.job_title)
  formData.append('company_name', jobData.company_name)
  formData.append('job_description', jobData.description)

  try {
    const response = await api.post('/optimize-resume', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })

    return response.data
  } catch (error: any) {
    // Better error handling
    if (error.response) {
      throw new Error(error.response.data.detail || 'Optimization failed')
    } else if (error.request) {
      throw new Error('No response from server. Is the backend running?')
    } else {
      throw new Error('Request failed: ' + error.message)
    }
  }
}

/**
 * Generate PDF from optimized resume
 */
export async function generatePDF(resumeData: any) {
  const response = await api.post('/generate-pdf', resumeData)
  return response.data
}

/**
 * Download generated PDF
 */
export function getDownloadUrl(filename: string): string {
  return `${API_URL}/download/${filename}`
}

/**
 * Health check
 */
export async function healthCheck() {
  const response = await api.get('/health')
  return response.data
}
