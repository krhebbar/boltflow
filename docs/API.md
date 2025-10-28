# Boltflow API Documentation

## Base URL

```
Development: http://localhost:8000
Production:  https://api.boltflow.dev
```

## Authentication

Currently, the API is open for development. In production, implement API key authentication:

```bash
curl -H "Authorization: Bearer YOUR_API_KEY" https://api.boltflow.dev/api/scraper/start
```

## API Endpoints

### 1. Web Scraper API

#### Start Scraping Job

```http
POST /api/scraper/start
```

**Request Body:**
```json
{
  "url": "https://example.com",
  "max_pages": 10,
  "screenshot": true,
  "extract_styles": true
}
```

**Response:**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "started",
  "message": "Scraping job started successfully"
}
```

**Status Codes:**
- `200` - Job started successfully
- `400` - Invalid request parameters
- `500` - Server error

#### Get Scraper Status

```http
GET /api/scraper/status/{job_id}
```

**Response:**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "in_progress",
  "progress": {
    "pages_scraped": 5,
    "total_pages": 10,
    "current_url": "https://example.com/about",
    "percentage": 50
  }
}
```

**Status Values:**
- `pending` - Job queued
- `in_progress` - Currently scraping
- `completed` - Finished successfully
- `failed` - Error occurred

#### Get Scraped Data

```http
GET /api/scraper/results/{job_id}
```

**Response:**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "pages": [
    {
      "url": "https://example.com",
      "html": "<html>...</html>",
      "css": "body { margin: 0; }",
      "screenshot": "data:image/png;base64,...",
      "metadata": {
        "title": "Example Site",
        "description": "...",
        "scraped_at": "2024-01-15T10:30:00Z"
      }
    }
  ],
  "statistics": {
    "total_pages": 10,
    "total_size_bytes": 1048576,
    "scrape_duration_seconds": 45.2
  }
}
```

---

### 2. Analyzer API

#### Analyze Page Structure

```http
POST /api/analyzer/analyze
```

**Request Body:**
```json
{
  "html": "<html>...</html>",
  "css": "body { margin: 0; }",
  "url": "https://example.com"
}
```

**Response:**
```json
{
  "structure": {
    "header": {
      "type": "header",
      "confidence": 0.95,
      "html": "<header>...</header>",
      "description": "Main navigation header with logo and menu"
    },
    "sections": [
      {
        "type": "hero",
        "confidence": 0.92,
        "html": "<section class='hero'>...</section>",
        "description": "Hero section with headline and CTA"
      },
      {
        "type": "features",
        "confidence": 0.88,
        "html": "<section class='features'>...</section>",
        "description": "Three-column feature showcase"
      }
    ],
    "footer": {
      "type": "footer",
      "confidence": 0.96,
      "html": "<footer>...</footer>",
      "description": "Footer with links and social media"
    }
  },
  "components": [
    {
      "id": "comp_001",
      "name": "NavigationHeader",
      "type": "header",
      "props": ["logo", "menuItems"],
      "complexity": "medium"
    }
  ],
  "design_tokens": {
    "colors": {
      "primary": "#3b82f6",
      "secondary": "#8b5cf6",
      "background": "#ffffff"
    },
    "typography": {
      "headings": "Inter, sans-serif",
      "body": "system-ui, sans-serif"
    },
    "spacing": {
      "container": "1280px",
      "padding": "1rem"
    }
  }
}
```

#### Get Pricing Quote

```http
POST /api/analyzer/quote
```

**Request Body:**
```json
{
  "html": "<html>...</html>",
  "css": "body { margin: 0; }",
  "url": "https://example.com"
}
```

**Response:**
```json
{
  "analysis": {
    "total_components": 12,
    "complexity_score": 7.5,
    "estimated_hours": 24
  },
  "pricing": {
    "total_cost": 2400,
    "currency": "USD",
    "breakdown": {
      "scraping": 100,
      "component_generation": 1800,
      "cms_integration": 300,
      "deployment": 200
    }
  },
  "timeline": {
    "estimated_days": 3,
    "completion_date": "2024-01-18"
  }
}
```

---

### 3. Generator API

#### Generate Code

```http
POST /api/generator/generate
```

**Request Body:**
```json
{
  "components": [
    {
      "id": "comp_001",
      "name": "Header",
      "type": "header",
      "html": "<header>...</header>",
      "css": ".header { ... }"
    }
  ],
  "ui_library": "shadcn",
  "typescript": true,
  "framework": "nextjs"
}
```

**Response:**
```json
{
  "files": [
    {
      "path": "components/Header.tsx",
      "content": "import { Button } from '@/components/ui/button'\n\nexport default function Header() {\n  return (\n    <header>...</header>\n  )\n}",
      "type": "component"
    },
    {
      "path": "app/page.tsx",
      "content": "import Header from '@/components/Header'\n\nexport default function Home() {\n  return (<main>...</main>)\n}",
      "type": "page"
    }
  ],
  "project_structure": {
    "framework": "nextjs",
    "ui_library": "shadcn",
    "total_files": 12,
    "components": 8,
    "pages": 3
  }
}
```

#### Generate Preview

```http
POST /api/generator/preview
```

**Request Body:**
```json
{
  "component_id": "comp_001",
  "props": {
    "variant": "default",
    "children": "Click me"
  }
}
```

**Response:**
```json
{
  "html": "<div>...</div>",
  "preview_url": "https://preview.boltflow.dev/comp_001"
}
```

---

### 4. CMS Integration API

#### List Available Providers

```http
GET /api/cms/providers
```

**Response:**
```json
{
  "providers": [
    {
      "name": "supabase",
      "display_name": "Supabase",
      "features": ["GraphQL", "Realtime", "Auth", "Storage"],
      "pricing": "Free tier available"
    },
    {
      "name": "sanity",
      "display_name": "Sanity.io",
      "features": ["Structured Content", "GROQ", "Real-time"],
      "pricing": "Free for development"
    },
    {
      "name": "hygraph",
      "display_name": "Hygraph",
      "features": ["GraphQL", "Multi-region", "Asset delivery"],
      "pricing": "Free tier available"
    },
    {
      "name": "strapi",
      "display_name": "Strapi",
      "features": ["Self-hosted", "REST & GraphQL", "Plugins"],
      "pricing": "Open source"
    }
  ]
}
```

#### Connect to CMS

```http
POST /api/cms/connect
```

**Request Body:**
```json
{
  "provider": "supabase",
  "credentials": {
    "url": "https://project.supabase.co",
    "key": "your-anon-key"
  },
  "project_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response:**
```json
{
  "connection_id": "conn_001",
  "provider": "supabase",
  "status": "connected",
  "features_enabled": ["content", "auth", "storage"]
}
```

#### Create Content Schema

```http
POST /api/cms/schema
```

**Request Body:**
```json
{
  "connection_id": "conn_001",
  "schema": {
    "collections": [
      {
        "name": "pages",
        "fields": [
          { "name": "title", "type": "string", "required": true },
          { "name": "content", "type": "richtext" },
          { "name": "slug", "type": "slug", "unique": true }
        ]
      }
    ]
  }
}
```

**Response:**
```json
{
  "schema_id": "schema_001",
  "status": "created",
  "collections_created": 1,
  "graphql_endpoint": "https://project.supabase.co/graphql/v1"
}
```

---

### 5. WebSocket API

#### Connection

```javascript
const socket = io('ws://localhost:8000')

socket.on('connect', () => {
  console.log('Connected to Boltflow')
})
```

#### Events

**Client → Server:**
```javascript
// Subscribe to job updates
socket.emit('subscribe', { job_id: '550e8400-...' })
```

**Server → Client:**
```javascript
// Progress update
socket.on('progress', (data) => {
  console.log(data)
  // {
  //   job_id: '550e8400-...',
  //   stage: 'scraping',
  //   progress: 50,
  //   message: 'Scraped 5 of 10 pages'
  // }
})

// Job completed
socket.on('completed', (data) => {
  console.log(data)
  // {
  //   job_id: '550e8400-...',
  //   status: 'completed',
  //   results_url: '/api/scraper/results/550e8400-...'
  // }
})

// Error occurred
socket.on('error', (data) => {
  console.error(data)
  // {
  //   job_id: '550e8400-...',
  //   error: 'Failed to scrape page',
  //   details: '...'
  // }
})
```

---

## Rate Limiting

Current limits (subject to change):
- **Scraping:** 10 jobs per hour per IP
- **Analysis:** 100 requests per hour
- **Code Generation:** 50 requests per hour

Exceeding limits returns `429 Too Many Requests`.

---

## Error Responses

All errors follow this format:

```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "URL is required",
    "details": {
      "field": "url",
      "validation": "required"
    }
  }
}
```

**Common Error Codes:**
- `INVALID_REQUEST` - Malformed request
- `RESOURCE_NOT_FOUND` - Job/resource doesn't exist
- `RATE_LIMIT_EXCEEDED` - Too many requests
- `INTERNAL_ERROR` - Server error
- `EXTERNAL_SERVICE_ERROR` - Third-party API error

---

## Interactive Documentation

Visit `/docs` on the API server for interactive Swagger UI documentation:

```
http://localhost:8000/docs
```

## SDK Support

Official SDKs (coming soon):
- TypeScript/JavaScript
- Python
- Go

For now, use standard HTTP clients:

```typescript
// TypeScript example
const response = await fetch('http://localhost:8000/api/scraper/start', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    url: 'https://example.com',
    max_pages: 10,
    screenshot: true
  })
})

const data = await response.json()
console.log(data.job_id)
```
