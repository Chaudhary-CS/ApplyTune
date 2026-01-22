'use client'

import { CheckCircle2, XCircle, Search } from 'lucide-react'
import { useState } from 'react'

interface KeywordListProps {
  matched: string[]
  missing: string[]
}

export default function KeywordList({ matched, missing }: KeywordListProps) {
  const [searchTerm, setSearchTerm] = useState('')

  // Filter keywords based on search
  const filteredMatched = matched.filter(kw => 
    kw.toLowerCase().includes(searchTerm.toLowerCase())
  )
  const filteredMissing = missing.filter(kw => 
    kw.toLowerCase().includes(searchTerm.toLowerCase())
  )

  return (
    <div className="space-y-6">
      <div>
        <h3 className="font-semibold text-gray-900 text-lg mb-2">Keyword Analysis</h3>
        <p className="text-sm text-gray-600">
          Keywords found in your optimized resume vs. what's still missing from the job description.
        </p>
      </div>

      {/* Search */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
        <input
          type="text"
          placeholder="Search keywords..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 gap-4">
        <div className="bg-green-50 border border-green-200 rounded-lg p-4 text-center">
          <div className="text-3xl font-bold text-green-600">{matched.length}</div>
          <div className="text-sm text-green-700 mt-1">Keywords Matched</div>
        </div>
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-center">
          <div className="text-3xl font-bold text-red-600">{missing.length}</div>
          <div className="text-sm text-red-700 mt-1">Keywords Missing</div>
        </div>
      </div>

      {/* Matched Keywords */}
      <div>
        <h4 className="font-medium text-gray-900 mb-3 flex items-center">
          <CheckCircle2 className="w-5 h-5 text-green-600 mr-2" />
          Matched Keywords ({filteredMatched.length})
        </h4>
        <div className="flex flex-wrap gap-2">
          {filteredMatched.length > 0 ? (
            filteredMatched.map((keyword, i) => (
              <span
                key={i}
                className="inline-flex items-center space-x-1 px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm"
              >
                <CheckCircle2 className="w-3 h-3" />
                <span>{keyword}</span>
              </span>
            ))
          ) : (
            <p className="text-sm text-gray-500 italic">
              {searchTerm ? 'No matched keywords found for your search' : 'No matched keywords'}
            </p>
          )}
        </div>
      </div>

      {/* Missing Keywords */}
      <div>
        <h4 className="font-medium text-gray-900 mb-3 flex items-center">
          <XCircle className="w-5 h-5 text-red-600 mr-2" />
          Missing Keywords ({filteredMissing.length})
        </h4>
        {filteredMissing.length > 0 ? (
          <>
            <div className="flex flex-wrap gap-2 mb-3">
              {filteredMissing.slice(0, 20).map((keyword, i) => (
                <span
                  key={i}
                  className="inline-flex items-center space-x-1 px-3 py-1 bg-red-100 text-red-800 rounded-full text-sm"
                >
                  <XCircle className="w-3 h-3" />
                  <span>{keyword}</span>
                </span>
              ))}
            </div>
            <div className="p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
              <p className="text-xs text-yellow-900">
                <strong>Tip:</strong> Consider adding these keywords to your resume if they accurately
                represent your skills and experience. Don't add keywords you don't actually have!
              </p>
            </div>
          </>
        ) : (
          <p className="text-sm text-gray-500 italic">
            {searchTerm ? 'No missing keywords found for your search' : 'Great! Your resume includes all major keywords.'}
          </p>
        )}
      </div>
    </div>
  )
}
