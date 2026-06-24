from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.search import SearchRequest, SearchResponse
from app.services.discovery import discovery_service

router = APIRouter()

@router.post("/", response_model=SearchResponse, status_code=status.HTTP_200_OK)
async def search_attractions(
    payload: SearchRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Search tourist attractions in a given city within a specific radius (in km).
    Validates inputs, pulls from database cache or calls Google API if missing.
    """
    try:
        center, attractions = await discovery_service.search_city_attractions(
            location_name=payload.location_name,
            radius_km=payload.radius_km,
            db=db
        )
        return {
            "center": center,
            "results": attractions
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during discovery: {str(e)}"
        )

@router.get("/autocomplete", response_model=list[str], status_code=status.HTTP_200_OK)
async def get_autocomplete(
    q: str
):
    """
    Get autocomplete location suggestions based on the user input query string.
    """
    try:
        from app.services.google_maps import google_maps_service
        suggestions = await google_maps_service.get_autocomplete_suggestions(query=q)
        return suggestions
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Autocomplete search failed: {str(e)}"
        )
