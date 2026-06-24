import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Search, MapPin, Compass } from 'lucide-react'
import { useSearch } from '../context/SearchContext'
import { searchAttractions, getAutocompleteSuggestions } from '../services/api'

interface SearchFormProps {
  onSearchStarted: () => void
  onSearchCompleted: () => void
}

export const SearchForm: React.FC<SearchFormProps> = ({ onSearchStarted, onSearchCompleted }) => {
  const {
    searchTerm,
    setSearchTerm,
    radius,
    setRadius,
    setSearchCenter,
    setAttractions,
    setActiveView,
    setSelectedAttraction,
    setDirections
  } = useSearch()

  const [inputVal, setInputVal] = useState(searchTerm)
  const [error, setError] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [suggestions, setSuggestions] = useState<string[]>([])
  const [showSuggestions, setShowSuggestions] = useState(false)
  const [highlightedIndex, setHighlightedIndex] = useState(-1)

  // Debounced autocomplete suggestions fetch
  useEffect(() => {
    const trimmed = inputVal.trim()
    if (!trimmed || trimmed.length < 1) {
      setSuggestions([])
      setShowSuggestions(false)
      return
    }

    const delayDebounce = setTimeout(async () => {
      try {
        const list = await getAutocompleteSuggestions(trimmed)
        setSuggestions(list)
        setShowSuggestions(list.length > 0)
        setHighlightedIndex(-1)
      } catch (err) {
        console.error("Autocomplete error:", err)
      }
    }, 200) // 200ms debounce

    return () => clearTimeout(delayDebounce)
  }, [inputVal])

  // Hide suggestions when clicking outside
  useEffect(() => {
    const handleOutsideClick = () => {
      setShowSuggestions(false)
    }
    document.addEventListener('click', handleOutsideClick)
    return () => document.removeEventListener('click', handleOutsideClick)
  }, [])

  // Keyboard navigation inside dropdown
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (!showSuggestions || suggestions.length === 0) return

    if (e.key === 'ArrowDown') {
      e.preventDefault()
      setHighlightedIndex((prev) => (prev + 1) % suggestions.length)
    } else if (e.key === 'ArrowUp') {
      e.preventDefault()
      setHighlightedIndex((prev) => (prev - 1 + suggestions.length) % suggestions.length)
    } else if (e.key === 'Enter') {
      if (highlightedIndex >= 0 && highlightedIndex < suggestions.length) {
        e.preventDefault()
        setInputVal(suggestions[highlightedIndex])
        setShowSuggestions(false)
      }
    } else if (e.key === 'Escape') {
      setShowSuggestions(false)
    }
  }

  const quickCities = ['Paris', 'Rome', 'Tokyo']

  const handleCityBadgeClick = (city: string) => {
    setInputVal(city)
    setError('')
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    const trimmed = inputVal.trim()
    if (!trimmed) {
      setError('Please enter a city or location name.')
      return
    }
    if (trimmed.length < 2) {
      setError('Location name must be at least 2 characters.')
      return
    }

    setError('')
    setIsSubmitting(true)
    onSearchStarted()

    try {
      setSearchTerm(trimmed)
      setSelectedAttraction(null)
      setDirections(null)
      
      const response = await searchAttractions(trimmed, radius)
      
      setSearchCenter(response.center)
      setAttractions(response.results)
      setActiveView('results')
      onSearchCompleted()
    } catch (err: any) {
      console.error(err)
      const errorMsg = err.response?.data?.detail || 'Could not find tourist attractions for this location. Please try another city.'
      setError(errorMsg)
      onSearchCompleted()
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="w-full max-w-2xl mx-auto p-6 md:p-8 rounded-3xl glass-panel shadow-2xl relative overflow-hidden"
    >
      {/* Background decorations */}
      <div className="absolute top-0 right-0 w-32 h-32 bg-brand-500/5 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-0 left-0 w-40 h-40 bg-brand-650/5 rounded-full blur-3xl pointer-events-none" />

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Destination Location Input */}
        <div className="space-y-2">
          <label className="block text-xs font-semibold text-slate-400 tracking-wider uppercase">
            Where to?
          </label>
          <div className="relative">
            <MapPin className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-brand-500" />
            <input
              type="text"
              value={inputVal}
              onChange={(e) => {
                setInputVal(e.target.value)
                if (error) setError('')
              }}
              onKeyDown={handleKeyDown}
              onFocus={() => {
                if (suggestions.length > 0) setShowSuggestions(true)
              }}
              placeholder="e.g. Paris, Rome, Tokyo..."
              className="w-full pl-12 pr-4 py-4 rounded-2xl glass-input text-base text-white placeholder-slate-500 font-sans"
              disabled={isSubmitting}
            />
            {showSuggestions && suggestions.length > 0 && (
              <ul className="absolute z-50 left-0 right-0 mt-2 p-1.5 rounded-2xl bg-slate-900/95 border border-slate-800 shadow-2xl overflow-hidden divide-y divide-slate-850/60 max-h-60 overflow-y-auto">
                {suggestions.map((suggestion, idx) => (
                  <li
                    key={idx}
                    onMouseDown={(e) => {
                      e.preventDefault() // Prevents input blur
                      setInputVal(suggestion)
                      setShowSuggestions(false)
                    }}
                    className={`px-4 py-3 text-sm text-slate-300 cursor-pointer transition-colors duration-150 flex items-center gap-2.5 hover:bg-brand-500/10 hover:text-white rounded-xl ${
                      idx === highlightedIndex ? 'bg-brand-500/15 text-white' : ''
                    }`}
                  >
                    <MapPin className="w-3.5 h-3.5 text-brand-400 flex-shrink-0" />
                    <span className="truncate">{suggestion}</span>
                  </li>
                ))}
              </ul>
            )}
          </div>
          {error && (
            <motion.p
              initial={{ opacity: 0, y: -5 }}
              animate={{ opacity: 1, y: 0 }}
              className="text-xs font-medium text-rose-500 pl-1"
            >
              {error}
            </motion.p>
          )}
        </div>

        {/* Quick select buttons */}
        <div className="flex items-center space-x-2 pt-1">
          <span className="text-xs text-slate-500">Popular:</span>
          <div className="flex gap-2 flex-wrap">
            {quickCities.map((city) => (
              <button
                key={city}
                type="button"
                onClick={() => handleCityBadgeClick(city)}
                className={`text-xs px-3 py-1.5 rounded-full border transition-all duration-300 ${
                  inputVal.toLowerCase() === city.toLowerCase()
                    ? 'bg-brand-500/15 border-brand-500 text-brand-200'
                    : 'border-slate-800 bg-slate-900/40 text-slate-400 hover:border-slate-700 hover:text-slate-300'
                }`}
                disabled={isSubmitting}
              >
                {city}
              </button>
            ))}
          </div>
        </div>

        {/* Radius Range Slider */}
        <div className="space-y-3 pt-2">
          <div className="flex justify-between items-center text-xs font-semibold text-slate-400 tracking-wider uppercase">
            <span>Search Radius</span>
            <span className="text-brand-500 font-bold normal-case tracking-normal">
              {radius} km
            </span>
          </div>
          <div className="relative pt-1 flex items-center">
            <input
              type="range"
              min="1"
              max="50"
              value={radius}
              onChange={(e) => setRadius(parseInt(e.target.value))}
              className="w-full h-1.5 bg-slate-900 rounded-lg appearance-none cursor-pointer accent-brand-500 transition-all duration-200"
              disabled={isSubmitting}
            />
          </div>
          <div className="flex justify-between text-[10px] text-slate-500 font-medium">
            <span>1 km</span>
            <span>25 km</span>
            <span>50 km</span>
          </div>
        </div>

        {/* Search Submit Button */}
        <button
          type="submit"
          disabled={isSubmitting}
          className="w-full flex items-center justify-center space-x-2 py-4 px-6 rounded-2xl bg-gradient-to-r from-brand-600 to-brand-700 hover:from-brand-500 hover:to-brand-600 text-white font-semibold text-base shadow-lg shadow-brand-500/20 hover:shadow-brand-500/35 transition-all duration-300 transform active:scale-[0.98] disabled:opacity-75 disabled:cursor-not-allowed"
        >
          {isSubmitting ? (
            <>
              <Compass className="w-5 h-5 animate-spin" />
              <span>Plotting route...</span>
            </>
          ) : (
            <>
              <Search className="w-5 h-5" />
              <span>Explore Attractions</span>
            </>
          )}
        </button>
      </form>
    </motion.div>
  )
}
export default SearchForm
