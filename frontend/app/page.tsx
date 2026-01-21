'use client'

import { useState } from 'react'
import { FileUp, Sparkles, TrendingUp, CheckCircle2, ArrowRight } from 'lucide-react'
import FileUploader from '@/components/FileUploader'
import JobDescriptionForm from '@/components/JobDescriptionForm'
import ResultsDashboard from '@/components/ResultsDashboard'
import MusicPlayer from '@/components/MusicPlayer'
import { optimizeResume } from '@/lib/api'
import toast from 'react-hot-toast'

export default function Home() {
  const [step, setStep] = useState(1)
  const [inputMethod, setInputMethod] = useState<'file' | 'latex'>('file') // NEW: Track input method
  const [resumeFile, setResumeFile] = useState<File | null>(null)
  const [latexCode, setLatexCode] = useState('') // NEW: Store LaTeX code
  const [jobData, setJobData] = useState({
    job_title: '',
    company_name: '',
    description: ''
  })
  const [results, setResults] = useState<any>(null)
  const [isLoading, setIsLoading] = useState(false)

  // Handle resume upload
  const handleResumeUpload = (file: File) => {
    setResumeFile(file)
    toast.success('Resume uploaded! Now add the job details.')
    setStep(2)
  }

  // NEW: Handle LaTeX paste
  const handleLatexPaste = () => {
    if (latexCode.trim().length < 100) {
      toast.error('Please paste your LaTeX code (at least 100 characters)')
      return
    }
    toast.success('LaTeX code ready! Now add the job details.')
    setStep(2)
  }

  // Handle job form submission and kick off optimization
  const handleJobSubmit = async (data: any) => {
    setJobData(data)
    setIsLoading(true)

    try {
      // Call the API to optimize resume (supports both file and LaTeX)
      const result = await optimizeResume(
        inputMethod === 'file' ? resumeFile! : null,
        data,
        inputMethod === 'latex' ? latexCode : undefined
      )
      setResults(result)
      setStep(3)
      toast.success('Resume optimized successfully! 🎉')
    } catch (error: any) {
      toast.error(error.message || 'Something went wrong. Please try again.')
      console.error('Optimization error:', error)
    } finally {
      setIsLoading(false)
    }
  }

  // Start over
  const handleReset = () => {
    setStep(1)
    setInputMethod('file')
    setResumeFile(null)
    setLatexCode('')
    setJobData({ job_title: '', company_name: '', description: '' })
    setResults(null)
  }

  return (
    <div className="min-h-screen bg-white">
      {/* Music Player - Top Right */}
      <MusicPlayer />
      
      {/* Header - Apple style */}
      <header className="glass border-b border-gray-100 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-9 h-9 bg-primary-900 rounded-[10px] flex items-center justify-center">
                <Sparkles className="w-5 h-5 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-semibold text-primary-900 tracking-tight">Applytune</h1>
                <p className="text-[10px] text-gray-500 tracking-wide">Fine-Tune Every Application</p>
              </div>
            </div>
            
            {/* Step indicator - Apple style */}
            <div className="hidden md:flex items-center space-x-1.5">
              {[1, 2, 3].map((s) => (
                <div key={s} className="flex items-center">
                  <div className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-medium transition-all duration-300 ${
                    step >= s 
                      ? 'bg-primary-900 text-white shadow-apple' 
                      : 'bg-gray-100 text-gray-400'
                  }`}>
                    {s}
                  </div>
                  {s < 3 && (
                    <div className={`w-10 h-0.5 mx-1 rounded-full transition-all duration-300 ${
                      step > s ? 'bg-primary-900' : 'bg-gray-200'
                    }`} />
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      </header>

      {/* Main content - Apple style spacing */}
      <main className="max-w-6xl mx-auto px-6 lg:px-8 py-16">
        
        {/* Hero section - Apple minimalist */}
        {step === 1 && !resumeFile && (
          <div className="text-center mb-20 animate-fade-in">
            <h2 className="text-hero font-semibold text-primary-900 mb-6 tracking-tight leading-tight">
              Land more interviews with<br />
              <span className="text-gray-600">AI-optimized resumes</span>
            </h2>
            <p className="text-xl text-gray-500 max-w-2xl mx-auto mb-12 font-light leading-relaxed">
              Fine-tune your resume for every job. Based on research from<br />
              Workday, Taleo, and Greenhouse ATS systems.
            </p>
            
            {/* Feature cards - Apple style */}
            <div className="grid md:grid-cols-3 gap-4 max-w-4xl mx-auto mb-16">
              {[
                {
                  icon: <FileUp className="w-6 h-6" />,
                  title: 'Upload Resume',
                  desc: 'PDF or DOCX'
                },
                {
                  icon: <Sparkles className="w-6 h-6" />,
                  title: 'AI Optimization',
                  desc: 'GPT-4 powered'
                },
                {
                  icon: <TrendingUp className="w-6 h-6" />,
                  title: 'Higher Score',
                  desc: '+27% average'
                }
              ].map((feature, i) => (
                <div key={i} className="bg-gray-50/50 p-8 rounded-2xl border border-gray-100 card-hover">
                  <div className="text-primary-900 mb-4">{feature.icon}</div>
                  <h3 className="font-medium text-primary-900 mb-1.5 text-base tracking-tight">{feature.title}</h3>
                  <p className="text-sm text-gray-500 font-light">{feature.desc}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Step 1: Choose Input Method */}
        {step === 1 && (
          <div className="max-w-3xl mx-auto animate-slide-up">
            {/* Tabs - Apple style */}
            <div className="flex justify-center mb-8">
              <div className="inline-flex bg-gray-100 rounded-2xl p-1">
                <button
                  onClick={() => setInputMethod('file')}
                  className={`px-6 py-2.5 rounded-xl font-medium text-sm transition-all duration-200 ${
                    inputMethod === 'file'
                      ? 'bg-white text-primary-900 shadow-apple'
                      : 'text-gray-600 hover:text-primary-900'
                  }`}
                >
                  📄 Upload File
                </button>
                <button
                  onClick={() => setInputMethod('latex')}
                  className={`px-6 py-2.5 rounded-xl font-medium text-sm transition-all duration-200 ${
                    inputMethod === 'latex'
                      ? 'bg-white text-primary-900 shadow-apple'
                      : 'text-gray-600 hover:text-primary-900'
                  }`}
                >
                  📋 Paste LaTeX
                </button>
              </div>
            </div>

            {/* File Upload Tab */}
            {inputMethod === 'file' && (
              <FileUploader onUpload={handleResumeUpload} />
            )}

            {/* LaTeX Paste Tab */}
            {inputMethod === 'latex' && (
              <div className="bg-white rounded-3xl border border-gray-200 p-8 shadow-apple">
                <div className="mb-4">
                  <h3 className="text-xl font-semibold text-primary-900 mb-2">
                    🎓 Paste Your LaTeX Code
                  </h3>
                  <p className="text-sm text-gray-600 font-light">
                    Copy your entire LaTeX resume from Overleaf and paste it here
                  </p>
                </div>

                <textarea
                  value={latexCode}
                  onChange={(e) => setLatexCode(e.target.value)}
                  placeholder="\documentclass[letterpaper,11pt]{article}&#10;\usepackage{latexsym}&#10;&#10;\begin{document}&#10;&#10;\section{Experience}&#10;\item Developed APIs...&#10;&#10;\end{document}"
                  className="w-full h-96 px-4 py-3 border border-gray-200 rounded-2xl font-mono text-sm resize-none focus:outline-none focus:ring-2 focus:ring-primary-900/20 focus:border-primary-900"
                  style={{ fontFamily: 'Monaco, Consolas, monospace' }}
                />

                <div className="mt-6 flex items-center justify-between">
                  <p className="text-xs text-gray-500">
                    {latexCode.length} characters • Perfect preservation guaranteed ✨
                  </p>
                  <button
                    onClick={handleLatexPaste}
                    disabled={latexCode.trim().length < 100}
                    className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Continue →
                  </button>
                </div>

                <div className="mt-6 pt-6 border-t border-gray-100">
                  <p className="text-xs text-gray-400 font-light mb-3 tracking-wide">HOW TO GET YOUR LATEX CODE</p>
                  <ol className="text-xs text-gray-600 space-y-2 font-light">
                    <li>1. Open your resume in Overleaf</li>
                    <li>2. Select all text (Cmd/Ctrl + A)</li>
                    <li>3. Copy (Cmd/Ctrl + C)</li>
                    <li>4. Paste here</li>
                  </ol>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Step 2: Job Description */}
        {step === 2 && !isLoading && (
          <div className="max-w-3xl mx-auto animate-slide-up">
            <div className="mb-6">
              <div className="flex items-center space-x-2 text-sm text-gray-600 mb-4">
                <CheckCircle2 className="w-5 h-5 text-green-500" />
                <span>
                  {inputMethod === 'file' 
                    ? `Resume uploaded: ${resumeFile?.name}`
                    : `LaTeX code ready (${latexCode.length} characters)`
                  }
                </span>
                <button 
                  onClick={() => setStep(1)} 
                  className="text-blue-500 hover:text-blue-600 ml-2"
                >
                  Change
                </button>
              </div>
            </div>
            <JobDescriptionForm onSubmit={handleJobSubmit} />
          </div>
        )}

        {/* Loading state */}
        {isLoading && (
          <div className="max-w-2xl mx-auto text-center py-20">
            <div className="inline-block w-16 h-16 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mb-6"></div>
            <h3 className="text-2xl font-semibold text-gray-900 mb-2">Optimizing Your Resume...</h3>
            <p className="text-gray-600 mb-4">This usually takes 15-30 seconds</p>
            <div className="max-w-md mx-auto space-y-2 text-sm text-gray-500">
              <p className="flex items-center justify-center">
                <span className="w-2 h-2 bg-blue-500 rounded-full mr-2 animate-pulse"></span>
                Analyzing job requirements
              </p>
              <p className="flex items-center justify-center">
                <span className="w-2 h-2 bg-purple-500 rounded-full mr-2 animate-pulse"></span>
                Extracting keywords
              </p>
              <p className="flex items-center justify-center">
                <span className="w-2 h-2 bg-green-500 rounded-full mr-2 animate-pulse"></span>
                Rewriting with AI
              </p>
            </div>
          </div>
        )}

        {/* Step 3: Results */}
        {step === 3 && results && (
          <div className="animate-slide-up">
            <ResultsDashboard 
              results={results}
              onStartOver={handleReset}
            />
          </div>
        )}

      </main>

      {/* Footer - Apple minimalist */}
      <footer className="border-t border-gray-100 mt-24">
        <div className="max-w-6xl mx-auto px-6 lg:px-8 py-12">
          <div className="text-center">
            <p className="text-xs text-gray-400 mb-2 font-light">
              Scoring methodology based on documented criteria from Workday, Taleo, and Greenhouse ATS systems.
            </p>
            <p className="text-xs text-gray-300 font-light">
              Built for job seekers. Not affiliated with any ATS provider.
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}
