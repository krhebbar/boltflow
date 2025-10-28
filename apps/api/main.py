"""
Boltflow FastAPI Backend
Main application entry point
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from routers import scraper, analyzer, generator, cms
from lib.websocket_manager import WebSocketManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# WebSocket manager for real-time updates
ws_manager = WebSocketManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    logger.info("🚀 Boltflow API starting up...")
    # Startup: Initialize connections, load models, etc.
    yield
    # Shutdown: Clean up resources
    logger.info("👋 Boltflow API shutting down...")

app = FastAPI(
    title="Boltflow API",
    description="AI-driven web migration and modernization system",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://*.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(scraper.router, prefix="/api/scraper", tags=["scraper"])
app.include_router(analyzer.router, prefix="/api/analyzer", tags=["analyzer"])
app.include_router(generator.router, prefix="/api/generator", tags=["generator"])
app.include_router(cms.router, prefix="/api/cms", tags=["cms"])

@app.get("/")
async def root():
    return {
        "service": "Boltflow API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "scraper": "/api/scraper",
            "analyzer": "/api/analyzer",
            "generator": "/api/generator",
            "cms": "/api/cms",
            "websocket": "/ws/{client_id}"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """WebSocket endpoint for real-time updates"""
    await ws_manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            await ws_manager.send_personal_message(f"Echo: {data}", client_id)
    except WebSocketDisconnect:
        ws_manager.disconnect(client_id)
        logger.info(f"Client {client_id} disconnected")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
