"""
ImaraFund Main Application
FastAPI app with CORS, startup events, and API routing
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.database import init_db
from app.api.endpoints import router

# Initialize FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI-powered matching platform for African SME funding",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix=settings.API_V1_PREFIX)


@app.on_event("startup")
async def startup_event():
    """Initialize database on application startup"""
    init_db()
    print("🚀 ImaraFund API started successfully!")


@app.get("/")
async def root():
    """Root endpoint with ImaraFund API information"""
    return {
        "message": "Welcome to ImaraFund API",
        "description": "AI-powered matching platform for African SME funding",
        "version": "1.0.0",
        "documentation": "/docs",
        "algorithm": "IntelligentMatcher v1.0 (40/30/20/10 scoring)",
        "endpoints": {
            "grants": f"{settings.API_V1_PREFIX}/grants",
            "companies": f"{settings.API_V1_PREFIX}/companies",
            "matching": f"{settings.API_V1_PREFIX}/match/{{company_id}}"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "service": "imarafund-api",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=settings.DEBUG)