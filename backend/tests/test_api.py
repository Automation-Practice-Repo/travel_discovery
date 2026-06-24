import pytest
from httpx import AsyncClient
from fastapi import status

@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "online"
    assert "mock_mode" in data

@pytest.mark.asyncio
async def test_search_attractions_valid(client: AsyncClient):
    payload = {
        "location_name": "Paris",
        "radius_km": 10.0
    }
    response = await client.post("/api/v1/search/", json=payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # Check geocoding center details
    assert "center" in data
    assert data["center"]["location_name"].lower() == "paris"
    assert data["center"]["radius_km"] == 10.0
    
    # Check results are present
    assert "results" in data
    assert len(data["results"]) > 0
    first_attraction = data["results"][0]
    assert "place_id" in first_attraction
    assert "name" in first_attraction
    assert "latitude" in first_attraction

@pytest.mark.asyncio
async def test_search_attractions_invalid_radius(client: AsyncClient):
    payload = {
        "location_name": "Paris",
        "radius_km": 60.0 # Invalid (max 50)
    }
    response = await client.post("/api/v1/search/", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

@pytest.mark.asyncio
async def test_search_attractions_empty_location(client: AsyncClient):
    payload = {
        "location_name": "",
        "radius_km": 10.0
    }
    response = await client.post("/api/v1/search/", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

@pytest.mark.asyncio
async def test_get_place_details_valid(client: AsyncClient):
    # Ensure attraction is searchable first
    await client.post("/api/v1/search/", json={"location_name": "Paris", "radius_km": 15.0})
    
    # Fetch details for Eiffel Tower
    place_id = "mock_paris_eiffel"
    response = await client.get(f"/api/v1/place/{place_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["place_id"] == place_id
    assert data["name"] == "Eiffel Tower"
    assert data["rating"] == 4.7

@pytest.mark.asyncio
async def test_get_place_details_not_found(client: AsyncClient):
    response = await client.get("/api/v1/place/non_existent_place_id")
    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.asyncio
async def test_get_directions_valid(client: AsyncClient):
    payload = {
        "origin_lat": 48.8566,
        "origin_lng": 2.3522,
        "destination_lat": 48.8584,
        "destination_lng": 2.2945,
        "destination_place_id": "mock_paris_eiffel"
    }
    response = await client.post("/api/v1/place/directions", json=payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "distance" in data
    assert "duration" in data
    assert "steps" in data
    assert len(data["steps"]) > 0
    assert "navigation_url" in data

@pytest.mark.asyncio
async def test_autocomplete_valid(client: AsyncClient):
    response = await client.get("/api/v1/search/autocomplete?q=ban")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert any("Bangalore" in item for item in data)

