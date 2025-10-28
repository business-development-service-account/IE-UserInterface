from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.api.v1.endpoints import projects
from app.utils.exceptions import DatabaseException
from auth_implementation.api.endpoints import auth as auth_router


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="A RESTful API for managing projects with user authentication and authorization",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
api_v1_prefix = "/api/v1"
app.include_router(projects.router, prefix=api_v1_prefix, tags=["projects"])
app.include_router(auth_router.router, prefix=api_v1_prefix, tags=["authentication"])


@app.exception_handler(DatabaseException)
async def database_exception_handler(request: Request, exc: DatabaseException):
    """Global exception handler for database errors."""
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "DATABASE_ERROR",
                "message": exc.message,
                "details": {}
            }
        }
    )


@app.get("/")
async def root():
    """Root endpoint to verify API is running."""
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "version": settings.app_version
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="info" if settings.debug else "warning"
    )