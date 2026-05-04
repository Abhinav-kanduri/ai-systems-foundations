"""
API application initialization and main setup.
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging

from api.routes import applications, decisions, status, human_review

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    
    app = FastAPI(
        title="Reliable Multi-Agent Loan Underwriting System",
        description="Production-grade multi-agent AI workflow for loan underwriting",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(
        applications.router,
        prefix="/api/v1/applications",
        tags=["Applications"]
    )
    
    app.include_router(
        status.router,
        prefix="/api/v1/status",
        tags=["Status"]
    )
    
    app.include_router(
        decisions.router,
        prefix="/api/v1/decisions",
        tags=["Decisions"]
    )
    
    app.include_router(
        human_review.router,
        prefix="/api/v1/human-review",
        tags=["Human Review"]
    )
    
    # Health check endpoint
    @app.get("/health")
    async def health():
        """Health check endpoint."""
        return {
            "status": "healthy",
            "service": "loan-underwriting-api"
        }
    
    # Root endpoint
    @app.get("/")
    async def root():
        """Root endpoint."""
        return {
            "service": "Reliable Multi-Agent Loan Underwriting System",
            "version": "1.0.0",
            "docs": "/docs"
        }
    
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request, exc):
        """Custom HTTP exception handler."""
        logger.error(f"HTTP Exception: {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.detail,
                "status_code": exc.status_code
            }
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request, exc):
        """Custom general exception handler."""
        logger.error(f"Unhandled Exception: {str(exc)}")
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "status_code": 500
            }
        )
    
    return app


# Create app instance
app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
