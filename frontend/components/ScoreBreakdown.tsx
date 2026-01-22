'use client'

import { Info } from 'lucide-react'
import { getScoreColor } from '@/lib/utils'

interface ScoreBreakdownProps {
  breakdown: Record<string, any>
}

export default function ScoreBreakdown({ breakdown }: ScoreBreakdownProps) {
  // Convert breakdown object to array for easier rendering
  const components = Object.entries(breakdown).map(([key, data]) => ({
    name: key.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' '),
    ...data
  }))

  return (
    <div className="space-y-6">
      <div>
        <h3 className="font-semibold text-gray-900 text-lg mb-2">How Your Score is Calculated</h3>
        <p className="text-sm text-gray-600">
          Your ATS score is based on multiple factors. Here's the detailed breakdown:
        </p>
      </div>

      {/* Components */}
      <div className="space-y-4">
        {components.map((component, i) => (
          <div key={i} className="bg-gray-50 rounded-lg p-5 border border-gray-200">
            <div className="flex items-start justify-between mb-3">
              <div className="flex-1">
                <div className="flex items-center space-x-2 mb-1">
                  <h4 className="font-semibold text-gray-900">{component.name}</h4>
                  <span className="text-xs text-gray-500 bg-gray-200 px-2 py-1 rounded">
                    Weight: {component.weight}
                  </span>
                </div>
                <p className="text-sm text-gray-600">{component.description}</p>
              </div>
              
              <div className="text-right ml-4">
                <div className={`text-2xl font-bold ${getScoreColor(component.score)}`}>
                  {component.score.toFixed(1)}
                </div>
                <div className="text-xs text-gray-500">/ 100</div>
              </div>
            </div>

            {/* Progress bar */}
            <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
              <div 
                className={`h-full rounded-full transition-all ${
                  component.score >= 80 ? 'bg-green-500' :
                  component.score >= 70 ? 'bg-yellow-500' :
                  component.score >= 60 ? 'bg-orange-500' :
                  'bg-red-500'
                }`}
                style={{ width: `${component.score}%` }}
              />
            </div>
          </div>
        ))}
      </div>

      {/* Explanation */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <div className="flex items-start space-x-3">
          <Info className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
          <div className="text-sm text-blue-900">
            <p className="font-semibold mb-2">About This Scoring</p>
            <p className="mb-2">
              Our scoring methodology is based on documented behavior from major ATS systems:
            </p>
            <ul className="list-disc list-inside space-y-1 text-xs">
              <li>Workday ATS Best Practices Guide (2024)</li>
              <li>Oracle Taleo Resume Optimization Whitepaper</li>
              <li>Greenhouse ATS Documentation</li>
              <li>Jobscan ATS Research Study (5,000+ resumes)</li>
            </ul>
            <p className="mt-2 text-xs">
              While scores are research-based, actual ATS behavior may vary by company configuration.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
