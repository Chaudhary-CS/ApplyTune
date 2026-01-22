'use client'

import { useState } from 'react'
import { 
  TrendingUp, Download, RotateCcw, CheckCircle2, XCircle, 
  ArrowRight, Award, Target, Zap, AlertCircle 
} from 'lucide-react'
import { OptimizationResult } from '@/lib/api'
import { getScoreColor, getScoreBgColor, getScoreLabel } from '@/lib/utils'
import ScoreCard from './ScoreCard'
import KeywordList from './KeywordList'
import ScoreBreakdown from './ScoreBreakdown'

interface ResultsDashboardProps {
  results: OptimizationResult
  onStartOver: () => void
}

export default function ResultsDashboard({ results, onStartOver }: ResultsDashboardProps) {
  const [activeTab, setActiveTab] = useState<'overview' | 'keywords' | 'breakdown'>('overview')

  const improvement = results.improvement_percentage

  return (
    <div className="space-y-6">
      {/* Success Banner */}
      <div className="bg-gradient-to-r from-green-500 to-emerald-600 rounded-2xl p-6 text-white shadow-lg">
        <div className="flex items-start justify-between">
          <div className="flex items-start space-x-4">
            <div className="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center">
              <Award className="w-7 h-7" />
            </div>
            <div>
              <h2 className="text-2xl font-bold mb-2">Resume Optimized Successfully! 🎉</h2>
              <p className="text-green-50">
                Your resume score improved by <strong>{improvement.toFixed(1)}%</strong>
                {' '}and is now more likely to pass ATS screening.
              </p>
            </div>
          </div>
          <button
            onClick={onStartOver}
            className="
              flex items-center space-x-2 px-4 py-2 bg-white/20 hover:bg-white/30
              rounded-lg transition-colors text-sm font-medium
            "
          >
            <RotateCcw className="w-4 h-4" />
            <span>Start Over</span>
          </button>
        </div>
      </div>

      {/* Score Comparison - Big numbers! */}
      <div className="grid md:grid-cols-3 gap-6">
        <ScoreCard
          title="Original Score"
          score={results.original_score}
          subtitle="Before optimization"
          icon={<Target className="w-6 h-6" />}
        />
        
        <div className="flex items-center justify-center">
          <div className="flex flex-col items-center">
            <ArrowRight className="w-8 h-8 text-blue-500 mb-2" />
            <div className={`text-2xl font-bold ${improvement > 0 ? 'text-green-600' : 'text-gray-600'}`}>
              {improvement > 0 ? '+' : ''}{improvement.toFixed(1)}%
            </div>
            <div className="text-sm text-gray-600">Improvement</div>
          </div>
        </div>

        <ScoreCard
          title="Optimized Score"
          score={results.optimized_score}
          subtitle="After AI optimization"
          icon={<Zap className="w-6 h-6" />}
          highlighted
        />
      </div>

      {/* Multi-ATS Scores */}
      <div className="bg-white rounded-2xl shadow-lg border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <TrendingUp className="w-5 h-5 mr-2 text-blue-500" />
          Score by ATS System
        </h3>
        <p className="text-sm text-gray-600 mb-4">
          Different companies use different ATS systems. Here's how your resume scores with each:
        </p>
        
        <div className="grid md:grid-cols-4 gap-4">
          {Object.entries(results.ats_scores.optimized).map(([ats, score]) => (
            <div key={ats} className="bg-gray-50 rounded-lg p-4 text-center">
              <div className="text-xs font-semibold text-gray-600 uppercase mb-2">
                {ats === 'average' ? 'Average' : ats}
              </div>
              <div className={`text-3xl font-bold ${getScoreColor(score as number)}`}>
                {score}
              </div>
              <div className="text-xs text-gray-500 mt-1">
                {getScoreLabel(score as number)}
              </div>
              {/* Show improvement */}
              {ats !== 'average' && results.ats_scores.original[ats] && (
                <div className="text-xs text-green-600 mt-2 font-medium">
                  +{(score as number - results.ats_scores.original[ats]).toFixed(1)} pts
                </div>
              )}
            </div>
          ))}
        </div>

        <div className="mt-4 p-3 bg-blue-50 rounded-lg border border-blue-200">
          <p className="text-xs text-blue-900">
            <strong>Note:</strong> Workday (30% market share), Taleo (20%), Greenhouse (15%).
            These scores are based on documented behavior from each ATS system.
          </p>
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white rounded-2xl shadow-lg border border-gray-200 overflow-hidden">
        {/* Tab Headers */}
        <div className="flex border-b border-gray-200 bg-gray-50">
          {[
            { id: 'overview', label: 'Overview', icon: <AlertCircle className="w-4 h-4" /> },
            { id: 'keywords', label: 'Keywords', icon: <CheckCircle2 className="w-4 h-4" /> },
            { id: 'breakdown', label: 'Score Breakdown', icon: <TrendingUp className="w-4 h-4" /> },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`
                flex-1 px-6 py-4 font-medium text-sm transition-colors
                flex items-center justify-center space-x-2
                ${activeTab === tab.id 
                  ? 'bg-white text-blue-600 border-b-2 border-blue-600' 
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                }
              `}
            >
              {tab.icon}
              <span>{tab.label}</span>
            </button>
          ))}
        </div>

        {/* Tab Content */}
        <div className="p-6">
          {activeTab === 'overview' && (
            <div className="space-y-4">
              <h3 className="font-semibold text-gray-900 text-lg mb-4">Optimization Summary</h3>
              
              <div className="space-y-3">
                {results.suggestions.map((suggestion, i) => (
                  <div key={i} className="flex items-start space-x-3 p-3 bg-green-50 rounded-lg border border-green-200">
                    <CheckCircle2 className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
                    <p className="text-sm text-gray-700">{suggestion}</p>
                  </div>
                ))}
              </div>

              <div className="mt-6 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                <p className="text-sm font-semibold text-yellow-900 mb-2">⚠️ Important Reminder:</p>
                <p className="text-sm text-yellow-800">
                  Please review all AI-generated changes before submitting. Make sure everything accurately
                  represents your experience and skills. The AI optimizes content but you're responsible
                  for accuracy.
                </p>
              </div>
            </div>
          )}

          {activeTab === 'keywords' && (
            <KeywordList 
              matched={results.matched_keywords}
              missing={results.missing_keywords}
            />
          )}

          {activeTab === 'breakdown' && (
            <ScoreBreakdown breakdown={results.score_breakdown} />
          )}
        </div>
      </div>

      {/* Download Section */}
      <div className="bg-gradient-to-r from-blue-500 to-purple-600 rounded-2xl p-8 text-white shadow-lg">
        <div className="max-w-3xl mx-auto text-center">
          <h3 className="text-2xl font-bold mb-3">Ready to Apply?</h3>
          <p className="text-blue-50 mb-6">
            {results.optimized_resume?.latex_content 
              ? 'Copy your optimized LaTeX code and paste it back into Overleaf.'
              : 'Download your optimized resume and start applying with confidence.'
            }
            {' '}Your ATS score is now <strong>{results.optimized_score.toFixed(1)}/100</strong>!
          </p>
          
          {/* LaTeX Output */}
          {results.optimized_resume?.latex_content && (
            <div className="mb-6 bg-white/10 rounded-xl p-6 text-left">
              <div className="flex items-center justify-between mb-3">
                <div>
                  <p className="text-sm font-semibold">🎓 Your Optimized LaTeX Code is Ready!</p>
                  <p className="text-xs text-white/70 mt-1">
                    {results.optimized_resume.latex_content.length} characters • Full code will be copied
                  </p>
                </div>
                <button
                  onClick={() => {
                    navigator.clipboard.writeText(results.optimized_resume.latex_content)
                    alert('✅ Full LaTeX code copied to clipboard!\n\nNow:\n1. Go to Overleaf\n2. Select All (Cmd/Ctrl+A)\n3. Paste (Cmd/Ctrl+V)\n4. Compile!')
                  }}
                  className="px-6 py-3 bg-white text-blue-600 hover:bg-blue-50 rounded-lg text-sm font-semibold transition-colors shadow-lg"
                >
                  📋 Copy Full Code
                </button>
              </div>
              <div className="bg-black/20 rounded-lg p-4">
                <p className="text-xs text-white/50 mb-2">Preview (first 20 lines):</p>
                <pre className="text-xs overflow-auto max-h-40 font-mono text-left text-white/90">
                  {results.optimized_resume.latex_content.split('\n').slice(0, 20).join('\n')}
                  {results.optimized_resume.latex_content.split('\n').length > 20 && '\n\n... (click "Copy Full Code" to get everything)'}
                </pre>
              </div>
            </div>
          )}
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            {results.optimized_resume?.latex_content ? (
              <button
                onClick={() => {
                  navigator.clipboard.writeText(results.optimized_resume.latex_content)
                  alert('✅ LaTeX code copied! Paste it into Overleaf.')
                }}
                className="
                  flex items-center justify-center space-x-2 px-8 py-4 
                  bg-white text-blue-600 font-semibold rounded-lg
                  hover:bg-blue-50 transition-colors shadow-lg
                "
              >
                <CheckCircle2 className="w-5 h-5" />
                <span>Copy LaTeX Code</span>
              </button>
            ) : (
              <button
                onClick={() => {
                  // TODO: Implement PDF download
                  alert('PDF download feature - would call generatePDF API here')
                }}
                className="
                  flex items-center justify-center space-x-2 px-8 py-4 
                  bg-white text-blue-600 font-semibold rounded-lg
                  hover:bg-blue-50 transition-colors shadow-lg
                "
              >
                <Download className="w-5 h-5" />
                <span>Download Optimized Resume</span>
              </button>
            )}
            
            <button
              onClick={onStartOver}
              className="
                flex items-center justify-center space-x-2 px-8 py-4 
                bg-white/20 text-white font-semibold rounded-lg
                hover:bg-white/30 transition-colors
              "
            >
              <RotateCcw className="w-5 h-5" />
              <span>Optimize Another Resume</span>
            </button>
          </div>
        </div>
      </div>

      {/* Tips */}
      <div className="bg-white rounded-2xl shadow-lg border border-gray-200 p-6">
        <h3 className="font-semibold text-gray-900 mb-4">💡 Next Steps</h3>
        <div className="grid md:grid-cols-2 gap-4">
          {[
            {
              title: 'Review the Changes',
              desc: 'Carefully read through all optimized content to ensure accuracy'
            },
            {
              title: 'Tailor File Name',
              desc: 'Save as "YourName_JobTitle.pdf" for better organization'
            },
            {
              title: 'Update LinkedIn',
              desc: 'Keep your LinkedIn profile consistent with your resume'
            },
            {
              title: 'Prepare Cover Letter',
              desc: 'Use the same keywords in your cover letter for consistency'
            }
          ].map((tip, i) => (
            <div key={i} className="flex items-start space-x-3 p-4 bg-gray-50 rounded-lg">
              <div className="w-6 h-6 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-sm font-bold flex-shrink-0">
                {i + 1}
              </div>
              <div>
                <p className="font-medium text-gray-900 text-sm">{tip.title}</p>
                <p className="text-xs text-gray-600 mt-1">{tip.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
