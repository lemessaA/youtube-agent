import time
import logging
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Dict, Any
import json

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Log request
        logger.info(f"Request: {request.method} {request.url}")
        
        # Process request
        response = await call_next(request)
        
        # Calculate processing time
        process_time = time.time() - start_time
        
        # Log response
        logger.info(f"Response: {response.status_code} - {process_time:.4f}s")
        
        # Add processing time to response headers
        response.headers["X-Process-Time"] = str(process_time)
        
        return response

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, calls: int = 100, period: int = 60):
        super().__init__(app)
        self.calls = calls  # Number of calls allowed
        self.period = period  # Time period in seconds
        self.clients: Dict[str, Dict[str, Any]] = {}
    
    async def dispatch(self, request: Request, call_next):
        # Get client IP
        client_ip = request.client.host
        
        # Get current time
        current_time = time.time()
        
        # Initialize client if not exists
        if client_ip not in self.clients:
            self.clients[client_ip] = {
                "calls": 0,
                "reset_time": current_time + self.period
            }
        
        client_data = self.clients[client_ip]
        
        # Reset counter if period has passed
        if current_time > client_data["reset_time"]:
            client_data["calls"] = 0
            client_data["reset_time"] = current_time + self.period
        
        # Check rate limit
        if client_data["calls"] >= self.calls:
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            return Response(
                content=json.dumps({"error": "Rate limit exceeded"}),
                status_code=429,
                headers={"Content-Type": "application/json"}
            )
        
        # Increment counter
        client_data["calls"] += 1
        
        # Process request
        response = await call_next(request)
        
        # Add rate limit headers
        response.headers["X-RateLimit-Limit"] = str(self.calls)
        response.headers["X-RateLimit-Remaining"] = str(self.calls - client_data["calls"])
        response.headers["X-RateLimit-Reset"] = str(int(client_data["reset_time"]))
        
        return response

class SecurityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Process request
        response = await call_next(request)
        
        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        return response

class CORSMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, allow_origins: list = ["*"], allow_methods: list = ["*"], allow_headers: list = ["*"]):
        super().__init__(app)
        self.allow_origins = allow_origins
        self.allow_methods = allow_methods
        self.allow_headers = allow_headers
    
    async def dispatch(self, request: Request, call_next):
        # Process request
        response = await call_next(request)
        
        # Add CORS headers
        origin = request.headers.get("origin")
        
        if "*" in self.allow_origins or origin in self.allow_origins:
            response.headers["Access-Control-Allow-Origin"] = origin or "*"
        
        response.headers["Access-Control-Allow-Methods"] = ", ".join(self.allow_methods)
        response.headers["Access-Control-Allow-Headers"] = ", ".join(self.allow_headers)
        response.headers["Access-Control-Allow-Credentials"] = "true"
        
        # Handle preflight requests
        if request.method == "OPTIONS":
            response = Response(status_code=200)
            response.headers["Access-Control-Allow-Origin"] = origin or "*"
            response.headers["Access-Control-Allow-Methods"] = ", ".join(self.allow_methods)
            response.headers["Access-Control-Allow-Headers"] = ", ".join(self.allow_headers)
            response.headers["Access-Control-Allow-Credentials"] = "true"
        
        return response
