import React, { useState, useRef } from 'react'
import { GoogleMap, useJsApiLoader, Marker, Polyline, InfoWindow } from '@react-google-maps/api'
import { motion } from 'framer-motion'
import { Navigation, Compass, MapPin } from 'lucide-react'
import { useSearch } from '../context/SearchContext'
import type { Attraction } from '../services/api'

// Styles for live Google Maps to match luxury dark theme
const darkMapStyle = [
  { elementType: "geometry", stylers: [{ color: "#0f172a" }] },
  { elementType: "labels.text.stroke", stylers: [{ color: "#0f172a" }, { weight: 2 }] },
  { elementType: "labels.text.fill", stylers: [{ color: "#94a3b8" }] },
  { featureType: "administrative.locality", elementType: "labels.text.fill", stylers: [{ color: "#cbd5e1" }] },
  { featureType: "poi", elementType: "labels.text.fill", stylers: [{ color: "#64748b" }] },
  { featureType: "poi.park", elementType: "geometry", stylers: [{ color: "#1e293b" }] },
  { featureType: "poi.park", elementType: "labels.text.fill", stylers: [{ color: "#475569" }] },
  { featureType: "road", elementType: "geometry", stylers: [{ color: "#1e293b" }] },
  { featureType: "road", elementType: "geometry.stroke", stylers: [{ color: "#0f172a" }] },
  { featureType: "road", elementType: "labels.text.fill", stylers: [{ color: "#475569" }] },
  { featureType: "road.highway", elementType: "geometry", stylers: [{ color: "#334155" }] },
  { featureType: "road.highway", elementType: "geometry.stroke", stylers: [{ color: "#0f172a" }] },
  { featureType: "water", elementType: "geometry", stylers: [{ color: "#020617" }] },
  { featureType: "water", elementType: "labels.text.fill", stylers: [{ color: "#1e293b" }] },
]

export const MapContainer: React.FC = () => {
  const {
    searchCenter,
    attractions,
    selectedAttraction,
    setSelectedAttraction,
    directions
  } = useSearch()

  const apiKey = import.meta.env.VITE_GOOGLE_MAPS_API_KEY || ''
  const isMockMode = !apiKey

  const [activePin, setActivePin] = useState<Attraction | null>(null)

  // 1. Google Maps SDK loader (runs if API key is present)
  const { isLoaded } = useJsApiLoader({
    googleMapsApiKey: apiKey,
    id: 'google-map-script',
  })

  // Map configuration
  const mapCenter = searchCenter
    ? { lat: searchCenter.latitude, lng: searchCenter.longitude }
    : { lat: 48.8566, lng: 2.3522 } // Paris default

  // Decode live Google Maps encoded overview polyline
  const decodePolyline = (encoded: string) => {
    if (!encoded) return []
    let len = encoded.length
    let index = 0
    let array = []
    let lat = 0
    let lng = 0

    while (index < len) {
      let b
      let shift = 0
      let result = 0
      do {
        b = encoded.charCodeAt(index++) - 63
        result |= (b & 0x1f) << shift
        shift += 5
      } while (b >= 0x20)
      let dlat = ((result & 1) ? ~(result >> 1) : (result >> 1))
      lat += dlat

      shift = 0
      result = 0
      do {
        b = encoded.charCodeAt(index++) - 63
        result |= (b & 0x1f) << shift
        shift += 5
      } while (b >= 0x20)
      let dlng = ((result & 1) ? ~(result >> 1) : (result >> 1))
      lng += dlng

      array.push({ lat: lat * 1e-5, lng: lng * 1e-5 })
    }
    return array
  }

  // Compile path points for polyline routing
  const polylinePath = directions?.encoded_polyline
    ? decodePolyline(directions.encoded_polyline)
    : directions?.polyline_points
      ? directions.polyline_points
      : []

  // ----------------------------------------------------
  // RENDER OPTION A: Live Google Map
  // ----------------------------------------------------
  if (!isMockMode && isLoaded) {
    return (
      <div className="w-full h-full relative bg-slate-905">
        <GoogleMap
          mapContainerClassName="w-full h-full"
          center={mapCenter}
          zoom={13}
          options={{
            styles: darkMapStyle,
            disableDefaultUI: true,
            zoomControl: true,
          }}
        >
          {/* Main search origin marker */}
          {searchCenter && (
            <Marker
              position={mapCenter}
              icon={{
                path: 'M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z',
                fillColor: '#8b5cf6', // Violet
                fillOpacity: 1,
                strokeColor: '#ffffff',
                strokeWeight: 2,
                scale: 1.5,
                anchor: new google.maps.Point(12, 21),
              }}
            />
          )}

          {/* Attraction Pin Markers */}
          {attractions.map((att) => (
            <Marker
              key={att.place_id}
              position={{ lat: att.latitude, lng: att.longitude }}
              onClick={() => {
                setSelectedAttraction(att)
                setActivePin(att)
              }}
              icon={{
                path: 'M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z',
                fillColor: selectedAttraction?.place_id === att.place_id ? '#10b981' : '#475569', // Emerald if active
                fillOpacity: 1,
                strokeColor: '#ffffff',
                strokeWeight: 1.5,
                scale: 1.2,
              }}
            />
          ))}

          {/* Active Info Window */}
          {activePin && (
            <InfoWindow
              position={{ lat: activePin.latitude, lng: activePin.longitude }}
              onCloseClick={() => setActivePin(null)}
            >
              <div className="p-2 text-slate-900 max-w-xs font-sans">
                <h5 className="font-bold text-sm mb-1">{activePin.name}</h5>
                <p className="text-xs text-slate-600 line-clamp-2">{activePin.description}</p>
              </div>
            </InfoWindow>
          )}

          {/* Polyline Route Overlay */}
          {selectedAttraction && polylinePath.length > 0 && (
            <Polyline
              path={polylinePath}
              options={{
                strokeColor: '#10b981', // Emerald
                strokeOpacity: 0.8,
                strokeWeight: 5,
              }}
            />
          )}
        </GoogleMap>
      </div>
    )
  }

  // ----------------------------------------------------
  // RENDER OPTION B: Visual Vector Mock Map Dashboard
  // ----------------------------------------------------
  // We calculate pixel offsets relative to searchCenter coordinates
  // to plot pins in a beautifully animated 2D SVG canvas dashboard.
  return <VectorMockMap
    center={mapCenter}
    attractions={attractions}
    selectedAttraction={selectedAttraction}
    setSelectedAttraction={setSelectedAttraction}
    polylinePath={polylinePath}
    locationName={searchCenter?.location_name || 'Paris'}
  />
}

// ----------------------------------------------------
// VectorMockMap Component for High-Fidelity API Fallbacks
// ----------------------------------------------------
interface VectorMapProps {
  center: { lat: number; lng: number }
  attractions: Attraction[]
  selectedAttraction: Attraction | null
  setSelectedAttraction: (att: Attraction | null) => void
  polylinePath: { lat: number; lng: number }[]
  locationName: string
}

const VectorMockMap: React.FC<VectorMapProps> = ({
  center,
  attractions,
  selectedAttraction,
  setSelectedAttraction,
  polylinePath,
  locationName,
}) => {
  const containerRef = useRef<HTMLDivElement>(null)

  // Map coordinates to pixel bounds (e.g. 500x500 box)
  // Compute max delta to auto-scale viewport dynamically
  let minLat = center.lat, maxLat = center.lat
  let minLng = center.lng, maxLng = center.lng

  attractions.forEach((att) => {
    if (att.latitude < minLat) minLat = att.latitude
    if (att.latitude > maxLat) maxLat = att.latitude
    if (att.longitude < minLng) minLng = att.longitude
    if (att.longitude > maxLng) maxLng = att.longitude
  })

  // Add margin delta padding
  const padding = 0.005
  minLat -= padding
  maxLat += padding
  minLng -= padding
  maxLng += padding

  const getCoordinates = (lat: number, lng: number) => {
    const latRange = maxLat - minLat || 1
    const lngRange = maxLng - minLng || 1
    // In SVG, Y coordinate grows downwards, so we invert Lat mapping
    const x = ((lng - minLng) / lngRange) * 100 // return percentage
    const y = (1 - (lat - minLat) / latRange) * 100
    return { x: `${x}%`, y: `${y}%` }
  }

  const centerCoords = getCoordinates(center.lat, center.lng)

  return (
    <div
      ref={containerRef}
      className="w-full h-full relative bg-slate-950 border border-slate-900 overflow-hidden flex flex-col justify-end select-none"
    >
      {/* City grid layout animation in background */}
      <div className="absolute inset-0 bg-[radial-gradient(#1e293b_1px,transparent_1px)] [background-size:24px_24px] opacity-35" />
      <div className="absolute top-1/2 left-0 right-0 h-[1px] bg-slate-900/50" />
      <div className="absolute left-1/2 top-0 bottom-0 w-[1px] bg-slate-900/50" />

      {/* Glow Rings at City Center */}
      <div
        className="absolute w-24 h-24 -ml-12 -mt-12 border border-brand-500/20 rounded-full animate-ping pointer-events-none"
        style={{ left: centerCoords.x, top: centerCoords.y, animationDuration: '3s' }}
      />

      {/* SVG Canvas overlaying route lines and nodes */}
      <svg className="absolute inset-0 w-full h-full pointer-events-none z-10">
        {/* Draw Neon glowing Route Path */}
        {selectedAttraction && polylinePath.length > 0 && (
          <>
            {/* Background Blur glow line */}
            <polyline
              points={polylinePath
                .map((pt) => {
                  const coords = getCoordinates(pt.lat, pt.lng)
                  if (!containerRef.current) return '0,0'
                  const w = containerRef.current.clientWidth
                  const h = containerRef.current.clientHeight
                  const px = (parseFloat(coords.x) / 100) * w
                  const py = (parseFloat(coords.y) / 100) * h
                  return `${px},${py}`
                })
                .join(' ')}
              fill="none"
              stroke="#10b981"
              strokeWidth="6"
              strokeOpacity="0.4"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="blur-sm"
            />
            {/* Solid line */}
            <polyline
              points={polylinePath
                .map((pt) => {
                  const coords = getCoordinates(pt.lat, pt.lng)
                  if (!containerRef.current) return '0,0'
                  const w = containerRef.current.clientWidth
                  const h = containerRef.current.clientHeight
                  const px = (parseFloat(coords.x) / 100) * w
                  const py = (parseFloat(coords.y) / 100) * h
                  return `${px},${py}`
                })
                .join(' ')}
              fill="none"
              stroke="#10b981"
              strokeWidth="3.5"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </>
        )}
      </svg>

      {/* 2. City Center Node */}
      <div
        className="absolute -translate-x-1/2 -translate-y-1/2 flex flex-col items-center z-20 group"
        style={{ left: centerCoords.x, top: centerCoords.y }}
      >
        <div className="w-5 h-5 rounded-full bg-brand-600 border-2 border-white flex items-center justify-center shadow-lg cursor-default">
          <Compass className="w-3.5 h-3.5 text-white" />
        </div>
        <div className="mt-1 px-2 py-0.5 rounded bg-slate-900/90 border border-slate-800 text-[9px] text-brand-300 font-semibold uppercase tracking-wider whitespace-nowrap">
          {locationName} Center
        </div>
      </div>

      {/* 3. Interactive Attraction Nodes */}
      {attractions.map((att) => {
        const coords = getCoordinates(att.latitude, att.longitude)
        const isSelected = selectedAttraction?.place_id === att.place_id
        
        return (
          <div
            key={att.place_id}
            className="absolute -translate-x-1/2 -translate-y-1/2 flex flex-col items-center z-30 cursor-pointer group"
            style={{ left: coords.x, top: coords.y }}
            onClick={() => setSelectedAttraction(att)}
          >
            {/* Animated Pin */}
            <motion.div
              animate={isSelected ? { scale: [1, 1.25, 1.15] } : { scale: 1 }}
              transition={{ duration: 0.3 }}
              className={`w-6 h-6 rounded-full flex items-center justify-center shadow-lg border transition-all duration-300 ${
                isSelected
                  ? 'bg-emerald-500 border-white text-white z-40 ring-4 ring-emerald-500/20'
                  : 'bg-slate-900 border-slate-700 text-slate-400 group-hover:border-slate-500 group-hover:text-slate-200'
              }`}
            >
              <MapPin className="w-3.5 h-3.5" />
            </motion.div>
            
            {/* Tooltip Overlay */}
            <div className={`mt-1.5 px-2.5 py-1 rounded-xl bg-slate-900/95 border shadow-xl text-xs font-semibold whitespace-nowrap pointer-events-none transition-all duration-300 ${
              isSelected 
                ? 'opacity-100 border-emerald-500 text-white scale-100 translate-y-0' 
                : 'opacity-0 scale-95 translate-y-1 group-hover:opacity-100 group-hover:scale-100 group-hover:translate-y-0 border-slate-800 text-slate-300'
            }`}>
              {att.name}
            </div>
          </div>
        )
      })}

      {/* Mock Map watermark footer */}
      <div className="absolute top-4 left-4 p-3 rounded-2xl glass border border-slate-850 flex items-center space-x-2 text-xs text-slate-400 z-10 pointer-events-none">
        <Navigation className="w-4 h-4 text-emerald-400 animate-pulse" />
        <span className="font-light">Virtual Vector Map Radar Active</span>
      </div>
    </div>
  )
}
export default MapContainer
