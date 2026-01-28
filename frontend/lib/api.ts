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

export interface GenuinityAnalysis {
  score: number
  risk_level: 'LOW' | 'MEDIUM' | 'HIGH'
  issues: Array<{
    type: string
    severity: string
    description: string
    impact: number
  }>
  warnings: Array<{
    type: string
    severity: string
    description: string
    impact: number
  }>
  strengths: string[]
  recommendations: string[]
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
  genuinity?: GenuinityAnalysis // New field
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
 * The big one - optimize resume for job with genuinity analysis
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
    formData.append('latex_code', latexCode)
  } else {
    throw new Error('Either file or LaTeX code must be provided')
  }
  
  formData.append('job_title', jobData.job_title || '')
  formData.append('job_description', jobData.description)

  try {
    const response = await api.post('/api/optimize', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })

    // Transform response to match OptimizationResult interface
    const data = response.data
    
    // Validation: ensure data is an object
    if (!data || typeof data !== 'object') {
      console.error('Invalid response data:', data)
      throw new Error('Invalid response from server')
    }
    
    // Validation: ensure required fields exist
    if (!data.scores || !data.keywords || !data.optimized_resume) {
      console.error('Missing required fields in response:', data)
      throw new Error('Incomplete response from server')
    }
    
    return {
      original_score: data.scores?.original?.overall_score || 0,
      optimized_score: data.scores?.optimized?.overall_score || 0,
      ats_scores: {
        original: data.scores?.original?.ats_specific || {},
        optimized: data.scores?.optimized?.ats_specific || {}
      },
      matched_keywords: data.keywords?.matched_optimized || [],
      missing_keywords: data.keywords?.missing_optimized || [],
      suggestions: data.genuinity?.recommendations || [],
      score_breakdown: data.scores?.optimized?.breakdown || {},
      improvement_percentage: data.scores?.improvement || 0,
      optimized_resume: {
        latex_content: data.optimized_resume?.content || null,
        ...data.optimized_resume
      },
      genuinity: data.genuinity // NEW: Genuinity analysis
    }
  } catch (error: any) {
    // Better error handling
    console.error('Optimization error:', error)
    if (error.response) {
      const detail = error.response.data?.detail || error.response.data || 'Optimization failed'
      throw new Error(typeof detail === 'string' ? detail : JSON.stringify(detail))
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
