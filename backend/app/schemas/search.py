from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator
from app.schemas.attraction import AttractionResponse

class SearchRequest(BaseModel):
    location_name: str = Field(..., min_length=2, max_length=100, description="City or location name to search in")
    radius_km: float = Field(..., ge=1.0, le=50.0, description="Search radius in kilometers")

    @field_validator("location_name")
    @classmethod
    def clean_location_name(cls, v: str) -> str:
        cleaned = v.strip()
        if not cleaned:
            raise ValueError("Location name cannot be empty or just whitespace.")
        return cleaned

class SearchCenter(BaseModel):
    location_name: str
    latitude: float
    longitude: float
    radius_km: float

class SearchResponse(BaseModel):
    center: SearchCenter
    results: List[AttractionResponse]

class DirectionsRequest(BaseModel):
    origin_lat: float = Field(..., ge=-90.0, le=90.0)
    origin_lng: float = Field(..., ge=-180.0, le=180.0)
    destination_lat: float = Field(..., ge=-90.0, le=90.0)
    destination_lng: float = Field(..., ge=-180.0, le=180.0)
    destination_place_id: str = Field(..., description="Target place Google place_id")

class DirectionsStep(BaseModel):
    instruction: str

class DirectionsResponse(BaseModel):
    distance: str
    duration: str
    duration_seconds: int
    steps: List[str]
    polyline_points: Optional[List[Dict[str, float]]] = None
    encoded_polyline: Optional[str] = None
    navigation_url: str
