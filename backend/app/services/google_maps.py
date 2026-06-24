import httpx
import logging
from typing import Dict, Any, List, Optional
import math
import random

from app.core.config import settings

logger = logging.getLogger("google_maps_service")

# Curated High-Fidelity Mock Data for Global Cities
MOCK_DATA: Dict[str, Dict[str, Any]] = {
    "paris": {
        "center": {"lat": 48.8566, "lng": 2.3522},
        "attractions": [
            {
                "place_id": "mock_paris_eiffel",
                "name": "Eiffel Tower",
                "description": "The iconic iron grid tower on the Champ de Mars, symbol of France and romance.",
                "address": "Champ de Mars, 5 Avenue Anatole France, 75007 Paris, France",
                "latitude": 48.8584,
                "longitude": 2.2945,
                "rating": 4.7,
                "user_ratings_total": 328000,
                "opening_hours": {
                    "weekday_text": [
                        "Monday: 9:30 AM – 10:45 PM",
                        "Tuesday: 9:30 AM – 10:45 PM",
                        "Wednesday: 9:30 AM – 10:45 PM",
                        "Thursday: 9:30 AM – 10:45 PM",
                        "Friday: 9:30 AM – 11:45 PM",
                        "Saturday: 9:30 AM – 11:45 PM",
                        "Sunday: 9:30 AM – 10:45 PM"
                    ],
                    "open_now": True
                },
                "image_url": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?auto=format&fit=crop&w=800&q=80"
            },
            {
                "place_id": "mock_paris_louvre",
                "name": "Louvre Museum",
                "description": "The world's largest art museum and a historic monument in Paris, home to the Mona Lisa.",
                "address": "Rue de Rivoli, 75001 Paris, France",
                "latitude": 48.8606,
                "longitude": 2.3376,
                "rating": 4.7,
                "user_ratings_total": 245000,
                "opening_hours": {
                    "weekday_text": [
                        "Monday: 9:00 AM – 6:00 PM",
                        "Tuesday: Closed",
                        "Wednesday: 9:00 AM – 6:00 PM",
                        "Thursday: 9:00 AM – 6:00 PM",
                        "Friday: 9:00 AM – 9:45 PM",
                        "Saturday: 9:00 AM – 6:00 PM",
                        "Sunday: 9:00 AM – 6:00 PM"
                    ],
                    "open_now": True
                },
                "image_url": "https://images.unsplash.com/photo-1601887389937-0b02c26b6c3c?auto=format&fit=crop&w=800&q=80"
            },
            {
                "place_id": "mock_paris_arc",
                "name": "Arc de Triomphe",
                "description": "One of the most famous monuments in Paris, standing at the western end of the Champs-Élysées.",
                "address": "Place Charles de Gaulle, 75008 Paris, France",
                "latitude": 48.8738,
                "longitude": 2.2950,
                "rating": 4.7,
                "user_ratings_total": 182000,
                "opening_hours": {
                    "weekday_text": [
                        "Monday: 10:00 AM – 11:00 PM",
                        "Tuesday: 10:00 AM – 11:00 PM",
                        "Wednesday: 10:00 AM – 11:00 PM",
                        "Thursday: 10:00 AM – 11:00 PM",
                        "Friday: 10:00 AM – 11:00 PM",
                        "Saturday: 10:00 AM – 11:00 PM",
                        "Sunday: 10:00 AM – 11:00 PM"
                    ],
                    "open_now": True
                },
                "image_url": "https://images.unsplash.com/photo-1509840141075-e5e6ff67854c?auto=format&fit=crop&w=800&q=80"
            },
            {
                "place_id": "mock_paris_notredame",
                "name": "Notre-Dame de Paris",
                "description": "A medieval Catholic cathedral on the Île de la Cité, exhibiting French Gothic architecture.",
                "address": "6 Parvis Notre-Dame - Pl. Jean-Paul II, 75004 Paris, France",
                "latitude": 48.8530,
                "longitude": 2.3499,
                "rating": 4.7,
                "user_ratings_total": 210000,
                "opening_hours": {
                    "weekday_text": [
                        "Monday: 8:00 AM – 6:45 PM",
                        "Tuesday: 8:00 AM – 6:45 PM",
                        "Wednesday: 8:00 AM – 6:45 PM",
                        "Thursday: 8:00 AM – 6:45 PM",
                        "Friday: 8:00 AM – 6:45 PM",
                        "Saturday: 8:00 AM – 6:45 PM",
                        "Sunday: 8:00 AM – 6:45 PM"
                    ],
                    "open_now": True
                },
                "image_url": "https://images.unsplash.com/photo-1478147427282-58a87a120781?auto=format&fit=crop&w=800&q=80"
            },
            {
                "place_id": "mock_paris_sacrecoeur",
                "name": "Sacré-Cœur Basilica",
                "description": "A Roman Catholic church and minor basilica, dedicated to the Sacred Heart of Jesus, located at the summit of Montmartre.",
                "address": "35 Rue du Chevalier de la Barre, 75018 Paris, France",
                "latitude": 48.8867,
                "longitude": 2.3431,
                "rating": 4.7,
                "user_ratings_total": 139000,
                "opening_hours": {
                    "weekday_text": [
                        "Monday: 6:00 AM – 10:30 PM",
                        "Tuesday: 6:00 AM – 10:30 PM",
                        "Wednesday: 6:00 AM – 10:30 PM",
                        "Thursday: 6:00 AM – 10:30 PM",
                        "Friday: 6:00 AM – 10:30 PM",
                        "Saturday: 6:00 AM – 10:30 PM",
                        "Sunday: 6:00 AM – 10:30 PM"
                    ],
                    "open_now": True
                },
                "image_url": "https://images.unsplash.com/photo-1503917988258-f87a78e3c995?auto=format&fit=crop&w=800&q=80"
            }
        ]
    },
    "rome": {
        "center": {"lat": 41.9028, "lng": 12.4964},
        "attractions": [
            {
                "place_id": "mock_rome_colosseum",
                "name": "Colosseum",
                "description": "The largest ancient amphitheatre ever built, located in the center of the city of Rome.",
                "address": "Piazza del Colosseo, 1, 00184 Roma RM, Italy",
                "latitude": 41.8902,
                "longitude": 12.4922,
                "rating": 4.8,
                "user_ratings_total": 352000,
                "opening_hours": {
                    "weekday_text": [
                        "Monday: 8:30 AM – 7:15 PM",
                        "Tuesday: 8:30 AM – 7:15 PM",
                        "Wednesday: 8:30 AM – 7:15 PM",
                        "Thursday: 8:30 AM – 7:15 PM",
                        "Friday: 8:30 AM – 7:15 PM",
                        "Saturday: 8:30 AM – 7:15 PM",
                        "Sunday: 8:30 AM – 7:15 PM"
                    ],
                    "open_now": True
                },
                "image_url": "https://images.unsplash.com/photo-1552832230-c0197dd311b5?auto=format&fit=crop&w=800&q=80"
            },
            {
                "place_id": "mock_rome_vatican",
                "name": "Vatican Museums",
                "description": "The public museums of Vatican City, displaying immense art collections accumulated by Popes, including the Sistine Chapel.",
                "address": "00120 Vatican City",
                "latitude": 41.9065,
                "longitude": 12.4536,
                "rating": 4.6,
                "user_ratings_total": 140000,
                "opening_hours": {
                    "weekday_text": [
                        "Monday: 9:00 AM – 6:00 PM",
                        "Tuesday: 9:00 AM – 6:00 PM",
                        "Wednesday: 9:00 AM – 6:00 PM",
                        "Thursday: 9:00 AM – 6:00 PM",
                        "Friday: 9:00 AM – 10:00 PM",
                        "Saturday: 9:00 AM – 6:00 PM",
                        "Sunday: Closed"
                    ],
                    "open_now": True
                },
                "image_url": "https://images.unsplash.com/photo-1542820229-081e0c12af0b?auto=format&fit=crop&w=800&q=80"
            },
            {
                "place_id": "mock_rome_trevi",
                "name": "Trevi Fountain",
                "description": "An 18th-century fountain in the Trevi district, designed by Nicola Salvi and one of the world's most famous fountains.",
                "address": "Piazza di Trevi, 00187 Roma RM, Italy",
                "latitude": 41.9009,
                "longitude": 12.4833,
                "rating": 4.8,
                "user_ratings_total": 298000,
                "opening_hours": {
                    "weekday_text": ["Open 24 hours a day, 7 days a week"],
                    "open_now": True
                },
                "image_url": "https://images.unsplash.com/photo-1525874684015-58379d421a52?auto=format&fit=crop&w=800&q=80"
            }
        ]
    },
    "tokyo": {
        "center": {"lat": 35.6762, "lng": 139.6503},
        "attractions": [
            {
                "place_id": "mock_tokyo_sensoji",
                "name": "Senso-ji",
                "description": "Tokyo's oldest and most famous Buddhist temple, situated in Asakusa.",
                "address": "2 Chome-3-1 Asakusa, Taito City, Tokyo 111-0032, Japan",
                "latitude": 35.7148,
                "longitude": 139.7967,
                "rating": 4.5,
                "user_ratings_total": 85000,
                "opening_hours": {
                    "weekday_text": ["Open 24 hours a day, 7 days a week"],
                    "open_now": True
                },
                "image_url": "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?auto=format&fit=crop&w=800&q=80"
            },
            {
                "place_id": "mock_tokyo_tower",
                "name": "Tokyo Tower",
                "description": "A communications and observation tower in the Shiba-koen district of Minato, Tokyo.",
                "address": "4 Chome-2-8 Shibakoen, Minato City, Tokyo 105-0011, Japan",
                "latitude": 35.6586,
                "longitude": 139.7454,
                "rating": 4.4,
                "user_ratings_total": 73000,
                "opening_hours": {
                    "weekday_text": [
                        "Monday: 9:00 AM – 11:00 PM",
                        "Tuesday: 9:00 AM – 11:00 PM",
                        "Wednesday: 9:00 AM – 11:00 PM",
                        "Thursday: 9:00 AM – 11:00 PM",
                        "Friday: 9:00 AM – 11:00 PM",
                        "Saturday: 9:00 AM – 11:00 PM",
                        "Sunday: 9:00 AM – 11:00 PM"
                    ],
                    "open_now": True
                },
                "image_url": "https://images.unsplash.com/photo-1540959733332-eab4deceeaf7?auto=format&fit=crop&w=800&q=80"
            },
            {
                "place_id": "mock_tokyo_shibuya",
                "name": "Shibuya Crossing",
                "description": "The world's busiest pedestrian scramble crossing, located in front of Shibuya Station.",
                "address": "Shibuya, Tokyo 150-0043, Japan",
                "latitude": 35.6595,
                "longitude": 139.7005,
                "rating": 4.5,
                "user_ratings_total": 42000,
                "opening_hours": {
                    "weekday_text": ["Open 24 hours a day, 7 days a week"],
                    "open_now": True
                },
                "image_url": "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?auto=format&fit=crop&w=800&q=80"
            }
        ]
    },
    "bangalore": {
        "center": {"lat": 12.9716, "lng": 77.5946},
        "attractions": [
            {
                "place_id": "mock_bangalore_palace",
                "name": "Bangalore Palace",
                "description": "A magnificent royal palace owned by the Mysore Royal Family, constructed in 1887 in Tudor Revival architecture style.",
                "address": "Vasanth Nagar, Bengaluru, Karnataka 560052, India",
                "latitude": 12.9982,
                "longitude": 77.5920,
                "rating": 4.5,
                "user_ratings_total": 52000,
                "opening_hours": {
                    "weekday_text": [
                        "Monday: 10:00 AM – 5:30 PM",
                        "Tuesday: 10:00 AM – 5:30 PM",
                        "Wednesday: 10:00 AM – 5:30 PM",
                        "Thursday: 10:00 AM – 5:30 PM",
                        "Friday: 10:00 AM – 5:30 PM",
                        "Saturday: 10:00 AM – 5:30 PM",
                        "Sunday: 10:00 AM – 5:30 PM"
                    ],
                    "open_now": True
                },
                "image_url": "https://images.unsplash.com/photo-1596176530529-78163a4f7af2?auto=format&fit=crop&w=800&q=80"
            },
            {
                "place_id": "mock_bangalore_lalbagh",
                "name": "Lalbagh Botanical Garden",
                "description": "An ancient, 240-acre botanical garden housing India's largest collection of tropical plants and an iconic Victorian-style glass house.",
                "address": "Mavalli, Bengaluru, Karnataka 560004, India",
                "latitude": 12.9507,
                "longitude": 77.5848,
                "rating": 4.4,
                "user_ratings_total": 45000,
                "opening_hours": {
                    "weekday_text": [
                        "Monday: 6:00 AM – 7:00 PM",
                        "Tuesday: 6:00 AM – 7:00 PM",
                        "Wednesday: 6:00 AM – 7:00 PM",
                        "Thursday: 6:00 AM – 7:00 PM",
                        "Friday: 6:00 AM – 7:00 PM",
                        "Saturday: 6:00 AM – 7:00 PM",
                        "Sunday: 6:00 AM – 7:00 PM"
                    ],
                    "open_now": True
                },
                "image_url": "https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?auto=format&fit=crop&w=800&q=80"
            },
            {
                "place_id": "mock_bangalore_cubbon",
                "name": "Cubbon Park",
                "description": "A historic, 300-acre park in the central administrative district, providing rich flora, walking paths, and colonial-era monuments.",
                "address": "Kasturba Road, Behind High Court, Bengaluru, Karnataka 560001, India",
                "latitude": 12.9739,
                "longitude": 77.5960,
                "rating": 4.5,
                "user_ratings_total": 38000,
                "opening_hours": {
                    "weekday_text": ["Open 24 hours, best visited: 6:00 AM - 8:00 PM"],
                    "open_now": True
                },
                "image_url": "https://images.unsplash.com/photo-1502082553048-f009c37129b9?auto=format&fit=crop&w=800&q=80"
            }
        ]
    },
    "mysore": {
        "center": {"lat": 12.2958, "lng": 76.6394},
        "attractions": [
            {
                "place_id": "mock_mysore_palace",
                "name": "Mysore Palace",
                "description": "An incredibly grand and historic palace, one of the most famous tourist destinations in India, and the official residence of the Wadiyar dynasty.",
                "address": "Sayyaji Rao Rd, Agrahara, Mysuru, Karnataka 570001, India",
                "latitude": 12.3051,
                "longitude": 76.6551,
                "rating": 4.6,
                "user_ratings_total": 85000,
                "opening_hours": {
                    "weekday_text": [
                        "Monday: 10:00 AM – 5:30 PM",
                        "Tuesday: 10:00 AM – 5:30 PM",
                        "Wednesday: 10:00 AM – 5:30 PM",
                        "Thursday: 10:00 AM – 5:30 PM",
                        "Friday: 10:00 AM – 5:30 PM",
                        "Saturday: 10:00 AM – 5:30 PM",
                        "Sunday: 10:00 AM – 5:30 PM"
                    ],
                    "open_now": True
                },
                "image_url": "https://images.unsplash.com/photo-1596176530529-78163a4f7af2?auto=format&fit=crop&w=800&q=80"
            },
            {
                "place_id": "mock_mysore_gardens",
                "name": "Brindavan Gardens",
                "description": "A famous ornamental garden adjoining the Krishnarajasagara Dam, renowned for its symmetric designs and musical dancing fountains.",
                "address": "KRS Dam Road, Mysuru, Karnataka 571607, India",
                "latitude": 12.3600,
                "longitude": 76.6000,
                "rating": 4.3,
                "user_ratings_total": 31000,
                "opening_hours": {
                    "weekday_text": [
                        "Monday: 7:00 AM – 8:00 PM",
                        "Tuesday: 7:00 AM – 8:00 PM",
                        "Wednesday: 7:00 AM – 8:00 PM",
                        "Thursday: 7:00 AM – 8:00 PM",
                        "Friday: 7:00 AM – 8:00 PM",
                        "Saturday: 7:00 AM – 8:00 PM",
                        "Sunday: 7:00 AM – 8:00 PM"
                    ],
                    "open_now": True
                },
                "image_url": "https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?auto=format&fit=crop&w=800&q=80"
            },
            {
                "place_id": "mock_mysore_chamundi",
                "name": "Chamundi Hill",
                "description": "A prominent hill overlooking the heritage city, topped by the ancient Chamundeshwari Temple dedicated to Goddess Durga.",
                "address": "Chamundi Hill, Mysuru, Karnataka 570010, India",
                "latitude": 12.2741,
                "longitude": 76.6710,
                "rating": 4.5,
                "user_ratings_total": 24000,
                "opening_hours": {
                    "weekday_text": ["Open 24 hours, best visited: 7:30 AM - 9:00 PM"],
                    "open_now": True
                },
                "image_url": "https://images.unsplash.com/photo-1608958214873-10d65a8cfdbd?auto=format&fit=crop&w=800&q=80"
            },
            {
                "place_id": "mock_mysore_zoo",
                "name": "Sri Chamarajendra Zoological Gardens",
                "description": "One of the oldest and most popular zoos in India, home to a wide range of exotic and native animal species.",
                "address": "Indiranagar, Mysuru, Karnataka 570010, India",
                "latitude": 12.3023,
                "longitude": 76.6660,
                "rating": 4.4,
                "user_ratings_total": 28000,
                "opening_hours": {
                    "weekday_text": [
                        "Monday: 8:30 AM – 5:30 PM",
                        "Tuesday: Closed",
                        "Wednesday: 8:30 AM – 5:30 PM",
                        "Thursday: 8:30 AM – 5:30 PM",
                        "Friday: 8:30 AM – 5:30 PM",
                        "Saturday: 8:30 AM – 5:30 PM",
                        "Sunday: 8:30 AM – 5:30 PM"
                    ],
                    "open_now": True
                },
                "image_url": "https://images.unsplash.com/photo-1534567153574-2b12153a87f0?auto=format&fit=crop&w=800&q=80"
            }
        ]
    }
}

class GoogleMapsService:
    def __init__(self):
        self.api_key = settings.GOOGLE_MAPS_API_KEY
        self.is_mock_mode = not bool(self.api_key)
        if self.is_mock_mode:
            logger.info("No GOOGLE_MAPS_API_KEY provided. Running in MOCK MODE.")
        else:
            logger.info("GOOGLE_MAPS_API_KEY detected. Running in LIVE MODE.")

    def _get_mock_city(self, query: str) -> str:
        """Helper to resolve a text query to a mock city name, dynamically generating data if unknown."""
        q = query.lower().strip()
        
        # Check standard mappings first
        if "paris" in q:
            return "paris"
        elif "rome" in q:
            return "rome"
        elif "tokyo" in q:
            return "tokyo"
        elif "bangalore" in q or "banglore" in q or "bengaluru" in q:
            return "bangalore"
        elif "mysore" in q or "mysuru" in q:
            return "mysore"
            
        # If not found, check if we already dynamically generated it
        if q in MOCK_DATA:
            return q
            
        # Generate new mock city dynamically
        city_name = query.strip().capitalize()
        
        # Deterministic coordinates based on character sum
        char_sum = sum(ord(c) for c in q)
        
        # Define some exact coordinates for common test cities
        exact_coords = {
            "london": {"lat": 51.5074, "lng": -0.1278},
            "new york": {"lat": 40.7128, "lng": -74.0060},
            "sydney": {"lat": -33.8688, "lng": 151.2093},
            "mumbai": {"lat": 19.0760, "lng": 72.8777},
            "delhi": {"lat": 28.7041, "lng": 77.1025},
            "mysore": {"lat": 12.2958, "lng": 76.6394},
            "mysuru": {"lat": 12.2958, "lng": 76.6394},
        }
        
        # Try finding exact matches, else derive deterministically
        center_coords = None
        for k, v in exact_coords.items():
            if k in q:
                center_coords = v
                break
                
        if center_coords:
            lat = center_coords["lat"]
            lng = center_coords["lng"]
        else:
            # Deterministic lat in range [-35, 55] and lng in range [-80, 130]
            lat = ((char_sum % 900) / 10.0) - 35.0
            lng = ((char_sum // 9 % 2100) / 10.0) - 80.0
            
        # Ensure coordinates are within standard bounds
        lat = max(-90.0, min(90.0, lat))
        lng = max(-180.0, min(180.0, lng))
        
        # Add to MOCK_DATA
        MOCK_DATA[q] = {
            "center": {"lat": lat, "lng": lng},
            "attractions": [
                {
                    "place_id": f"mock_dynamic_{q}_palace",
                    "name": f"{city_name} Palace",
                    "description": f"A historic royal residence representing the unique heritage and local architecture of {city_name}.",
                    "address": f"Palace Road, {city_name}",
                    "latitude": lat + 0.012,
                    "longitude": lng - 0.015,
                    "rating": 4.6,
                    "user_ratings_total": (char_sum % 450) + 50,
                    "opening_hours": {
                        "weekday_text": ["Monday - Sunday: 9:00 AM – 5:30 PM"],
                        "open_now": True
                    },
                    "image_url": "https://images.unsplash.com/photo-1596176530529-78163a4f7af2?auto=format&fit=crop&w=800&q=80"
                },
                {
                    "place_id": f"mock_dynamic_{q}_garden",
                    "name": f"{city_name} Botanical Garden",
                    "description": f"A scenic public park containing native flora, walking paths, and conservatory glass structures.",
                    "address": f"Garden Avenue, {city_name}",
                    "latitude": lat - 0.018,
                    "longitude": lng + 0.011,
                    "rating": 4.4,
                    "user_ratings_total": (char_sum % 380) + 30,
                    "opening_hours": {
                        "weekday_text": ["Monday - Sunday: 6:00 AM – 7:00 PM"],
                        "open_now": True
                    },
                    "image_url": "https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?auto=format&fit=crop&w=800&q=80"
                },
                {
                    "place_id": f"mock_dynamic_{q}_museum",
                    "name": f"{city_name} National Museum",
                    "description": f"A premium cultural museum exhibiting local historical artifacts, scientific galleries, and art collections.",
                    "address": f"Museum Square, {city_name}",
                    "latitude": lat + 0.005,
                    "longitude": lng + 0.017,
                    "rating": 4.5,
                    "user_ratings_total": (char_sum % 290) + 20,
                    "opening_hours": {
                        "weekday_text": ["Tuesday - Sunday: 10:00 AM – 6:00 PM", "Monday: Closed"],
                        "open_now": True
                    },
                    "image_url": "https://images.unsplash.com/photo-1560697529-7236591c0066?auto=format&fit=crop&w=800&q=80"
                },
                {
                    "place_id": f"mock_dynamic_{q}_landmark",
                    "name": f"{city_name} Historic Landmark",
                    "description": f"An iconic structural tower and landmark offering panoramic city vistas and rich historical heritage.",
                    "address": f"Hilltop Crest, {city_name}",
                    "latitude": lat - 0.009,
                    "longitude": lng - 0.022,
                    "rating": 4.7,
                    "user_ratings_total": (char_sum % 580) + 10,
                    "opening_hours": {
                        "weekday_text": ["Open 24 hours, best visited during daytime"],
                        "open_now": True
                    },
                    "image_url": "https://images.unsplash.com/photo-1502082553048-f009c37129b9?auto=format&fit=crop&w=800&q=80"
                }
            ]
        }
        
        return q

    def _haversine_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate the great-circle distance between two points in km."""
        R = 6371.0  # Earth's radius in kilometers
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (math.sin(dlat / 2) ** 2 +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    async def geocode_city(self, city_name: str) -> Dict[str, Any]:
        """Geocodes a city/location name to retrieve lat/lng coordinates."""
        if self.is_mock_mode:
            city_key = self._get_mock_city(city_name)
            center = MOCK_DATA[city_key]["center"]
            # Standardized return schema matching google response structure
            resolved_title = city_name.strip().capitalize()
            return {
                "location_name": resolved_title,
                "latitude": center["lat"],
                "longitude": center["lng"],
                "formatted_address": f"{resolved_title}"
            }

        # Live Google Geocoding API call
        async with httpx.AsyncClient() as client:
            url = "https://maps.googleapis.com/maps/api/geocode/json"
            params = {"address": city_name, "key": self.api_key}
            response = await client.get(url)
            data = response.json()
            
            if data.get("status") == "OK" and data.get("results"):
                result = data["results"][0]
                geometry = result["geometry"]["location"]
                return {
                    "location_name": result["address_components"][0]["long_name"],
                    "latitude": geometry["lat"],
                    "longitude": geometry["lng"],
                    "formatted_address": result["formatted_address"]
                }
            else:
                raise ValueError(f"Geocoding failed for '{city_name}': {data.get('status')}")

    async def search_attractions(self, lat: float, lng: float, radius_km: float, query_city: str) -> List[Dict[str, Any]]:
        """Searches tourist attractions within the given radius."""
        if self.is_mock_mode:
            city_key = self._get_mock_city(query_city)
            city_data = MOCK_DATA[city_key]
            results = []
            for attr in city_data["attractions"]:
                dist = self._haversine_distance(lat, lng, attr["latitude"], attr["longitude"])
                if dist <= radius_km:
                    results.append(attr)
            return results

        # Live Google Places API call
        # Using standard Places Text Search API
        async with httpx.AsyncClient() as client:
            url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
            # Google Places API radius is in meters
            radius_meters = int(radius_km * 1000)
            params = {
                "query": "tourist attraction",
                "location": f"{lat},{lng}",
                "radius": radius_meters,
                "key": self.api_key
            }
            response = await client.get(url)
            data = response.json()
            
            attractions = []
            if data.get("status") in ["OK", "ZERO_RESULTS"] and data.get("results"):
                for result in data["results"][:15]:  # limit to top 15 results
                    geom = result["geometry"]["location"]
                    
                    # Resolve Place Photos API URL if reference exists
                    image_url = None
                    if result.get("photos"):
                        photo_ref = result["photos"][0]["photo_reference"]
                        image_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=600&photo_reference={photo_ref}&key={self.api_key}"
                    else:
                        # Fallback placeholder travel image
                        image_url = "https://images.unsplash.com/photo-1488646953014-85cb44e25828?auto=format&fit=crop&w=600&q=80"

                    attractions.append({
                        "place_id": result["place_id"],
                        "name": result["name"],
                        "description": result.get("formatted_address", ""),
                        "address": result.get("formatted_address", ""),
                        "latitude": geom["lat"],
                        "longitude": geom["lng"],
                        "rating": result.get("rating"),
                        "user_ratings_total": result.get("user_ratings_total", 0),
                        "opening_hours": result.get("opening_hours", {"open_now": True}),
                        "image_url": image_url
                    })
            return attractions

    async def get_place_details(self, place_id: str) -> Dict[str, Any]:
        """Fetches detailed information for a single attraction."""
        if self.is_mock_mode:
            # Locate attraction in mock dictionary
            for city in MOCK_DATA.values():
                for attr in city["attractions"]:
                    if attr["place_id"] == place_id:
                        return attr
            raise ValueError(f"Mock place '{place_id}' not found.")

        # Live Google Place Details call
        async with httpx.AsyncClient() as client:
            url = "https://maps.googleapis.com/maps/api/place/details/json"
            fields = "name,formatted_address,geometry,rating,user_ratings_total,opening_hours,photos,editorial_summary"
            params = {
                "place_id": place_id,
                "fields": fields,
                "key": self.api_key
            }
            response = await client.get(url)
            data = response.json()
            
            if data.get("status") == "OK" and data.get("result"):
                result = data["result"]
                geom = result["geometry"]["location"]
                
                # Fetch description
                description = result.get("formatted_address", "")
                if result.get("editorial_summary"):
                    description = result["editorial_summary"].get("overview", description)

                # Set up image
                image_url = None
                if result.get("photos"):
                    photo_ref = result["photos"][0]["photo_reference"]
                    image_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=800&photo_reference={photo_ref}&key={self.api_key}"
                else:
                    image_url = "https://images.unsplash.com/photo-1488646953014-85cb44e25828?auto=format&fit=crop&w=800&q=80"

                return {
                    "place_id": place_id,
                    "name": result["name"],
                    "description": description,
                    "address": result.get("formatted_address"),
                    "latitude": geom["lat"],
                    "longitude": geom["lng"],
                    "rating": result.get("rating"),
                    "user_ratings_total": result.get("user_ratings_total", 0),
                    "opening_hours": result.get("opening_hours", {"open_now": True}),
                    "image_url": image_url
                }
            else:
                raise ValueError(f"Details fetch failed for place_id '{place_id}': {data.get('status')}")

    async def get_directions(
        self, origin_lat: float, origin_lng: float, dest_lat: float, dest_lng: float, dest_place_id: str
    ) -> Dict[str, Any]:
        """Calculates distance, travel time, and routes/directions."""
        if self.is_mock_mode:
            # Generate mock distance and travel time based on coordinates
            dist_km = self._haversine_distance(origin_lat, origin_lng, dest_lat, dest_lng)
            
            # Speed estimate: ~40 km/h average city traffic speed
            travel_time_min = int((dist_km / 40.0) * 60) + 3 # Add a offset
            if travel_time_min < 2:
                travel_time_min = 5

            # Mock step-by-step navigation instructions
            steps = [
                f"Head north from City Center towards target location.",
                f"After {round(dist_km*0.3, 1)} km, turn right onto main street.",
                f"Continue straight for {round(dist_km*0.5, 1)} km.",
                f"At the roundabout, take the 2nd exit.",
                f"Destination will be on the right in {round(dist_km*0.2, 1)} km."
            ]

            # Generate simple path points (polyline equivalent) between center and destination
            # We construct a 10-point interpolation path with some slight noise to look like roads
            path = []
            steps_count = 10
            for i in range(steps_count + 1):
                t = i / steps_count
                # Line interpolation
                curr_lat = origin_lat + t * (dest_lat - origin_lat)
                curr_lng = origin_lng + t * (dest_lng - origin_lng)
                
                # Add minor curves for visualization, except at ends
                if 0 < i < steps_count:
                    curr_lat += math.sin(t * math.pi) * 0.002 * random.choice([-1, 1])
                    curr_lng += math.cos(t * math.pi) * 0.002 * random.choice([-1, 1])
                
                path.append({"lat": curr_lat, "lng": curr_lng})

            return {
                "distance": f"{round(dist_km, 1)} km",
                "duration": f"{travel_time_min} mins",
                "duration_seconds": travel_time_min * 60,
                "steps": steps,
                "polyline_points": path,
                "navigation_url": f"https://www.google.com/maps/dir/?api=1&origin={origin_lat},{origin_lng}&destination={dest_lat},{dest_lng}&destination_place_id={dest_place_id}&travelmode=driving"
            }

        # Live Google Directions API Call
        async with httpx.AsyncClient() as client:
            url = "https://maps.googleapis.com/maps/api/directions/json"
            params = {
                "origin": f"{origin_lat},{origin_lng}",
                "destination": f"{dest_lat},{dest_lng}",
                "mode": "driving",
                "key": self.api_key
            }
            response = await client.get(url)
            data = response.json()
            
            if data.get("status") == "OK" and data.get("routes"):
                route = data["routes"][0]
                leg = route["legs"][0]
                
                # Extract step by step instructions (removing HTML tags)
                import re
                steps = []
                for step in leg["steps"]:
                    clean_instruction = re.sub('<[^<]+?>', '', step["html_instructions"])
                    steps.append(clean_instruction)

                # Decode polyline points into lat/lng path (simplified for UI)
                # To avoid writing a full polyline decoder here, we can return the encoded polyline string
                # and decode it in the frontend, OR return the raw step coordinates.
                # Let's pass the raw steps starts/ends coordinates, and the encoded polyline itself.
                encoded_polyline = route["overview_polyline"]["points"]

                return {
                    "distance": leg["distance"]["text"],
                    "duration": leg["duration"]["text"],
                    "duration_seconds": leg["duration"]["value"],
                    "steps": steps,
                    "encoded_polyline": encoded_polyline,
                    "navigation_url": f"https://www.google.com/maps/dir/?api=1&origin={origin_lat},{origin_lng}&destination={dest_lat},{dest_lng}&destination_place_id={dest_place_id}&travelmode=driving"
                }
            else:
                # Fallback to simple straight line route if directions fail
                dist_km = self._haversine_distance(origin_lat, origin_lng, dest_lat, dest_lng)
                duration_min = int((dist_km / 40) * 60) + 5
                return {
                    "distance": f"{round(dist_km, 1)} km",
                    "duration": f"{duration_min} mins",
                    "duration_seconds": duration_min * 60,
                    "steps": ["Head straight toward your destination."],
                    "polyline_points": [{"lat": origin_lat, "lng": origin_lng}, {"lat": dest_lat, "lng": dest_lng}],
                    "navigation_url": f"https://www.google.com/maps/dir/?api=1&origin={origin_lat},{origin_lng}&destination={dest_lat},{dest_lng}"
                }

    async def get_autocomplete_suggestions(self, query: str) -> List[str]:
        """Fetches auto-complete suggestions based on user query string."""
        if not query or len(query.strip()) < 1:
            return []

        q = query.lower().strip()

        if self.is_mock_mode:
            mock_suggestions = [
                "Bangalore, Karnataka, India",
                "Anantapur, Andhra Pradesh, India",
                "Mysore, Karnataka, India",
                "Paris, Île-de-France, France",
                "Rome, Lazio, Italy",
                "Tokyo, Kanto, Japan",
                "London, Greater London, United Kingdom",
                "New York, NY, United States",
                "Sydney, New South Wales, Australia",
                "Mumbai, Maharashtra, India",
                "Delhi, National Capital Territory of Delhi, India",
                "Chennai, Tamil Nadu, India",
                "Hyderabad, Telangana, India",
                "Kochi, Kerala, India",
                "Goa, India",
            ]
            matches = [city for city in mock_suggestions if q in city.lower()]
            return matches[:5]

        # Live Google Autocomplete API call
        async with httpx.AsyncClient() as client:
            url = "https://maps.googleapis.com/maps/api/place/autocomplete/json"
            params = {
                "input": query,
                "types": "(cities)",
                "key": self.api_key
            }
            response = await client.get(url)
            data = response.json()
            
            suggestions = []
            if data.get("status") == "OK" and data.get("predictions"):
                for prediction in data["predictions"]:
                    suggestions.append(prediction["description"])
            return suggestions

google_maps_service = GoogleMapsService()
