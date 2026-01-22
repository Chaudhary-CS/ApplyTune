'use client'

import { ReactNode } from 'react'
import { getScoreColor, getScoreBgColor, getScoreLabel } from '@/lib/utils'

interface ScoreCardProps {
  title: string
  score: number
  subtitle?: string
  icon?: ReactNode
  highlighted?: boolean
}

export default function ScoreCard({ 
  title, 
  score, 
  subtitle, 
  icon,
  highlighted = false 
}: ScoreCardProps) {
  return (
    <div className={`
      rounded-2xl p-6 shadow-lg border-2 transition-all
      ${highlighted 
        ? 'bg-gradient-to-br from-blue-50 to-purple-50 border-blue-200' 
        : 'bg-white border-gray-200'
      }
    `}>
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-sm font-medium text-gray-600">{title}</h3>
        {icon && <div className="text-gray-400">{icon}</div>}
      </div>
      
      <div className="space-y-3">
        {/* Big score number */}
        <div className="flex items-end space-x-2">
          <div className={`text-5xl font-bold ${getScoreColor(score)}`}>
            {score.toFixed(1)}
          </div>
          <div className="text-2xl text-gray-400 pb-1">/100</div>
        </div>

        {/* Score label */}
        <div className="flex items-center space-x-2">
          <span className={`
            inline-block px-3 py-1 rounded-full text-xs font-semibold
            ${getScoreBgColor(score)} ${getScoreColor(score)}
          `}>
            {getScoreLabel(score)}
          </span>
        </div>

        {subtitle && (
          <p className="text-xs text-gray-500">{subtitle}</p>
        )}

        {/* Visual bar */}
        <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
          <div 
            className={`h-full rounded-full transition-all duration-1000 ${
              score >= 80 ? 'bg-green-500' :
              score >= 70 ? 'bg-yellow-500' :
              score >= 60 ? 'bg-orange-500' :
              'bg-red-500'
            }`}
            style={{ width: `${score}%` }}
          />
        </div>
      </div>
    </div>
  )
}
