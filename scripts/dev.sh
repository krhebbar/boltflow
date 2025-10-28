#!/bin/bash

set -e

echo "🚀 Starting Boltflow development servers..."

# Start Redis in background if not running
if ! docker ps | grep -q redis; then
    echo "📦 Starting Redis..."
    docker run -d --name boltflow-redis -p 6379:6379 redis:7-alpine
fi

# Start API server in background
echo "🐍 Starting FastAPI backend..."
cd apps/api
python3 -m uvicorn main:app --reload --port 8000 &
API_PID=$!
cd ../..

# Start Next.js dev server
echo "⚡ Starting Next.js frontend..."
npm run dev --filter=web &
WEB_PID=$!

echo ""
echo "✅ Development servers started!"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all servers"

# Trap Ctrl+C and kill both processes
trap "kill $API_PID $WEB_PID; exit" INT

wait
