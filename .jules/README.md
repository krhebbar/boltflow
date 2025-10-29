# Jules Environment Setup - Boltflow

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for GPT-4 analysis | Yes |
| `DATABASE_URL` | PostgreSQL connection (Supabase) | Yes |
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase project URL | Yes |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Supabase anonymous key | Yes |
| `REDIS_URL` | Redis connection URL | Default: redis://localhost:6379 |
| `NEXT_PUBLIC_API_URL` | Backend API URL | Default: http://localhost:8000 |
| `NEXT_PUBLIC_WS_URL` | WebSocket URL | Default: ws://localhost:8000 |

## Tech Stack
- Next.js 14 + FastAPI, Python 3.11+, Playwright, GPT-4, Redis, Supabase
