from typing import List, Optional
import uuid
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy import delete

from app.repositories.base import BaseRepository
from app.models.attraction import Attraction, SearchQuery, search_query_association

class AttractionRepository(BaseRepository[Attraction]):
    def __init__(self, db: AsyncSession):
        super().__init__(Attraction, db)

    async def get_by_place_id(self, place_id: str) -> Optional[Attraction]:
        return await self.get(place_id)

    async def get_by_place_ids(self, place_ids: List[str]) -> List[Attraction]:
        query = select(Attraction).where(Attraction.place_id.in_(place_ids))
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_search_query(
        self, location_name: str, radius_km: float
    ) -> Optional[SearchQuery]:
        # Perform case-insensitive match on location_name and within same radius
        # Radius check can be within a small delta (e.g. 0.1km)
        query = (
            select(SearchQuery)
            .where(
                SearchQuery.location_name.ilike(location_name),
                SearchQuery.radius_km == radius_km
            )
            .options(selectinload(SearchQuery.attractions))
            .order_by(SearchQuery.created_at.desc())
            .limit(1)
        )
        result = await self.db.execute(query)
        return result.scalars().first()

    async def create_search_query(
        self,
        location_name: str,
        latitude: float,
        longitude: float,
        radius_km: float,
        attractions: List[Attraction]
    ) -> SearchQuery:
        search_query = SearchQuery(
            location_name=location_name,
            latitude=latitude,
            longitude=longitude,
            radius_km=radius_km,
            attractions=attractions
        )
        self.db.add(search_query)
        await self.db.flush()
        return search_query

    async def upsert_attractions(self, attractions_in: List[dict]) -> List[Attraction]:
        """
        Upserts multiple attractions. Handles conflicts on primary key place_id.
        """
        attractions = []
        for att_data in attractions_in:
            place_id = att_data["place_id"]
            existing = await self.get_by_place_id(place_id)
            if existing:
                # Update existing
                updated = await self.update(existing, att_data)
                attractions.append(updated)
            else:
                # Create new
                new_att = Attraction(**att_data)
                created = await self.create(new_att)
                attractions.append(created)
        return attractions
