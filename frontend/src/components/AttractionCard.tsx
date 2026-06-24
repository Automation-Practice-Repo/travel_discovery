import React from 'react'
import { Star, MapPin } from 'lucide-react'
import type { Attraction } from '../services/api'
import { useSearch } from '../context/SearchContext'

interface AttractionCardProps {
  attraction: Attraction
}

export const AttractionCard: React.FC<AttractionCardProps> = ({ attraction }) => {
  const { selectedAttraction, setSelectedAttraction } = useSearch()

  const isSelected = selectedAttraction?.place_id === attraction.place_id
  const hasRating = attraction.rating !== null && attraction.rating !== undefined

  // Shorten reviews count to look clean (e.g., 32.8k reviews)
  const formatReviews = (count: number | null): string => {
    if (!count) return '0'
    if (count >= 1000) {
      return (count / 1000).toFixed(1) + 'k'
    }
    return count.toString()
  }

  // Format description snippet
  const getExcerpt = (text: string | null): string => {
    if (!text) return 'No description available.'
    if (text.length > 85) {
      return text.substring(0, 82) + '...'
    }
    return text
  }

  return (
    <div
      onClick={() => setSelectedAttraction(attraction)}
      className={`relative flex flex-col h-full rounded-2xl glass-card cursor-pointer overflow-hidden group select-none transition-all duration-300 ${
        isSelected ? 'border-brand-500 ring-2 ring-brand-500/20 bg-slate-900/60' : ''
      }`}
    >
      {/* Attraction Image Section */}
      <div className="relative h-48 w-full overflow-hidden bg-slate-900">
        <img
          src={attraction.image_url || 'https://images.unsplash.com/photo-1488646953014-85cb44e25828?auto=format&fit=crop&w=600&q=80'}
          alt={attraction.name}
          className="w-full h-full object-cover transform group-hover:scale-105 transition-transform duration-500 ease-out"
          loading="lazy"
        />
        {/* Shadow Overlay */}
        <div className="absolute inset-0 bg-gradient-to-t from-slate-950/80 via-transparent to-transparent opacity-60" />

        {/* Rating overlay badge */}
        {hasRating && (
          <div className="absolute top-3 right-3 flex items-center space-x-1 px-2.5 py-1 rounded-full bg-slate-950/70 backdrop-blur-md border border-white/10 text-xs font-semibold text-white">
            <Star className="w-3.5 h-3.5 text-amber-400 fill-amber-400" />
            <span>{attraction.rating?.toFixed(1)}</span>
          </div>
        )}
      </div>

      {/* Content Section */}
      <div className="flex flex-col flex-grow p-4 justify-between space-y-3">
        <div className="space-y-1">
          <h3 className="font-bold text-base text-white tracking-wide leading-tight group-hover:text-brand-200 transition-colors">
            {attraction.name}
          </h3>
          <p className="text-xs text-slate-400 font-light leading-relaxed">
            {getExcerpt(attraction.description)}
          </p>
        </div>

        {/* Footnotes: Address & Details */}
        <div className="flex items-center justify-between pt-2 border-t border-slate-900 text-xs">
          <div className="flex items-center text-slate-400 space-x-1 max-w-[65%]">
            <MapPin className="w-3.5 h-3.5 text-brand-500 flex-shrink-0" />
            <span className="truncate">{attraction.address || 'Address N/A'}</span>
          </div>
          
          {attraction.user_ratings_total !== null && attraction.user_ratings_total > 0 && (
            <span className="text-slate-500 font-medium">
              ({formatReviews(attraction.user_ratings_total)} reviews)
            </span>
          )}
        </div>
      </div>
    </div>
  )
}
export default AttractionCard
