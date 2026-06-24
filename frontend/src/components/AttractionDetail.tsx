import React, { useEffect, useState } from 'react'
import { X, Clock, Star, MapPin, Navigation, Compass } from 'lucide-react'
import { useSearch } from '../context/SearchContext'
import { getDirections } from '../services/api'

export const AttractionDetail: React.FC = () => {
  const {
    selectedAttraction,
    setSelectedAttraction,
    searchCenter,
    directions,
    setDirections,
    setJourneyDestination
  } = useSearch()

  const [loadingRoute, setLoadingRoute] = useState(false)

  // Fetch directions route when attraction is selected
  useEffect(() => {
    if (!selectedAttraction || !searchCenter) return

    const fetchRoute = async () => {
      setLoadingRoute(true)
      try {
        const response = await getDirections({
          origin_lat: searchCenter.latitude,
          origin_lng: searchCenter.longitude,
          destination_lat: selectedAttraction.latitude,
          destination_lng: selectedAttraction.longitude,
          destination_place_id: selectedAttraction.place_id
        })
        setDirections(response)
      } catch (err) {
        console.error("Failed to load directions:", err)
      } finally {
        setLoadingRoute(false)
      }
    }

    fetchRoute()
  }, [selectedAttraction, searchCenter, setDirections])

  if (!selectedAttraction) return null

  // Determine open/closed status badge
  const isOpen = selectedAttraction.opening_hours?.open_now

  return (
    <div className="w-full lg:w-[420px] h-full flex flex-col bg-slate-900 border-l border-slate-800 shadow-2xl overflow-hidden relative">
      {/* Header Close button */}
      <div className="absolute top-4 right-4 z-10">
        <button
          onClick={() => setSelectedAttraction(null)}
          className="p-2 rounded-full bg-slate-950/60 backdrop-blur-md border border-white/10 text-slate-400 hover:text-white transition-colors"
        >
          <X className="w-4 h-4" />
        </button>
      </div>

      {/* Main Image Banner */}
      <div className="relative h-64 w-full bg-slate-950 flex-shrink-0">
        <img
          src={selectedAttraction.image_url || 'https://images.unsplash.com/photo-1488646953014-85cb44e25828?auto=format&fit=crop&w=800&q=80'}
          alt={selectedAttraction.name}
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-slate-900 via-slate-900/20 to-transparent" />
        
        {/* Name and Status */}
        <div className="absolute bottom-4 left-5 right-5">
          <div className="flex items-center space-x-2 mb-1.5">
            <span className={`px-2 py-0.5 rounded-full text-[10px] font-semibold tracking-wider uppercase border ${
              isOpen 
                ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400' 
                : 'bg-rose-500/10 border-rose-500/30 text-rose-400'
            }`}>
              {isOpen ? 'Open Now' : 'Closed'}
            </span>
          </div>
          <h2 className="text-xl md:text-2xl font-extrabold text-white tracking-wide leading-tight font-sans">
            {selectedAttraction.name}
          </h2>
        </div>
      </div>

      {/* Details Scroll Area */}
      <div className="flex-grow overflow-y-auto px-5 py-4 space-y-6">
        
        {/* Rating and Distance Summary */}
        <div className="grid grid-cols-2 gap-4 pb-4 border-b border-slate-800">
          <div className="flex flex-col space-y-1">
            <span className="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Rating</span>
            <div className="flex items-center space-x-1.5">
              <Star className="w-4 h-4 text-amber-400 fill-amber-400" />
              <span className="text-sm font-semibold text-white">
                {selectedAttraction.rating ? selectedAttraction.rating.toFixed(1) : 'N/A'}
              </span>
              {selectedAttraction.user_ratings_total !== null && selectedAttraction.user_ratings_total > 0 && (
                <span className="text-xs text-slate-400">
                  ({selectedAttraction.user_ratings_total.toLocaleString()})
                </span>
              )}
            </div>
          </div>
          <div className="flex flex-col space-y-1">
            <span className="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Distance</span>
            <span className="text-sm font-semibold text-white flex items-center gap-1.5">
              <MapPin className="w-4 h-4 text-brand-500" />
              {directions ? directions.distance : 'Calculating...'}
            </span>
          </div>
        </div>

        {/* Place Description */}
        <div className="space-y-2">
          <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider">Overview</h4>
          <p className="text-sm text-slate-300 font-light leading-relaxed">
            {selectedAttraction.description || 'Discover this magnificent spot. No description details provided.'}
          </p>
        </div>

        {/* Opening Hours */}
        {selectedAttraction.opening_hours?.weekday_text && (
          <div className="space-y-2">
            <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
              <Clock className="w-3.5 h-3.5 text-slate-400" />
              Opening Hours
            </h4>
            <div className="p-3.5 rounded-xl bg-slate-950/40 border border-slate-850 space-y-1.5 text-xs text-slate-400 font-light">
              {selectedAttraction.opening_hours.weekday_text.map((day, idx) => (
                <div key={idx} className="flex justify-between">
                  <span>{day.split(': ')[0]}</span>
                  <span className="text-slate-300 font-medium">{day.split(': ')[1]}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Travel Information & Step-by-Step Directions */}
        <div className="space-y-3">
          <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
            <Navigation className="w-3.5 h-3.5 text-slate-400" />
            Directions & Route
          </h4>
          
          {loadingRoute ? (
            <div className="space-y-2 py-4">
              <div className="h-4 bg-slate-800 rounded animate-pulse w-3/4"></div>
              <div className="h-4 bg-slate-800 rounded animate-pulse w-5/6"></div>
              <div className="h-4 bg-slate-800 rounded animate-pulse w-2/3"></div>
            </div>
          ) : directions ? (
            <div className="space-y-3">
              {/* Est Travel Time banner */}
              <div className="flex items-center justify-between p-3 rounded-xl bg-brand-500/10 border border-brand-500/20 text-xs text-brand-200">
                <span className="font-medium">Estimated Drive Time:</span>
                <span className="font-bold text-white text-sm">{directions.duration}</span>
              </div>
              
              {/* Steps list */}
              <div className="p-3.5 rounded-xl bg-slate-950/40 border border-slate-850 space-y-2 text-xs">
                {directions.steps && directions.steps.map((step, idx) => (
                  <div key={idx} className="flex space-x-2 text-slate-400 leading-normal">
                    <span className="text-brand-400 font-bold">{idx + 1}.</span>
                    <span className="font-light">{step}</span>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <p className="text-xs text-slate-500 italic">No route details available.</p>
          )}
        </div>
      </div>

      {/* Start Journey sticky panel */}
      <div className="p-5 bg-slate-950/80 border-t border-slate-850 flex-shrink-0">
        <button
          onClick={() => setJourneyDestination(selectedAttraction)}
          className="w-full flex items-center justify-center space-x-2 py-4 rounded-xl bg-gradient-to-r from-emerald-600 to-emerald-700 hover:from-emerald-500 hover:to-emerald-600 text-white font-semibold text-base shadow-lg shadow-emerald-500/10 hover:shadow-emerald-500/25 transition-all duration-300 transform active:scale-[0.98]"
        >
          <Compass className="w-5 h-5 animate-pulse-slow" />
          <span>Start Happy Journey</span>
        </button>
      </div>
    </div>
  )
}
export default AttractionDetail
