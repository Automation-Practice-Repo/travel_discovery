from fastapi import APIRouter
from app.api.v1.endpoints import search, place

api_router = APIRouter()
api_router.include_router(search.router, prefix="/search", tags=["search"])
api_router.include_router(place.router, prefix="/place", tags=["place"])
