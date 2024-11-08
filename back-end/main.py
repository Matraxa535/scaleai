from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from app.core.config import settings
from app.api.endpoints import mpi, health, preprocess, news, summarize

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True, 
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=3600 # 1 Hour cache for preflight requests
)

@app.get("/")
async def root():
    """Redirect root to API documentation"""
    return RedirectResponse(url="/docs")

# Include routers
app.include_router(mpi.router, prefix=f"{settings.API_V1_STR}/mpi", tags=["mpi"])
app.include_router(health.router, prefix=f"{settings.API_V1_STR}/health", tags=["health"])
app.include_router(
    preprocess.router,
    prefix=f"{settings.API_V1_STR}/preprocess",  # Changed this line
    tags=["preprocess"]
)
app.include_router(
    news.router,
    prefix=f"{settings.API_V1_STR}/news",
    tags=["news"]
)

app.include_router(
    summarize.router,
    prefix=f"{settings.API_V1_STR}/summarize",
    tags=["summarize"]
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)