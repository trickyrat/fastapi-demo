from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from app.api.api_v1.api import api_router
from config import settings

app = FastAPI(title="Fastapi Demo", openapi_url=f"{settings.API_BASE_URL}/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router, prefix=settings.API_BASE_URL)
