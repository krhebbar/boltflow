# Boltflow Deployment Guide

## Table of Contents
- [Development Setup](#development-setup)
- [Docker Deployment](#docker-deployment)
- [Cloud Deployment](#cloud-deployment)
- [Environment Variables](#environment-variables)
- [Troubleshooting](#troubleshooting)

## Development Setup

### Prerequisites
- Node.js 20+
- Python 3.11+
- Redis (via Docker or local install)
- OpenAI API key

### Quick Start

1. **Clone and Install:**
```bash
git clone https://github.com/yourusername/boltflow-modern.git
cd boltflow-modern
./scripts/setup.sh
```

2. **Configure Environment:**
```bash
# Copy environment files
cp .env.example .env
cp apps/web/.env.local.example apps/web/.env.local
cp apps/api/.env.example apps/api/.env

# Add your OpenAI API key to .env
echo "OPENAI_API_KEY=sk-your-key-here" >> .env
```

3. **Start Development Servers:**
```bash
./scripts/dev.sh
```

Or manually:
```bash
# Terminal 1 - Redis
docker run -d --name boltflow-redis -p 6379:6379 redis:7-alpine

# Terminal 2 - Backend
cd apps/api
python3 -m uvicorn main:app --reload

# Terminal 3 - Frontend
npm run dev --filter=web
```

Access the app:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## Docker Deployment

### Using Docker Compose (Recommended)

1. **Build and Start:**
```bash
docker-compose up -d
```

2. **View Logs:**
```bash
docker-compose logs -f
```

3. **Stop Services:**
```bash
docker-compose down
```

### Individual Container Builds

**Backend:**
```bash
docker build -f docker/api.Dockerfile -t boltflow-api .
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=sk-your-key \
  -e REDIS_URL=redis://host.docker.internal:6379 \
  boltflow-api
```

**Frontend:**
```bash
docker build -f docker/web.Dockerfile -t boltflow-web .
docker run -p 3000:3000 \
  -e NEXT_PUBLIC_API_URL=http://localhost:8000 \
  boltflow-web
```

---

## Cloud Deployment

### Option 1: Vercel + Railway

#### Deploy Frontend to Vercel

1. **Install Vercel CLI:**
```bash
npm i -g vercel
```

2. **Deploy:**
```bash
cd apps/web
vercel --prod
```

3. **Configure Environment:**
In Vercel dashboard, add:
- `NEXT_PUBLIC_API_URL` → Your Railway API URL
- `NEXT_PUBLIC_SUPABASE_URL` → Your Supabase URL
- `NEXT_PUBLIC_SUPABASE_ANON_KEY` → Your Supabase key

#### Deploy Backend to Railway

1. **Install Railway CLI:**
```bash
npm i -g @railway/cli
railway login
```

2. **Create Project:**
```bash
railway init
```

3. **Deploy:**
```bash
cd apps/api
railway up
```

4. **Add Environment Variables:**
```bash
railway variables set OPENAI_API_KEY=sk-your-key
railway variables set REDIS_URL=redis://...
```

5. **Add Redis:**
```bash
railway add
# Select Redis from the list
```

### Option 2: Fly.io

#### Backend on Fly.io

1. **Install Fly CLI:**
```bash
curl -L https://fly.io/install.sh | sh
fly auth login
```

2. **Create `fly.toml`:**
```toml
app = "boltflow-api"
primary_region = "sjc"

[build]
  dockerfile = "docker/api.Dockerfile"

[env]
  PORT = "8000"

[[services]]
  internal_port = 8000
  protocol = "tcp"

  [[services.ports]]
    port = 80
    handlers = ["http"]

  [[services.ports]]
    port = 443
    handlers = ["tls", "http"]
```

3. **Deploy:**
```bash
fly deploy
fly secrets set OPENAI_API_KEY=sk-your-key
```

4. **Add Redis:**
```bash
fly redis create
```

#### Frontend on Vercel (as above)

### Option 3: Self-Hosted (VPS)

#### Requirements
- Ubuntu 22.04+ VPS
- 2GB RAM minimum
- Docker installed

#### Setup

1. **SSH into VPS:**
```bash
ssh user@your-server.com
```

2. **Clone Repository:**
```bash
git clone https://github.com/yourusername/boltflow-modern.git
cd boltflow-modern
```

3. **Configure Environment:**
```bash
cp .env.example .env
nano .env  # Add your secrets
```

4. **Install Docker:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```

5. **Deploy:**
```bash
docker-compose up -d
```

6. **Setup Nginx Reverse Proxy:**
```nginx
server {
    server_name boltflow.yourdomain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
    }

    location /api {
        proxy_pass http://localhost:8000;
    }

    location /ws {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

7. **Enable SSL:**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d boltflow.yourdomain.com
```

---

## Environment Variables

### Required Variables

**Backend (`apps/api/.env`):**
```bash
OPENAI_API_KEY=sk-your-key-here
REDIS_URL=redis://localhost:6379
```

**Frontend (`apps/web/.env.local`):**
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

### Optional Variables

**Database (for production):**
```bash
DATABASE_URL=postgresql://user:pass@host:5432/boltflow
NEXT_PUBLIC_SUPABASE_URL=https://project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-key
```

**CMS Integrations:**
```bash
SANITY_PROJECT_ID=your-project-id
SANITY_DATASET=production
SANITY_API_TOKEN=your-token

HYGRAPH_ENDPOINT=https://api.hygraph.com/v2/...
HYGRAPH_TOKEN=your-token

STRAPI_URL=http://localhost:1337
STRAPI_API_TOKEN=your-token
```

**Deployment:**
```bash
VERCEL_TOKEN=your-vercel-token
```

---

## Production Checklist

- [ ] Set `NODE_ENV=production`
- [ ] Use production Redis instance (Upstash, Redis Cloud)
- [ ] Set up PostgreSQL database (Supabase, Neon)
- [ ] Configure CORS properly
- [ ] Enable rate limiting
- [ ] Set up error tracking (Sentry)
- [ ] Configure monitoring (DataDog, New Relic)
- [ ] Set up SSL/TLS certificates
- [ ] Configure CDN for static assets
- [ ] Enable logging and analytics
- [ ] Set up automated backups
- [ ] Configure auto-scaling (if needed)

---

## Scaling Considerations

### Horizontal Scaling

**Backend:**
- Run multiple API instances behind load balancer
- Use Redis for session storage
- Implement distributed job queue

**Frontend:**
- Vercel automatically handles scaling
- Use edge caching for static assets

### Vertical Scaling

**For High Load:**
- API: 4GB RAM, 2 vCPUs minimum
- Redis: 2GB RAM minimum
- Database: Based on data volume

### Database Optimization

```sql
-- Add indexes for common queries
CREATE INDEX idx_projects_user_id ON projects(user_id);
CREATE INDEX idx_jobs_status ON jobs(status);
```

### Caching Strategy

```python
# Cache AI analysis results
@cache(ttl=3600)
async def analyze_page(html: str):
    # Expensive AI analysis
    pass
```

---

## Monitoring

### Health Checks

**Backend:**
```bash
curl http://localhost:8000/health
```

**Frontend:**
```bash
curl http://localhost:3000/api/health
```

### Logs

**Docker:**
```bash
docker-compose logs -f api
docker-compose logs -f web
```

**Production:**
```bash
pm2 logs boltflow-api
pm2 logs boltflow-web
```

---

## Troubleshooting

### Common Issues

**1. Redis Connection Failed**
```bash
# Check if Redis is running
docker ps | grep redis

# Restart Redis
docker restart boltflow-redis
```

**2. Playwright Install Failed**
```bash
# Install Playwright browsers manually
cd apps/api
playwright install chromium
playwright install-deps
```

**3. Build Errors**
```bash
# Clear caches
rm -rf node_modules .next apps/web/.next
npm install
npm run build
```

**4. WebSocket Connection Issues**
```bash
# Check CORS settings in main.py
# Ensure WS_URL matches your deployment
```

**5. OpenAI API Errors**
```bash
# Verify API key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"

# Check rate limits and billing
```

### Debug Mode

**Backend:**
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
uvicorn main:app --reload --log-level debug
```

**Frontend:**
```bash
# Enable Next.js debug mode
DEBUG=* npm run dev
```

---

## Backup & Recovery

### Database Backup

```bash
# PostgreSQL backup
pg_dump -U user -h host boltflow > backup.sql

# Restore
psql -U user -h host boltflow < backup.sql
```

### Scraped Data Backup

```bash
# Backup scraped files
tar -czf scraped-backup.tar.gz apps/api/scraped/

# Restore
tar -xzf scraped-backup.tar.gz -C apps/api/
```

---

## Support

- **Issues:** https://github.com/yourusername/boltflow-modern/issues
- **Discussions:** https://github.com/yourusername/boltflow-modern/discussions
- **Email:** support@boltflow.dev

---

## License

MIT License - see LICENSE file for details
