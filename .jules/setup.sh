#!/bin/bash
set -e

echo "🚀 Setting up Boltflow..."

# Install Node dependencies
npm install

# Install Python dependencies
cd apps/api
pip install -r requirements.txt
playwright install chromium
cd ../..

# Build packages
npm run build

echo ""
echo "✅ Boltflow setup complete!"
echo "Note: Start Redis before running: docker run -d -p 6379:6379 redis:7-alpine"
