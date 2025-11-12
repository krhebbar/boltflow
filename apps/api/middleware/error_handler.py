"""Global error handling middleware"""
import logging
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

from lib.exceptions import BoltflowException

logger = logging.getLogger(__name__)


async def boltflow_exception_handler(request: Request, exc: BoltflowException):
    """Handle custom Boltflow exceptions"""
    logger.error(
        f"BoltflowException: {exc.message}",
        extra={
            "status_code": exc.status_code,
            "path": request.url.path,
            "details": exc.details
        }
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "message": exc.message,
                "details": exc.details,
                "type": exc.__class__.__name__
            }
        }
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors"""
    logger.warning(
        f"Validation error: {exc.errors()}",
        extra={"path": request.url.path}
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "message": "Validation failed",
                "details": exc.errors(),
                "type": "ValidationError"
            }
        }
    )


async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """Handle database errors"""
    logger.error(
        f"Database error: {str(exc)}",
        extra={"path": request.url.path},
        exc_info=True
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "message": "Database operation failed",
                "type": "DatabaseError"
            }
        }
    )


async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions"""
    logger.error(
        f"Unexpected error: {str(exc)}",
        extra={"path": request.url.path},
        exc_info=True
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "message": "An unexpected error occurred",
                "type": "InternalServerError"
            }
        }
    )
