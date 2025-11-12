"""
Boltflow FastAPI Backend
Main application entry point
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from contextlib import asynccontextmanager
import structlog

from routers import scraper, analyzer, generator, cms, auth
from lib.websocket_manager import WebSocketManager
from lib.exceptions import BoltflowException
from middleware.error_handler import (
    boltflow_exception_handler,
    validation_exception_handler,
    sqlalchemy_exception_handler,
    general_exception_handler
)
from config.database import init_db
from config.settings import settings

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger(__name__)

# WebSocket manager for real-time updates
ws_manager = WebSocketManager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    logger.info("boltflow_startup", message="Boltflow API starting up...")

    # Initialize database tables
    try:
        await init_db()
        logger.info("database_initialized", message="Database tables created/verified")
    except Exception as e:
        logger.error("database_init_failed", error=str(e))
        raise

    # Validate settings
    logger.info("settings_loaded",
                debug=settings.debug,
                log_level=settings.log_level)

    yield

    # Shutdown: Clean up resources
    logger.info("boltflow_shutdown", message="Boltflow API shutting down...")


app = FastAPI(
    title=settings.app_name,
    description="AI-driven web migration and modernization system",
    version=settings.app_version,
    lifespan=lifespan
)

# CORS middleware - restrict to configured origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
    max_age=600,
)

# Register exception handlers
app.add_exception_handler(BoltflowException, boltflow_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(scraper.router, prefix="/api/scraper", tags=["scraper"])
app.include_router(analyzer.router, prefix="/api/analyzer", tags=["analyzer"])
app.include_router(generator.router, prefix="/api/generator", tags=["generator"])
app.include_router(cms.router, prefix="/api/cms", tags=["cms"])


@app.get("/")
async def root():
    return {
        "service": settings.app_name,
        "version": settings.app_version,
        "status": "running",
        "endpoints": {
            "auth": "/api/auth",
            "scraper": "/api/scraper",
            "analyzer": "/api/analyzer",
            "generator": "/api/generator",
            "cms": "/api/cms",
            "websocket": "/ws/{client_id}",
            "docs": "/docs",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint with dependency verification"""
    # TODO: Add checks for Redis, database connection, OpenAI API
    return {
        "status": "healthy",
        "version": settings.app_version,
        "checks": {
            "api": "ok",
            # Add more health checks as needed
        }
    }


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """WebSocket endpoint for real-time updates"""
    await ws_manager.connect(websocket, client_id)
    logger.info("websocket_connected", client_id=client_id)

    try:
        while True:
            data = await websocket.receive_text()
            # Echo for now, can add routing logic later
            await ws_manager.send_personal_message(f"Echo: {data}", client_id)
    except WebSocketDisconnect:
        ws_manager.disconnect(client_id)
        logger.info("websocket_disconnected", client_id=client_id)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
