from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.attraction import AttractionResponse
from app.schemas.search import DirectionsRequest, DirectionsResponse
from app.services.discovery import discovery_service
from app.services.google_maps import google_maps_service

router = APIRouter()

@router.get("/{place_id}", response_model=AttractionResponse, status_code=status.HTTP_200_OK)
async def get_place_details(
    place_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Fetches comprehensive attraction details including images, ratings, opening hours,
    and description. Integrates Google Places Details.
    """
    try:
        attraction = await discovery_service.get_attraction_details(place_id=place_id, db=db)
        return attraction
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to load place details: {str(e)}"
        )

@router.post("/directions", response_model=DirectionsResponse, status_code=status.HTTP_200_OK)
async def get_directions(
    payload: DirectionsRequest
):
    """
    Calculates distance, travel duration, steps, and polyline coordinate route
    between search origin and destination attraction.
    """
    try:
        directions = await google_maps_service.get_directions(
            origin_lat=payload.origin_lat,
            origin_lng=payload.origin_lng,
            dest_lat=payload.destination_lat,
            dest_lng=payload.destination_lng,
            dest_place_id=payload.destination_place_id
        )
        return directions
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch route directions: {str(e)}"
        )
