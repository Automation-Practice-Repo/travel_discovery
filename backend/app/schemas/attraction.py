from typing import Optional, List
from pydantic import BaseModel, ConfigDict

class AttractionBase(BaseModel):
    place_id: str
    name: str
    description: Optional[str] = None
    address: Optional[str] = None
    latitude: float
    longitude: float
    rating: Optional[float] = None
    user_ratings_total: Optional[int] = 0
    opening_hours: Optional[dict] = None
    image_url: Optional[str] = None

class AttractionCreate(AttractionBase):
    pass

class AttractionResponse(AttractionBase):
    model_config = ConfigDict(from_attributes=True)
