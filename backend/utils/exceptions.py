from fastapi import HTTPException
from typing import Dict, Any

class YouTubeAutomationException(Exception):
    """Base exception for YouTube automation system"""
    
    def __init__(self, message: str, error_code: str = None, details: Dict[str, Any] = None):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)

class AgentException(YouTubeAutomationException):
    """Exception raised by AI agents"""
    
    def __init__(self, agent_name: str, message: str, details: Dict[str, Any] = None):
        self.agent_name = agent_name
        super().__init__(f"Agent {agent_name}: {message}", "AGENT_ERROR", details)

class DatabaseException(YouTubeAutomationException):
    """Exception raised by database operations"""
    
    def __init__(self, operation: str, message: str, details: Dict[str, Any] = None):
        self.operation = operation
        super().__init__(f"Database {operation}: {message}", "DATABASE_ERROR", details)

class VideoProcessingException(YouTubeAutomationException):
    """Exception raised during video processing"""
    
    def __init__(self, operation: str, message: str, details: Dict[str, Any] = None):
        self.operation = operation
        super().__init__(f"Video processing {operation}: {message}", "VIDEO_PROCESSING_ERROR", details)

class YouTubeAPIException(YouTubeAutomationException):
    """Exception raised by YouTube API operations"""
    
    def __init__(self, operation: str, message: str, details: Dict[str, Any] = None):
        self.operation = operation
        super().__init__(f"YouTube API {operation}: {message}", "YOUTUBE_API_ERROR", details)

class ValidationException(YouTubeAutomationException):
    """Exception raised during data validation"""
    
    def __init__(self, field: str, message: str, details: Dict[str, Any] = None):
        self.field = field
        super().__init__(f"Validation error for {field}: {message}", "VALIDATION_ERROR", details)

class RateLimitException(YouTubeAutomationException):
    """Exception raised when rate limit is exceeded"""
    
    def __init__(self, service: str, message: str = None, details: Dict[str, Any] = None):
        self.service = service
        message = message or f"Rate limit exceeded for {service}"
        super().__init__(message, "RATE_LIMIT_ERROR", details)

class AuthenticationException(YouTubeAutomationException):
    """Exception raised during authentication"""
    
    def __init__(self, service: str, message: str = None, details: Dict[str, Any] = None):
        self.service = service
        message = message or f"Authentication failed for {service}"
        super().__init__(message, "AUTHENTICATION_ERROR", details)

class ConfigurationException(YouTubeAutomationException):
    """Exception raised due to configuration issues"""
    
    def __init__(self, config_key: str, message: str = None, details: Dict[str, Any] = None):
        self.config_key = config_key
        message = message or f"Configuration error for {config_key}"
        super().__init__(message, "CONFIGURATION_ERROR", details)

# HTTP Exception helpers
def create_http_exception(status_code: int, message: str, error_code: str = None, details: Dict[str, Any] = None) -> HTTPException:
    """Create an HTTP exception with consistent format"""
    content = {
        "error": message,
        "error_code": error_code,
        "details": details or {},
        "status_code": status_code
    }
    return HTTPException(status_code=status_code, detail=content)

def create_bad_request_exception(message: str, field: str = None, details: Dict[str, Any] = None) -> HTTPException:
    """Create a 400 Bad Request exception"""
    error_code = "BAD_REQUEST"
    if field:
        error_code = "VALIDATION_ERROR"
        details = details or {}
        details["field"] = field
    
    return create_http_exception(400, message, error_code, details)

def create_unauthorized_exception(message: str = "Unauthorized", details: Dict[str, Any] = None) -> HTTPException:
    """Create a 401 Unauthorized exception"""
    return create_http_exception(401, message, "UNAUTHORIZED", details)

def create_forbidden_exception(message: str = "Forbidden", details: Dict[str, Any] = None) -> HTTPException:
    """Create a 403 Forbidden exception"""
    return create_http_exception(403, message, "FORBIDDEN", details)

def create_not_found_exception(resource: str, identifier: str = None, details: Dict[str, Any] = None) -> HTTPException:
    """Create a 404 Not Found exception"""
    message = f"{resource} not found"
    if identifier:
        message = f"{resource} with identifier '{identifier}' not found"
    
    details = details or {}
    details["resource"] = resource
    if identifier:
        details["identifier"] = identifier
    
    return create_http_exception(404, message, "NOT_FOUND", details)

def create_conflict_exception(message: str, details: Dict[str, Any] = None) -> HTTPException:
    """Create a 409 Conflict exception"""
    return create_http_exception(409, message, "CONFLICT", details)

def create_rate_limit_exception(message: str = "Rate limit exceeded", details: Dict[str, Any] = None) -> HTTPException:
    """Create a 429 Too Many Requests exception"""
    return create_http_exception(429, message, "RATE_LIMIT_EXCEEDED", details)

def create_internal_server_exception(message: str = "Internal server error", details: Dict[str, Any] = None) -> HTTPException:
    """Create a 500 Internal Server Error exception"""
    return create_http_exception(500, message, "INTERNAL_SERVER_ERROR", details)

def create_service_unavailable_exception(message: str = "Service unavailable", details: Dict[str, Any] = None) -> HTTPException:
    """Create a 503 Service Unavailable exception"""
    return create_http_exception(503, message, "SERVICE_UNAVAILABLE", details)
