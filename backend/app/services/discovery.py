import logging
from typing import Dict, Any, List, Tuple
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.attraction_repo import AttractionRepository
from app.services.google_maps import google_maps_service
from app.services.cache import cache_service
from app.models.attraction import Attraction

logger = logging.getLogger("discovery_service")

class DiscoveryService:
    async def search_city_attractions(
        self, location_name: str, radius_km: float, db: AsyncSession
    ) -> Tuple[Dict[str, Any], List[Attraction]]:
        """
        Orchestrates search for tourist attractions:
        1. Checks database for matching query (same name and radius).
        2. Checks Redis cache for cached attractions of that query.
        3. If not found, calls Google Maps API for geocoding and place search.
        4. Upserts attractions and query to database.
        5. Caches in Redis and returns.
        """
        repo = AttractionRepository(db)

        # 1. Check if this exact search has been performed
        existing_query = await repo.get_search_query(location_name, radius_km)
        
        if existing_query:
            logger.info(f"Cache hit in DB for search: '{location_name}' with radius {radius_km}km")
            
            # Check Redis for attractions mapping
            cache_key = f"search_results:{existing_query.id}"
            cached_attractions = await cache_service.get(cache_key)
            
            if cached_attractions:
                logger.info(f"Cache hit in Redis for key: {cache_key}")
                # Convert back to Attraction models
                attraction_models = [Attraction(**attr) for attr in cached_attractions]
                
                center = {
                    "location_name": existing_query.location_name,
                    "latitude": existing_query.latitude,
                    "longitude": existing_query.longitude,
                    "radius_km": existing_query.radius_km
                }
                return center, attraction_models

            # If in DB but not Redis, write back to Redis
            logger.info(f"Redis cache miss, loading from DB relationships")
            attraction_models = existing_query.attractions
            
            # Write to cache (serialize models to dicts)
            serialized_attractions = [
                {
                    "place_id": att.place_id,
                    "name": att.name,
                    "description": att.description,
                    "address": att.address,
                    "latitude": att.latitude,
                    "longitude": att.longitude,
                    "rating": att.rating,
                    "user_ratings_total": att.user_ratings_total,
                    "opening_hours": att.opening_hours,
                    "image_url": att.image_url
                }
                for att in attraction_models
            ]
            await cache_service.set(cache_key, serialized_attractions, expire_seconds=86400) # 24 hours
            
            center = {
                "location_name": existing_query.location_name,
                "latitude": existing_query.latitude,
                "longitude": existing_query.longitude,
                "radius_km": existing_query.radius_km
            }
            return center, attraction_models

        # 2. Search miss -> Call Geocoding + Google Places
        logger.info(f"Cache miss. Fetching live/mock data for '{location_name}'")
        
        # Geocode the city center
        geocode_res = await google_maps_service.geocode_city(location_name)
        lat = geocode_res["latitude"]
        lng = geocode_res["longitude"]
        resolved_name = geocode_res["location_name"]

        # Find attractions
        raw_attractions = await google_maps_service.search_attractions(
            lat, lng, radius_km, resolved_name
        )

        # Upsert attractions in Database
        upserted_attractions = await repo.upsert_attractions(raw_attractions)

        # Create SearchQuery record with relation to attractions
        search_query = await repo.create_search_query(
            location_name=resolved_name,
            latitude=lat,
            longitude=lng,
            radius_km=radius_km,
            attractions=upserted_attractions
        )

        # Cache results in Redis
        cache_key = f"search_results:{search_query.id}"
        serialized_attractions = [
            {
                "place_id": att.place_id,
                "name": att.name,
                "description": att.description,
                "address": att.address,
                "latitude": att.latitude,
                "longitude": att.longitude,
                "rating": att.rating,
                "user_ratings_total": att.user_ratings_total,
                "opening_hours": att.opening_hours,
                "image_url": att.image_url
            }
            for att in upserted_attractions
        ]
        await cache_service.set(cache_key, serialized_attractions, expire_seconds=86400)

        center = {
            "location_name": resolved_name,
            "latitude": lat,
            "longitude": lng,
            "radius_km": radius_km
        }
        return center, upserted_attractions

    async def get_attraction_details(self, place_id: str, db: AsyncSession) -> Attraction:
        """Gets complete details of a specific tourist place."""
        repo = AttractionRepository(db)
        
        # Check database first
        attraction = await repo.get_by_place_id(place_id)
        if attraction:
            # If details are stale or missing description, trigger detail update
            if not attraction.description:
                details = await google_maps_service.get_place_details(place_id)
                attraction = await repo.update(attraction, details)
            return attraction
            
        # Fetch from Google API / Mock
        details = await google_maps_service.get_place_details(place_id)
        attraction = Attraction(**details)
        await repo.create(attraction)
        return attraction

discovery_service = DiscoveryService()
