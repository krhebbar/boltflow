/**
 * API client for making authenticated requests to the backend
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export class APIError extends Error {
  constructor(
    message: string,
    public status: number,
    public details?: Record<string, unknown>
  ) {
    super(message)
    this.name = 'APIError'
  }
}

interface RequestOptions extends RequestInit {
  token?: string
}

async function request<T>(
  endpoint: string,
  options: RequestOptions = {}
): Promise<T> {
  const { token, ...fetchOptions } = options

  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...fetchOptions.headers,
  }

  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...fetchOptions,
    headers,
  })

  const data = await response.json()

  if (!response.ok) {
    throw new APIError(
      data.error?.message || 'An error occurred',
      response.status,
      data.error?.details
    )
  }

  return data
}

export const api = {
  // Auth endpoints
  auth: {
    signup: (email: string, password: string, name?: string) =>
      request<{ access_token: string; user: { id: string; email: string; name?: string } }>(
        '/api/auth/signup',
        {
          method: 'POST',
          body: JSON.stringify({ email, password, name }),
        }
      ),

    login: (email: string, password: string) =>
      request<{ access_token: string; user: { id: string; email: string; name?: string } }>(
        '/api/auth/login',
        {
          method: 'POST',
          body: JSON.stringify({ email, password }),
        }
      ),

    me: (token: string) =>
      request<{ id: string; email: string; name?: string; created_at: string }>(
        '/api/auth/me',
        { token }
      ),
  },

  // Scraper endpoints
  scraper: {
    start: (
      data: {
        url: string
        project_name: string
        max_pages?: number
        include_assets?: boolean
        screenshot?: boolean
      },
      token: string
    ) =>
      request<{ job_id: string; project_id: string; status: string; message: string }>(
        '/api/scraper/start',
        {
          method: 'POST',
          body: JSON.stringify(data),
          token,
        }
      ),

    status: (jobId: string, token: string) =>
      request<{
        job_id: string
        status: string
        progress: number
        pages_scraped: number
        total_pages: number
        progress_percentage: number
        error?: string
      }>(`/api/scraper/status/${jobId}`, { token }),
  },

  // Analyzer endpoints
  analyzer: {
    analyze: (data: { html: string; css?: string; url: string }, token: string) =>
      request('/api/analyzer/analyze', {
        method: 'POST',
        body: JSON.stringify(data),
        token,
      }),

    quote: (data: { html: string; css?: string; url: string }, token: string) =>
      request('/api/analyzer/quote', {
        method: 'POST',
        body: JSON.stringify(data),
        token,
      }),
  },

  // Generator endpoints
  generator: {
    generate: (
      data: {
        job_id: string
        components: Array<Record<string, unknown>>
        target_framework?: string
        ui_library?: string
      },
      token: string
    ) =>
      request('/api/generator/generate', {
        method: 'POST',
        body: JSON.stringify(data),
        token,
      }),
  },
}
