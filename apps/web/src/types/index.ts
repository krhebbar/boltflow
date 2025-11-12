/**
 * Shared TypeScript types for the application
 */

export interface User {
  id: string
  email: string
  name?: string
  created_at?: string
}

export interface Project {
  id: string
  user_id: string
  name: string
  url: string
  status: ProjectStatus
  max_pages: number
  created_at: string
  updated_at: string
}

export type ProjectStatus =
  | 'pending'
  | 'scraping'
  | 'scraped'
  | 'analyzing'
  | 'analyzed'
  | 'generating'
  | 'generated'
  | 'completed'
  | 'failed'

export interface Job {
  id: string
  project_id: string
  type: JobType
  status: JobStatus
  progress: number
  result?: Record<string, unknown>
  error?: string
  created_at: string
  completed_at?: string
}

export type JobType = 'scrape' | 'analyze' | 'generate' | 'deploy'
export type JobStatus = 'pending' | 'running' | 'completed' | 'failed'

export interface WebSocketMessage {
  type: string
  job_id?: string
  project_id?: string
  progress?: unknown
  result?: unknown
  error?: string
}
