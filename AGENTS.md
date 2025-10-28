# Repository Guidelines

## Project Structure & Module Organization

Full-stack Turbo monorepo with Next.js frontend and FastAPI backend:

```
boltflow-modern/
├── apps/
│   ├── web/             # Next.js 14 dashboard (App Router)
│   └── api/             # FastAPI backend (Python)
├── packages/
│   ├── ui/              # Shared ShadCN component library
│   ├── db/              # Database schema (Drizzle ORM)
│   ├── cms/             # CMS connectors
│   └── generators/      # Code generation templates
├── docker/              # Docker configurations
├── docs/                # Architecture documentation
└── scripts/             # Setup and development scripts
```

## Build, Test, and Development Commands

```bash
# Quick start
./scripts/setup.sh         # Install all dependencies
./scripts/dev.sh           # Start all services (Redis + API + Web)

# Turbo commands
npm run dev                # Start frontend and backend
npm run build              # Build all packages
npm run lint               # Lint all packages
npm run type-check         # TypeScript type checking
npm run format             # Prettier formatting

# Per-app commands
npm run dev --filter=web   # Next.js frontend only
npm run dev --filter=api   # FastAPI backend only

# Docker deployment
docker-compose up          # Start all services in containers
docker-compose down        # Stop all services
```

## Coding Style & Naming Conventions

**TypeScript (Next.js/React):**
- **Prettier:** Configured for consistent formatting
- **Components:** PascalCase (`ProjectCard`, `MigrationProgress`, `NewProjectDialog`)
- **Files:** kebab-case (`project-card.tsx`, `migration-progress.tsx`)
- **Functions:** camelCase (`handleSubmit()`, `fetchProjects()`, `parseData()`)
- **Hooks:** camelCase with `use` prefix (`useWebSocket`, `useProjects`)
- Server Components by default; mark Client Components with `"use client"`

**Python (FastAPI):**
- **PEP 8:** Strict style guide compliance
- **Functions:** snake_case (`analyze_page()`, `generate_code()`, `scrape_website()`)
- **Classes:** PascalCase (`DOMAnalyzer`, `ComponentClassifier`, `WebSocketManager`)
- **Files:** snake_case (`dom_analyzer.py`, `playwright_scraper.py`)
- Type hints required for all public APIs
- Async/await for all I/O operations

## Testing Guidelines

**Framework:** Vitest (TypeScript), pytest (Python)

**Running Tests:**
```bash
# Frontend tests
npm run test --filter=web

# Backend tests
cd apps/api && pytest

# Test coverage
npm run test -- --coverage
```

**Conventions:**
- Test files: `*.test.ts` (TypeScript), `test_*.py` (Python)
- Mock external services (OpenAI, Supabase)
- Test real-time WebSocket events

## Commit & Pull Request Guidelines

**Commit Format:** Conventional Commits

```
feat(web): add real-time migration progress component
feat(api): implement GPT-4 DOM analysis
fix(scraper): handle dynamic content loading
docs(deployment): add Railway deployment guide
chore(docker): update base images to latest
```

**Scopes:** `web`, `api`, `ui`, `db`, `cms`, `generators`, `docker`, `docs`

**PR Requirements:**
- Link related issues
- Update relevant documentation
- Test both frontend and backend changes
- Ensure Docker build succeeds
- No lint/type errors

## Architecture & Patterns

**Real-Time Communication:**
- WebSocket server in FastAPI (`/ws/{client_id}`)
- Socket.io client in Next.js
- Broadcast progress updates during scraping/analysis

**AI Integration:**
- OpenAI GPT-4 for structural analysis
- Text embeddings for component classification
- Langchain for workflow orchestration

**Database:**
- Supabase (PostgreSQL) for persistence
- Drizzle ORM for type-safe queries
- Redis for job queues and caching

**Key Patterns:**
- Server Actions for mutations in Next.js
- Provider pattern for CMS integrations
- Background job processing with BullMQ
- Multi-stage Docker builds for optimization

## Environment Setup

**Required:**
- Node.js >= 20.0.0
- Python >= 3.11
- Redis (via Docker)
- OpenAI API key

**Environment Variables:**
```bash
# Copy templates
cp .env.example .env
cp apps/web/.env.local.example apps/web/.env.local
cp apps/api/.env.example apps/api/.env

# Add your keys
OPENAI_API_KEY=sk-your-key
DATABASE_URL=postgresql://...
REDIS_URL=redis://localhost:6379
```

**Docker Setup:**
```bash
docker-compose up redis    # Start Redis only
# OR
docker-compose up          # Start all services
```
