import React, { createContext, useContext, useState } from 'react'
import type { ReactNode } from 'react'
import type { Attraction, SearchCenter, DirectionsResponse } from '../services/api'

export type ActiveView = 'search' | 'results' | 'journey'

interface SearchContextType {
  searchTerm: string
  setSearchTerm: (term: string) => void
  radius: number
  setRadius: (r: number) => void
  searchCenter: SearchCenter | null
  setSearchCenter: (center: SearchCenter | null) => void
  attractions: Attraction[]
  setAttractions: (list: Attraction[]) => void
  selectedAttraction: Attraction | null
  setSelectedAttraction: (attraction: Attraction | null) => void
  directions: DirectionsResponse | null
  setDirections: (dirs: DirectionsResponse | null) => void
  activeView: ActiveView
  setActiveView: (view: ActiveView) => void
  journeyDestination: Attraction | null
  setJourneyDestination: (attraction: Attraction | null) => void
}

const SearchContext = createContext<SearchContextType | undefined>(undefined)

export const SearchProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [searchTerm, setSearchTerm] = useState('')
  const [radius, setRadius] = useState(15)
  const [searchCenter, setSearchCenter] = useState<SearchCenter | null>(null)
  const [attractions, setAttractions] = useState<Attraction[]>([])
  const [selectedAttraction, setSelectedAttraction] = useState<Attraction | null>(null)
  const [directions, setDirections] = useState<DirectionsResponse | null>(null)
  const [activeView, setActiveView] = useState<ActiveView>('search')
  const [journeyDestination, setJourneyDestination] = useState<Attraction | null>(null)

  return (
    <SearchContext.Provider
      value={{
        searchTerm,
        setSearchTerm,
        radius,
        setRadius,
        searchCenter,
        setSearchCenter,
        attractions,
        setAttractions,
        selectedAttraction,
        setSelectedAttraction,
        directions,
        setDirections,
        activeView,
        setActiveView,
        journeyDestination,
        setJourneyDestination,
      }}
    >
      {children}
    </SearchContext.Provider>
  )
}

export const useSearch = () => {
  const context = useContext(SearchContext)
  if (!context) {
    throw new Error('useSearch must be used within a SearchProvider')
  }
  return context
}
