"""Custom exceptions for better error handling"""
from typing import Any, Optional


class BoltflowException(Exception):
    """Base exception for all Boltflow errors"""
    def __init__(
        self,
        message: str,
        status_code: int = 500,
        details: Optional[dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class ValidationError(BoltflowException):
    """Raised when input validation fails"""
    def __init__(self, message: str, details: Optional[dict[str, Any]] = None):
        super().__init__(message, status_code=400, details=details)


class AuthenticationError(BoltflowException):
    """Raised when authentication fails"""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, status_code=401)


class AuthorizationError(BoltflowException):
    """Raised when user doesn't have permission"""
    def __init__(self, message: str = "Permission denied"):
        super().__init__(message, status_code=403)


class NotFoundError(BoltflowException):
    """Raised when a resource is not found"""
    def __init__(self, resource: str, identifier: Any):
        message = f"{resource} with identifier '{identifier}' not found"
        super().__init__(message, status_code=404)


class RateLimitError(BoltflowException):
    """Raised when rate limit is exceeded"""
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(message, status_code=429)


class ExternalServiceError(BoltflowException):
    """Raised when external service (OpenAI, etc.) fails"""
    def __init__(self, service: str, message: str):
        super().__init__(
            f"{service} error: {message}",
            status_code=502,
            details={"service": service}
        )


class DatabaseError(BoltflowException):
    """Raised when database operation fails"""
    def __init__(self, message: str):
        super().__init__(f"Database error: {message}", status_code=500)
