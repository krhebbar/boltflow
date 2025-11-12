# Boltflow Architecture

## Overview

Boltflow is an experimental AI-driven web migration system that transforms legacy websites into modern Next.js applications with automated component generation, CMS integration, and deployment.

## System Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        CL[Next.js 14 App Router<br/>React 18 + ShadCN UI<br/>TanStack Query + Socket.io]
    end

    subgraph "Orchestration Layer"
        OL[FastAPI + WebSocket Manager<br/>Background Jobs + Redis Queue]
    end

    subgraph "Processing Engines"
        SE[Scraper Engine<br/>Playwright]
        AI[AI Analysis<br/>GPT-4 + Embeddings]
        GE[Code Generator<br/>React + TypeScript]
        CM[CMS Integration<br/>Multi-Provider]
    end

    subgraph "Data Layer"
        DB[(PostgreSQL<br/>SQLAlchemy + Drizzle)]
        RD[(Redis<br/>Cache + Queue)]
    end

    CL -->|REST API<br/>WebSocket| OL
    OL --> SE
    OL --> AI
    OL --> GE
    OL --> CM
    OL -.-> DB
    OL -.-> RD
    SE -.-> DB
    AI -.-> DB
    GE -.-> DB
    CM -.-> DB

    style CL fill:#e3f2fd
    style OL fill:#fff3e0
    style SE fill:#e8f5e9
    style AI fill:#f3e5f5
    style GE fill:#ede7f6
    style CM fill:#fce4ec
    style DB fill:#e0f2f1
    style RD fill:#ffebee
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
│   │   ├── (auth)/       # Auth pages (login, signup)
│   │   ├── dashboard/    # Dashboard pages
│   │   └── page.tsx      # Landing page
│   ├── components/       # React components
│   │   ├── ui/          # ShadCN UI components
│   │   └── dashboard/   # Dashboard-specific
│   ├── providers/        # Context providers
│   ├── hooks/            # Custom React hooks
│   ├── lib/              # Utilities and API client
│   └── types/            # TypeScript types
└── public/              # Static assets
```

### 2. Backend Layer (FastAPI)

**Location:** `apps/api/`

**Technology Stack:**
- FastAPI (Python 3.11+)
- SQLAlchemy with asyncpg
- Playwright for web scraping
- OpenAI GPT-4 for AI analysis
- Redis for caching and job queues
- WebSocket for real-time communication

**Architecture Patterns:**
- Router-based modular design
- Async/await throughout
- Background task processing
- Event-driven WebSocket updates
- Custom exception hierarchy
- Structured logging with structlog

**File Structure:**
```
apps/api/
├── main.py              # FastAPI app entry
├── config/              # Configuration
│   ├── database.py      # Database session management
│   └── settings.py      # Pydantic settings
├── models/              # SQLAlchemy models
│   ├── user.py
│   ├── project.py
│   ├── job.py
│   └── ...
├── routers/             # API endpoints
│   ├── auth.py         # Authentication
│   ├── scraper.py      # Web scraping
│   ├── analyzer.py     # AI analysis
│   ├── generator.py    # Code generation
│   └── cms.py          # CMS integration
├── lib/                 # Core utilities
│   ├── auth.py         # JWT authentication
│   ├── exceptions.py   # Custom exceptions
│   └── websocket_manager.py
├── middleware/          # FastAPI middleware
│   └── error_handler.py
├── ai/                  # AI modules
│   ├── analyzer.py     # DOM analysis
│   └── classifier.py   # Component classification
└── scrapers/            # Scraping engines
    └── playwright_scraper.py
```

### 3. AI Analysis Pipeline

```mermaid
flowchart LR
    A[HTML/CSS Input] --> B[GPT-4 Analysis]
    B --> C[Structural Parsing]
    C --> D[Component Detection]
    D --> E[Embedding Generation]
    E --> F[Similarity Matching]
    F --> G[Complexity Scoring]
    G --> H[Analysis Output]

    style A fill:#e3f2fd
    style B fill:#f3e5f5
    style H fill:#e8f5e9
```

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

**Job Queue (Redis):**
- Background job processing
- Retry logic for failed tasks
- Progress tracking
- Job status persistence in database

## Data Flow

### Migration Workflow

```mermaid
stateDiagram-v2
    [*] --> UserInput: URL Submission
    UserInput --> Scraping: Create Project & Job
    Scraping --> Analysis: Pages Scraped
    Analysis --> Generation: Components Identified
    Generation --> CMSSync: Code Generated
    CMSSync --> Deployment: Content Synced
    Deployment --> [*]: Complete

    Scraping --> Failed: Error
    Analysis --> Failed: Error
    Generation --> Failed: Error
    CMSSync --> Failed: Error
    Failed --> [*]

    note right of Scraping
        Playwright crawls site
        Extracts HTML/CSS
        Saves to database
        Real-time WebSocket updates
    end note

    note right of Analysis
        GPT-4 analyzes structure
        Classifies components
        Calculates complexity
        Stores results
    end note

    note right of Generation
        Generates React components
        Creates TypeScript types
        Extracts Tailwind styles
        Builds project structure
    end note
```

**Detailed Steps:**

1. **User Input**
   - URL submission
   - Configuration (max pages, UI library, CMS)
   - Authentication required

2. **Web Scraping (Playwright)**
   - Crawl website
   - Extract HTML/CSS
   - Capture screenshots
   - Save to database
   - Broadcast progress via WebSocket

3. **AI Analysis (GPT-4 + Embeddings)**
   - Analyze DOM structure
   - Classify components
   - Extract design tokens
   - Calculate complexity
   - Store analysis results

4. **Code Generation**
   - Generate React components
   - Create page structure
   - Adapt styles to Tailwind
   - Generate TypeScript types
   - Save to database

5. **CMS Integration (Optional)**
   - Create content schema
   - Migrate content
   - Configure API
   - Test integration

6. **Output**
   - Generated code (ZIP download)
   - GitHub repository
   - Vercel deployment

## Deployment Architecture

### Development Environment

```mermaid
graph LR
    A[Next.js<br/>:3000] -->|HTTP| B[FastAPI<br/>:8000]
    B -->|TCP| C[Redis<br/>:6379]
    B -->|TCP| D[PostgreSQL<br/>:5432]
    A -.->|WebSocket| B

    style A fill:#e3f2fd
    style B fill:#fff3e0
    style C fill:#ffebee
    style D fill:#e0f2f1
```

### Production (Docker)

```mermaid
graph TB
    subgraph "Docker Compose"
        subgraph "Frontend"
            WEB[Web Container<br/>Next.js<br/>Port 3000]
        end
        subgraph "Backend"
            API[API Container<br/>FastAPI<br/>Port 8000]
        end
        subgraph "Data Services"
            REDIS[Redis Container<br/>Port 6379]
            PG[PostgreSQL Container<br/>Port 5432]
        end
    end

    WEB --> API
    API --> REDIS
    API --> PG
    WEB -.->|WebSocket| API

    style WEB fill:#e3f2fd
    style API fill:#fff3e0
    style REDIS fill:#ffebee
    style PG fill:#e0f2f1
```

### Cloud Deployment

```mermaid
graph TB
    subgraph "Edge Network"
        CDN[Vercel Edge<br/>Global CDN]
    end

    subgraph "Application Layer"
        FE[Next.js Frontend<br/>Vercel]
        BE[FastAPI Backend<br/>Railway/Fly.io]
    end

    subgraph "Data Layer"
        DB[(Supabase<br/>PostgreSQL)]
        CACHE[(Upstash<br/>Redis)]
        STORAGE[(Supabase<br/>Storage)]
    end

    CDN --> FE
    FE --> BE
    BE --> DB
    BE --> CACHE
    BE --> STORAGE
    FE -.->|WebSocket| BE

    style CDN fill:#f3e5f5
    style FE fill:#e3f2fd
    style BE fill:#fff3e0
    style DB fill:#e0f2f1
    style CACHE fill:#ffebee
    style STORAGE fill:#e8f5e9
```

**Recommended Services:**
- **Frontend:** Vercel Edge Network
- **Backend:** Railway / Fly.io
- **Database:** Supabase (PostgreSQL)
- **Cache:** Upstash (Redis)
- **Storage:** Supabase Storage / S3

## Security Considerations

```mermaid
mindmap
  root((Security))
    API Security
      JWT Authentication
      CORS Configuration
      Rate Limiting
      Input Validation
    Data Privacy
      Encryption at Rest
      Secure Credentials
      User Data Isolation
      GDPR Compliance
    Code Security
      Dependency Scanning
      Output Sanitization
      SQL Injection Prevention
      XSS Protection
```

1. **API Security**
   - JWT authentication with bcrypt
   - CORS configuration (no wildcards)
   - Rate limiting per user
   - Input sanitization and validation

2. **Data Privacy**
   - Database encryption at rest
   - Secure credential storage
   - User data isolation
   - Compliance with data protection regulations

3. **Code Generation**
   - Safe template rendering
   - Output sanitization
   - Dependency security scanning
   - No arbitrary code execution

## Performance Optimizations

1. **Frontend**
   - Server-side rendering
   - Image optimization
   - Code splitting
   - Edge caching
   - React Server Components

2. **Backend**
   - Redis caching for AI results
   - Background job processing
   - Database connection pooling
   - Async operations throughout
   - Query optimization with indexes

3. **AI Pipeline**
   - Prompt optimization
   - Response caching (1 hour TTL)
   - Batch processing where possible
   - Token usage optimization
   - Rate limit handling with retries

## Monitoring & Observability

```mermaid
graph LR
    APP[Application] --> LOGS[Structured Logs<br/>structlog]
    APP --> METRICS[Metrics<br/>Prometheus]
    APP --> ERRORS[Error Tracking<br/>Sentry]
    APP --> TRACES[Request Tracing<br/>OpenTelemetry]

    LOGS --> VIZ[Visualization<br/>Grafana/DataDog]
    METRICS --> VIZ
    ERRORS --> VIZ
    TRACES --> VIZ

    style APP fill:#e3f2fd
    style LOGS fill:#fff3e0
    style METRICS fill:#e8f5e9
    style ERRORS fill:#ffebee
    style TRACES fill:#f3e5f5
    style VIZ fill:#ede7f6
```

**Implemented:**
- Structured logging with structlog (JSON output)
- Request/response logging
- Error tracking with custom exceptions
- WebSocket connection monitoring
- Database query logging

**Planned:**
- Sentry integration for error tracking
- Prometheus metrics
- Performance monitoring (APM)
- Health check endpoints with dependency verification
- Alerting for critical failures

## Database Schema

```mermaid
erDiagram
    USERS ||--o{ PROJECTS : owns
    PROJECTS ||--o{ JOBS : contains
    JOBS ||--o{ SCRAPED_PAGES : produces
    JOBS ||--o{ GENERATED_COMPONENTS : produces

    USERS {
        uuid id PK
        string email UK
        string password_hash
        string name
        timestamp created_at
        timestamp updated_at
    }

    PROJECTS {
        uuid id PK
        uuid user_id FK
        string name
        string url
        string status
        int max_pages
        timestamp created_at
        timestamp updated_at
    }

    JOBS {
        uuid id PK
        uuid project_id FK
        string type
        string status
        int progress
        jsonb result
        string error
        timestamp created_at
        timestamp completed_at
    }

    SCRAPED_PAGES {
        uuid id PK
        uuid job_id FK
        string url
        text html
        text css
        text screenshot
        jsonb metadata
        timestamp scraped_at
    }

    GENERATED_COMPONENTS {
        uuid id PK
        uuid job_id FK
        string component_type
        string filename
        text content
        timestamp created_at
    }
```

## Future Enhancements

1. **Advanced Features**
   - Multi-page application support
   - State management generation (Zustand/Redux)
   - API endpoint generation from backend analysis
   - Database schema inference

2. **AI Improvements**
   - Fine-tuned models for better accuracy
   - Custom component library training
   - Automated testing generation
   - Code review and optimization suggestions

3. **Platform Extensions**
   - VS Code extension for inline migration
   - CLI tool for batch processing
   - Browser extension for one-click capture
   - Public API for programmatic access

4. **Infrastructure**
   - Kubernetes deployment support
   - Multi-region deployment
   - Advanced caching strategies
   - CDN integration for assets
