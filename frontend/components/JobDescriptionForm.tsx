'use client'

import { useState } from 'react'
import { Briefcase, Building2, FileText, ArrowRight } from 'lucide-react'

interface JobDescriptionFormProps {
  onSubmit: (data: any) => void
}

export default function JobDescriptionForm({ onSubmit }: JobDescriptionFormProps) {
  const [formData, setFormData] = useState({
    job_title: '',
    company_name: '',
    description: ''
  })

  const [errors, setErrors] = useState<Record<string, string>>({})

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()

    // Validate
    const newErrors: Record<string, string> = {}
    
    if (!formData.job_title.trim()) {
      newErrors.job_title = 'Job title is required'
    }
    
    if (!formData.company_name.trim()) {
      newErrors.company_name = 'Company name is required'
    }
    
    if (!formData.description.trim()) {
      newErrors.description = 'Job description is required'
    } else if (formData.description.trim().split(' ').length < 50) {
      newErrors.description = 'Please provide a more detailed job description (at least 50 words)'
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors)
      return
    }

    // Submit
    onSubmit(formData)
  }

  const handleChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }))
    // Clear error for this field
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: '' }))
    }
  }

  return (
    <div className="bg-white rounded-3xl shadow-apple-lg border border-gray-100 p-10">
      <div className="mb-8">
        <h2 className="text-display font-semibold text-primary-900 mb-3 tracking-tight">Job details</h2>
        <p className="text-gray-500 font-light leading-relaxed">
          Paste the job posting you're applying to. More details lead to better optimization.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Job Title */}
        <div>
          <label htmlFor="job_title" className="block text-xs font-medium text-gray-500 mb-3 tracking-wide">
            JOB TITLE *
          </label>
          <input
            id="job_title"
            type="text"
            value={formData.job_title}
            onChange={(e) => handleChange('job_title', e.target.value)}
            placeholder="e.g., Senior Software Engineer"
            className={`
              w-full px-4 py-3.5 rounded-xl border bg-white text-primary-900
              focus:ring-2 focus:ring-primary-900 focus:border-transparent
              transition-all duration-300
              placeholder:text-gray-400 font-light
              ${errors.job_title ? 'border-red-300' : 'border-gray-200 hover:border-gray-300'}
            `}
          />
          {errors.job_title && (
            <p className="mt-2 text-xs text-red-600 font-light">{errors.job_title}</p>
          )}
        </div>

        {/* Company Name */}
        <div>
          <label htmlFor="company_name" className="block text-xs font-medium text-gray-500 mb-3 tracking-wide">
            COMPANY NAME *
          </label>
          <input
            id="company_name"
            type="text"
            value={formData.company_name}
            onChange={(e) => handleChange('company_name', e.target.value)}
            placeholder="e.g., Apple"
            className={`
              w-full px-4 py-3.5 rounded-xl border bg-white text-primary-900
              focus:ring-2 focus:ring-primary-900 focus:border-transparent
              transition-all duration-300
              placeholder:text-gray-400 font-light
              ${errors.company_name ? 'border-red-300' : 'border-gray-200 hover:border-gray-300'}
            `}
          />
          {errors.company_name && (
            <p className="mt-2 text-xs text-red-600 font-light">{errors.company_name}</p>
          )}
        </div>

        {/* Job Description */}
        <div>
          <label htmlFor="description" className="block text-xs font-medium text-gray-500 mb-3 tracking-wide">
            JOB DESCRIPTION *
          </label>
          <textarea
            id="description"
            value={formData.description}
            onChange={(e) => handleChange('description', e.target.value)}
            placeholder="Paste the full job description including requirements, responsibilities, and qualifications..."
            rows={14}
            className={`
              w-full px-4 py-3.5 rounded-xl border bg-white text-primary-900
              focus:ring-2 focus:ring-primary-900 focus:border-transparent
              transition-all duration-300 resize-none
              placeholder:text-gray-400 font-light leading-relaxed
              ${errors.description ? 'border-red-300' : 'border-gray-200 hover:border-gray-300'}
            `}
          />
          <div className="flex justify-between items-center mt-3">
            {errors.description ? (
              <p className="text-xs text-red-600 font-light">{errors.description}</p>
            ) : (
              <p className="text-xs text-gray-400 font-light">
                {formData.description.trim().split(/\s+/).filter(w => w).length} words
                {' '}· Aim for 50+ words
              </p>
            )}
          </div>
        </div>

        {/* Tips */}
        <div className="bg-gray-50/50 border border-gray-100 rounded-2xl p-5">
          <p className="text-xs font-medium text-gray-500 mb-3 tracking-wide">PRO TIPS</p>
          <ul className="text-xs text-gray-600 space-y-2 font-light">
            <li>• Include the entire job posting, not just a summary</li>
            <li>• Make sure to include requirements and qualifications sections</li>
            <li>• More keywords lead to better optimization</li>
          </ul>
        </div>

        {/* Submit Button - Apple style */}
        <button
          type="submit"
          className="
            w-full py-4 px-6 bg-primary-900 hover:bg-primary-800
            text-white font-medium rounded-full
            flex items-center justify-center space-x-2
            transition-all duration-300 transform hover:scale-[1.01]
            shadow-apple-lg hover:shadow-apple-xl
            tracking-tight
          "
        >
          <span>Optimize Resume</span>
          <ArrowRight className="w-5 h-5" />
        </button>
      </form>
    </div>
  )
}
