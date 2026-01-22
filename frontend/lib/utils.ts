import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

/**
 * Utility to merge Tailwind classes
 * Useful for conditional styling
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

/**
 * Format a score as a percentage with color
 */
export function getScoreColor(score: number): string {
  if (score >= 80) return 'text-green-600'
  if (score >= 70) return 'text-yellow-600'
  if (score >= 60) return 'text-orange-600'
  return 'text-red-600'
}

/**
 * Get score background color
 */
export function getScoreBgColor(score: number): string {
  if (score >= 80) return 'bg-green-100'
  if (score >= 70) return 'bg-yellow-100'
  if (score >= 60) return 'bg-orange-100'
  return 'bg-red-100'
}

/**
 * Get score label
 */
export function getScoreLabel(score: number): string {
  if (score >= 85) return 'Excellent'
  if (score >= 75) return 'Good'
  if (score >= 65) return 'Fair'
  if (score >= 50) return 'Needs Work'
  return 'Poor'
}

/**
 * Truncate text
 */
export function truncate(text: string, length: number): string {
  if (text.length <= length) return text
  return text.slice(0, length) + '...'
}

/**
 * Format date
 */
export function formatDate(date: Date): string {
  return new Intl.DateTimeFormat('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  }).format(date)
}
