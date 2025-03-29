from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings

from .api import router

app = FastAPI(title="Flight School API")

origins = settings.CORS_ORIGINS.split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"} 