# Boltflow Architecture

## Overview

Boltflow is a production-grade AI-driven web migration system that transforms legacy websites into modern Next.js applications with automated component generation, CMS integration, and deployment.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                       Client Layer                          │
│  Next.js 14 (App Router) + React 18 + ShadCN UI           │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  │ REST API / WebSocket
                  │
┌─────────────────▼───────────────────────────────────────────┐
│                  Orchestration Layer                        │
│    FastAPI + WebSocket Manager + BullMQ Job Queue         │
└─────┬───────────┬──────────┬─────────────┬─────────────────┘
      │           │          │             │
      │           │          │             │
┌─────▼────┐ ┌───▼────┐ ┌──▼─────┐  ┌────▼────────┐
│ Scraper  │ │   AI   │ │  Code  │  │    CMS      │
│ Engine   │ │ Analysis│ │Generator│  │ Integration │
└──────────┘ └────────┘ └────────┘  └─────────────┘
```

## Core Components

### 1. Frontend Layer (Next.js 14)

**Location:** `apps/web/`

**Technology Stack:**
- Next.js 14 with App Router
- React 18 with TypeScript
- ShadCN UI (Radix primitives + Tailwind)
- TanStack Query for server state
- Socket.io client for real-time updates

**Key Features:**
- Server-side rendering for optimal performance
- Real-time progress tracking via WebSocket
- Responsive dashboard for project management
- Component preview and code viewer

**File Structure:**
```
apps/web/
├── src/
│   ├── app/              # App Router pages
│   │   ├── dashboard/    # Dashboard pages
│   │   └── page.tsx      # Landing page
│   ├── components/       # React components
│   │   ├── ui/          # ShadCN UI components
│   │   └── dashboard/   # Dashboard-specific
│   └── lib/             # Utilities
└── public/              # Static assets
```

### 2. Backend Layer (FastAPI)

**Location:** `apps/api/`

**Technology Stack:**
- FastAPI (Python 3.11+)
- Playwright for web scraping
- OpenAI GPT-4 for AI analysis
- Redis for caching and job queues
- WebSocket for real-time communication

**Architecture Patterns:**
- Router-based modular design
- Async/await throughout
- Background task processing
- Event-driven WebSocket updates

**File Structure:**
```
apps/api/
├── main.py              # FastAPI app entry
├── routers/             # API endpoints
│   ├── scraper.py      # Web scraping
│   ├── analyzer.py     # AI analysis
│   ├── generator.py    # Code generation
│   └── cms.py          # CMS integration
├── ai/                  # AI modules
│   ├── analyzer.py     # DOM analysis
│   └── classifier.py   # Component classification
├── scrapers/            # Scraping engines
│   └── playwright_scraper.py
└── lib/                 # Utilities
    └── websocket_manager.py
```

### 3. AI Analysis Pipeline

**Flow:**
1. **DOM Analysis** (GPT-4)
   - Extract semantic structure
   - Identify component boundaries
   - Classify sections (header, nav, hero, etc.)

2. **Component Classification** (Embeddings)
   - Generate text embeddings for sections
   - Match against component patterns
   - Calculate similarity scores

3. **Complexity Scoring** (ML Model)
   - Analyze component complexity
   - Estimate development effort
   - Generate pricing quotes

**Models Used:**
- `gpt-4-turbo-preview` for structural analysis
- `text-embedding-ada-002` for semantic similarity
- Custom scoring model for complexity

### 4. Code Generation Engine

**Process:**
1. Parse analyzed component data
2. Select UI library (ShadCN, Material-UI, Chakra)
3. Transform HTML → React JSX
4. Generate TypeScript component files
5. Extract and adapt styles
6. Create project structure

**Output:**
- TypeScript React components
- CSS modules / Tailwind classes
- Next.js page structure
- Type definitions

### 5. CMS Integration Layer

**Supported Providers:**
- **Supabase** - PostgreSQL + Realtime
- **Sanity** - Headless CMS
- **Hygraph** - GraphQL CMS
- **Strapi** - Open-source CMS

**Integration Pattern:**
```typescript
interface CMSProvider {
  connect(credentials: Credentials): Promise<Connection>
  createSchema(components: Component[]): Promise<Schema>
  migrate(data: Data[]): Promise<Result>
}
```

### 6. Real-time Orchestration

**WebSocket Manager:**
- Maintains active client connections
- Broadcasts progress updates
- Handles client reconnection
- Coordinates multi-step workflows

**Job Queue (BullMQ + Redis):**
- Background job processing
- Retry logic for failed tasks
- Progress tracking
- Scheduled tasks

## Data Flow

### Migration Workflow

```
1. User Input
   ├─> URL submission
   └─> Configuration (max pages, UI library, CMS)

2. Web Scraping (Playwright)
   ├─> Crawl website
   ├─> Extract HTML/CSS
   ├─> Capture screenshots
   └─> Broadcast progress via WebSocket

3. AI Analysis (GPT-4 + Embeddings)
   ├─> Analyze DOM structure
   ├─> Classify components
   ├─> Extract design tokens
   └─> Calculate complexity

4. Code Generation
   ├─> Generate React components
   ├─> Create page structure
   ├─> Adapt styles
   └─> Generate types

5. CMS Integration (Optional)
   ├─> Create content schema
   ├─> Migrate content
   └─> Configure API

6. Output
   ├─> Generated code (ZIP download)
   ├─> GitHub repository
   └─> Vercel deployment
```

## Deployment Architecture

### Development
```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Next.js     │────▶│   FastAPI    │────▶│    Redis     │
│  :3000       │     │   :8000      │     │   :6379      │
└──────────────┘     └──────────────┘     └──────────────┘
```

### Production (Docker)
```
┌──────────────────────────────────────────┐
│         Docker Compose                   │
│  ┌────────┐  ┌────────┐  ┌────────┐    │
│  │  Web   │  │  API   │  │ Redis  │    │
│  │ :3000  │  │ :8000  │  │ :6379  │    │
│  └────────┘  └────────┘  └────────┘    │
└──────────────────────────────────────────┘
```

### Cloud Deployment
- **Frontend:** Vercel Edge Network
- **Backend:** Railway / Fly.io
- **Database:** Supabase (PostgreSQL)
- **Cache:** Upstash (Redis)
- **Storage:** Supabase Storage / S3

## Security Considerations

1. **API Security**
   - CORS configuration
   - Rate limiting
   - API key validation
   - Input sanitization

2. **Data Privacy**
   - Scraped data encryption
   - Secure credential storage
   - User data isolation

3. **Code Generation**
   - Safe template rendering
   - Output sanitization
   - Dependency security scanning

## Performance Optimizations

1. **Frontend**
   - Server-side rendering
   - Image optimization
   - Code splitting
   - Edge caching

2. **Backend**
   - Redis caching
   - Background job processing
   - Connection pooling
   - Async operations

3. **AI Pipeline**
   - Prompt optimization
   - Response caching
   - Batch processing
   - Token usage optimization

## Monitoring & Observability

- Request/response logging
- Error tracking (Sentry integration ready)
- Performance metrics
- WebSocket connection monitoring
- Job queue status tracking

## Future Enhancements

1. **Advanced Features**
   - Multi-page application support
   - State management generation
   - API endpoint generation
   - Database schema inference

2. **AI Improvements**
   - Fine-tuned models for better accuracy
   - Custom component library training
   - Automated testing generation

3. **Platform Extensions**
   - VS Code extension
   - CLI tool
   - Browser extension
   - API for programmatic access
