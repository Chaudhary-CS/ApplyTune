'use client'

import React, { useState, useMemo } from 'react'
import { ResumeChange, ChangePreview } from '../lib/api'

interface DiffViewerProps {
  changePreview: ChangePreview
  onToggleChange?: (changeId: string, accepted: boolean) => void
}

/**
 * Real-Time ATS Preview Component
 * 
 * THE UX GAME-CHANGER! Shows every single modification side-by-side.
 * User can accept/reject individual changes and see live ATS impact.
 * 
 * This is what competitors charge $50/month for!
 */
export default function DiffViewer({ changePreview, onToggleChange }: DiffViewerProps) {
  const [selectedChanges, setSelectedChanges] = useState<Set<string>>(
    new Set(changePreview.changes.filter(c => c.status === 'accepted').map(c => c.id))
  )
  
  // Group changes by section
  const groupedChanges = useMemo(() => {
    const groups: Record<string, ResumeChange[]> = {}
    changePreview.changes.forEach(change => {
      if (!groups[change.section]) {
        groups[change.section] = []
      }
      groups[change.section].push(change)
    })
    return groups
  }, [changePreview.changes])
  
  // Calculate live ATS score based on selected changes
  const liveATSImpact = useMemo(() => {
    return changePreview.changes
      .filter(c => selectedChanges.has(c.id))
      .reduce((sum, c) => sum + c.ats_impact, 0)
  }, [selectedChanges, changePreview.changes])
  
  const toggleChange = (changeId: string) => {
    const newSelected = new Set(selectedChanges)
    if (newSelected.has(changeId)) {
      newSelected.delete(changeId)
    } else {
      newSelected.add(changeId)
    }
    setSelectedChanges(newSelected)
    
    if (onToggleChange) {
      onToggleChange(changeId, newSelected.has(changeId))
    }
  }
  
  const getChangeTypeColor = (type: ResumeChange['type']) => {
    switch (type) {
      case 'keyword_added':
        return 'bg-blue-50 border-blue-200 text-blue-700'
      case 'skill_added':
        return 'bg-green-50 border-green-200 text-green-700'
      case 'skill_removed':
        return 'bg-red-50 border-red-200 text-red-700'
      case 'bullet_modified':
        return 'bg-purple-50 border-purple-200 text-purple-700'
      default:
        return 'bg-gray-50 border-gray-200 text-gray-700'
    }
  }
  
  const getChangeTypeLabel = (type: ResumeChange['type']) => {
    switch (type) {
      case 'keyword_added':
        return 'Keyword Added'
      case 'skill_added':
        return 'Skill Added'
      case 'skill_removed':
        return 'Skill Removed'
      case 'bullet_modified':
        return 'Bullet Modified'
      default:
        return 'Content Enhanced'
    }
  }
  
  // Escape special regex characters
  const escapeRegex = (str: string) => {
    return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
  }
  
  // Highlight keywords in text
  const highlightKeywords = (text: string, keywords: string[]) => {
    if (!keywords.length) return text
    
    let highlighted = text
    keywords.forEach(keyword => {
      const escapedKeyword = escapeRegex(keyword)
      const regex = new RegExp(`(${escapedKeyword})`, 'gi')
      highlighted = highlighted.replace(regex, '<mark class="bg-yellow-200 px-1 rounded">$1</mark>')
    })
    
    return highlighted
  }
  
  if (!changePreview || changePreview.total_changes === 0) {
    return (
      <div className="p-8 text-center text-gray-500">
        <p>No changes to preview</p>
      </div>
    )
  }
  
  return (
    <div className="space-y-6">
      {/* Live Stats Header */}
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-2xl p-6 border border-blue-100">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-xl font-semibold text-gray-900">Real-Time Change Preview</h3>
            <p className="text-sm text-gray-600 mt-1">
              Review and customize your optimization
            </p>
          </div>
          <div className="text-right">
            <div className="text-3xl font-bold text-blue-600">
              +{liveATSImpact.toFixed(1)}%
            </div>
            <div className="text-sm text-gray-600">
              {selectedChanges.size} / {changePreview.accepted} changes applied
            </div>
          </div>
        </div>
      </div>
      
      {/* Summary Cards */}
      <div className="grid grid-cols-3 gap-4">
        <div className="bg-white rounded-xl p-4 border border-gray-200">
          <div className="text-sm text-gray-600">Total Changes</div>
          <div className="text-2xl font-bold text-gray-900 mt-1">
            {changePreview.total_changes}
          </div>
        </div>
        <div className="bg-green-50 rounded-xl p-4 border border-green-200">
          <div className="text-sm text-green-700">Accepted</div>
          <div className="text-2xl font-bold text-green-900 mt-1">
            {changePreview.accepted}
          </div>
        </div>
        <div className="bg-red-50 rounded-xl p-4 border border-red-200">
          <div className="text-sm text-red-700">Rejected</div>
          <div className="text-2xl font-bold text-red-900 mt-1">
            {changePreview.rejected}
          </div>
        </div>
      </div>
      
      {/* Changes by Section */}
      <div className="space-y-6">
        {Object.entries(groupedChanges).map(([section, changes]) => (
          <div key={section} className="bg-white rounded-2xl border border-gray-200 overflow-hidden">
            <div className="bg-gray-50 px-6 py-4 border-b border-gray-200">
              <h4 className="font-semibold text-gray-900">{section}</h4>
              <p className="text-sm text-gray-600 mt-1">
                {changes.length} {changes.length === 1 ? 'change' : 'changes'}
              </p>
            </div>
            
            <div className="divide-y divide-gray-200">
              {changes.map((change) => (
                <div
                  key={change.id}
                  className={`p-6 transition-all ${
                    selectedChanges.has(change.id) ? 'bg-white' : 'bg-gray-50 opacity-60'
                  }`}
                >
                  {/* Change Header */}
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center gap-3">
                      <input
                        type="checkbox"
                        checked={selectedChanges.has(change.id)}
                        onChange={() => toggleChange(change.id)}
                        className="w-5 h-5 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                      />
                      <div>
                        <span className={`inline-block px-3 py-1 rounded-full text-xs font-medium border ${getChangeTypeColor(change.type)}`}>
                          {getChangeTypeLabel(change.type)}
                        </span>
                        {change.keywords_added.length > 0 && (
                          <span className="ml-2 text-sm text-gray-600">
                            Keywords: {change.keywords_added.join(', ')}
                          </span>
                        )}
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-lg font-semibold text-blue-600">
                        +{change.ats_impact.toFixed(1)}%
                      </div>
                      <div className="text-xs text-gray-500">ATS Impact</div>
                    </div>
                  </div>
                  
                  {/* Change Reason */}
                  <div className="mb-4">
                    <p className="text-sm text-gray-700">
                      <span className="font-medium">Why:</span> {change.reason}
                    </p>
                    {change.validation_warnings.length > 0 && (
                      <div className="mt-2 bg-yellow-50 border border-yellow-200 rounded-lg p-3">
                        <p className="text-xs font-medium text-yellow-800">Validation Warnings:</p>
                        <ul className="text-xs text-yellow-700 mt-1 list-disc list-inside">
                          {change.validation_warnings.map((warning, idx) => (
                            <li key={idx}>{warning}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                  
                  {/* Split Screen Diff */}
                  <div className="grid grid-cols-2 gap-4">
                    {/* Original */}
                    <div className="bg-red-50 rounded-lg p-4 border border-red-200">
                      <div className="text-xs font-semibold text-red-800 mb-2 flex items-center gap-2">
                        <span className="w-2 h-2 bg-red-500 rounded-full"></span>
                        ORIGINAL
                      </div>
                      <div className="text-sm text-gray-900 font-mono">
                        {change.original_text || <span className="text-gray-400 italic">(empty)</span>}
                      </div>
                    </div>
                    
                    {/* Modified */}
                    <div className="bg-green-50 rounded-lg p-4 border border-green-200">
                      <div className="text-xs font-semibold text-green-800 mb-2 flex items-center gap-2">
                        <span className="w-2 h-2 bg-green-500 rounded-full"></span>
                        OPTIMIZED
                      </div>
                      <div
                        className="text-sm text-gray-900 font-mono"
                        dangerouslySetInnerHTML={{
                          __html: highlightKeywords(change.modified_text, change.keywords_added)
                        }}
                      />
                    </div>
                  </div>
                  
                  {/* Validation Status */}
                  <div className="mt-4 flex items-center gap-2 text-xs text-gray-600">
                    <svg className="w-4 h-4 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                    <span>
                      Validation: {change.validation_layers_passed.join(' → ')}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
