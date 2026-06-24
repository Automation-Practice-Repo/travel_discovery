import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export interface Attraction {
  place_id: string
  name: string
  description: string | null
  address: string | null
  latitude: number
  longitude: number
  rating: number | null
  user_ratings_total: number | null
  opening_hours: {
    weekday_text?: string[]
    open_now?: boolean
  } | null
  image_url: string | null
}

export interface SearchCenter {
  location_name: string
  latitude: number
  longitude: number
  radius_km: number
}

export interface SearchResponse {
  center: SearchCenter
  results: Attraction[]
}

export interface DirectionsRequest {
  origin_lat: number
  origin_lng: number
  destination_lat: number
  destination_lng: number
  destination_place_id: string
}

export interface DirectionsResponse {
  distance: string
  duration: string
  duration_seconds: number
  steps: string[]
  polyline_points?: { lat: number; lng: number }[]
  encoded_polyline?: string
  navigation_url: string
}

export const searchAttractions = async (locationName: string, radiusKm: number): Promise<SearchResponse> => {
  const response = await apiClient.post<SearchResponse>('/search/', {
    location_name: locationName,
    radius_km: radiusKm,
  })
  return response.data
}

export const getPlaceDetails = async (placeId: string): Promise<Attraction> => {
  const response = await apiClient.get<Attraction>(`/place/${placeId}`)
  return response.data
}

export const getDirections = async (payload: DirectionsRequest): Promise<DirectionsResponse> => {
  const response = await apiClient.post<DirectionsResponse>('/place/directions', payload)
  return response.data
}

export const getAutocompleteSuggestions = async (q: string): Promise<string[]> => {
  if (!q || q.trim().length === 0) return []
  const response = await apiClient.get<string[]>('/search/autocomplete', {
    params: { q },
  })
  return response.data
}
