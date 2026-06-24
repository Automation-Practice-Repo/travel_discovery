import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { Compass, SlidersHorizontal, ArrowLeft } from 'lucide-react'
import { SearchProvider, useSearch } from './context/SearchContext'
import Splash from './components/Splash'
import SearchForm from './components/SearchForm'
import AttractionCard from './components/AttractionCard'
import AttractionDetail from './components/AttractionDetail'
import MapContainer from './components/MapContainer'
import JourneyCelebration from './components/JourneyCelebration'

// Shimmer card placeholder for skeleton loading states
const SkeletonCard = () => (
  <div className="rounded-2xl border border-slate-900 bg-slate-900/40 p-4 space-y-4 animate-pulse">
    <div className="h-40 w-full bg-slate-800/60 rounded-xl"></div>
    <div className="space-y-3">
      <div className="h-5 bg-slate-800/60 rounded w-2/3"></div>
      <div className="h-3.5 bg-slate-800/60 rounded w-full"></div>
      <div className="h-3.5 bg-slate-800/60 rounded w-4/5"></div>
    </div>
    <div className="h-3 bg-slate-800/40 rounded w-1/2 pt-2"></div>
  </div>
)

const MainAppContent: React.FC = () => {
  const [showSplash, setShowSplash] = useState(true)
  const [isSearching, setIsSearching] = useState(false)
  const {
    activeView,
    setActiveView,
    searchTerm,
    radius,
    attractions,
    journeyDestination,
    selectedAttraction
  } = useSearch()

  // Handler to clear search loading skeleton
  const handleSearchStarted = () => {
    setIsSearching(true)
  }

  const handleSearchCompleted = () => {
    setIsSearching(false)
  }

  if (showSplash) {
    return <Splash show={showSplash} onComplete={() => setShowSplash(false)} />
  }

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col relative text-slate-100 font-sans">
      {/* 1. Global Navigation Header */}
      <header className="w-full py-4 px-6 md:px-8 border-b border-slate-900 bg-slate-950/80 backdrop-blur-md sticky top-0 z-40 flex items-center justify-between">
        <div 
          onClick={() => setActiveView('search')}
          className="flex items-center space-x-2.5 cursor-pointer select-none group"
        >
          <Compass className="w-6 h-6 text-brand-500 group-hover:rotate-45 transition-transform duration-300" />
          <span className="font-extrabold text-lg tracking-wider bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400">
            VAGABOND
          </span>
        </div>
        
        {activeView !== 'search' && (
          <button
            onClick={() => setActiveView('search')}
            className="flex items-center space-x-1.5 px-4 py-2 rounded-full border border-slate-800 hover:border-slate-700 bg-slate-900/40 text-xs text-slate-300 hover:text-white transition-all transform active:scale-95"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            <span>New Search</span>
          </button>
        )}
      </header>

      {/* 2. Main Page Layouts */}
      <main className="flex-grow flex flex-col">
        {/* VIEW A: Search Landing Portal */}
        {activeView === 'search' && (
          <div className="flex-grow flex flex-col justify-center items-center px-4 py-12 md:py-24 relative overflow-hidden">
            {/* Soft ambient background radial glows */}
            <div className="absolute w-[500px] h-[500px] rounded-full bg-brand-500/5 blur-[120px] -translate-y-20 pointer-events-none" />
            <div className="absolute w-[400px] h-[400px] rounded-full bg-indigo-500/5 blur-[100px] translate-y-20 pointer-events-none" />

            <div className="w-full max-w-4xl text-center space-y-8 z-10">
              <div className="space-y-4 max-w-2xl mx-auto">
                <motion.h1 
                  initial={{ opacity: 0, y: 15 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6 }}
                  className="text-4xl sm:text-5xl md:text-6xl font-extrabold tracking-tight text-white leading-tight font-sans"
                >
                  DISCOVER THE <span className="bg-clip-text text-transparent bg-gradient-to-r from-brand-500 to-indigo-400">UNSEEN</span>
                </motion.h1>
                <motion.p
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: 0.2 }}
                  className="text-sm sm:text-base text-slate-400 font-light max-w-lg mx-auto leading-relaxed"
                >
                  Enter a destination and radius to explore local attractions, maps, driving directions, and curated travel reviews instantly.
                </motion.p>
              </div>

              <SearchForm 
                onSearchStarted={handleSearchStarted} 
                onSearchCompleted={handleSearchCompleted} 
              />
            </div>
          </div>
        )}

        {/* VIEW B: Interactive Results Dashboard */}
        {activeView === 'results' && (
          <div className="flex-grow flex flex-col lg:flex-row h-[calc(100vh-68px)] overflow-hidden">
            
            {/* Left Column: Attractions Grid List */}
            <div className="w-full lg:w-[480px] xl:w-[540px] h-1/2 lg:h-full flex flex-col border-r border-slate-900 bg-slate-950/60 overflow-hidden">
              
              {/* Search details header */}
              <div className="p-5 border-b border-slate-900 bg-slate-950/40 flex-shrink-0 flex items-center justify-between text-xs">
                <div className="space-y-1">
                  <span className="text-[10px] font-bold text-slate-500 uppercase tracking-wider block">Results near</span>
                  <h3 className="font-bold text-sm text-white flex items-center gap-1.5">
                    {searchTerm} 
                    <span className="text-[11px] px-2 py-0.5 rounded-full bg-brand-500/10 text-brand-300 font-medium">
                      within {radius}km
                    </span>
                  </h3>
                </div>
                {!isSearching && (
                  <span className="text-slate-400 font-medium">
                    {attractions.length} spots found
                  </span>
                )}
              </div>

              {/* Scrollable grid items */}
              <div className="flex-grow overflow-y-auto p-5">
                {isSearching ? (
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-1 xl:grid-cols-2 gap-4">
                    <SkeletonCard />
                    <SkeletonCard />
                    <SkeletonCard />
                    <SkeletonCard />
                  </div>
                ) : attractions.length > 0 ? (
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-1 xl:grid-cols-2 gap-4 pb-6">
                    {attractions.map((att) => (
                      <AttractionCard key={att.place_id} attraction={att} />
                    ))}
                  </div>
                ) : (
                  <div className="h-full flex flex-col justify-center items-center text-center px-4 space-y-4 py-12">
                    <SlidersHorizontal className="w-12 h-12 text-slate-700 animate-float" />
                    <div className="space-y-1 max-w-xs">
                      <h4 className="font-bold text-sm text-white">No spots discovered</h4>
                      <p className="text-xs text-slate-550 font-light leading-relaxed">
                        We couldn't find attractions in "{searchTerm}" within {radius}km. Try increasing your radius or check another city.
                      </p>
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Right Column: Dynamic Map Radar Panel */}
            <div className="flex-grow h-1/2 lg:h-full relative">
              <MapContainer />
              
              {/* Slide-out detail drawer */}
              <div className="absolute top-0 bottom-0 right-0 z-20 pointer-events-none">
                <div className="h-full pointer-events-auto flex justify-end">
                  {selectedAttraction && <AttractionDetail />}
                </div>
              </div>
            </div>

          </div>
        )}
      </main>

      {/* 3. Global Journey Success Page overlay */}
      {journeyDestination && <JourneyCelebration />}
    </div>
  )
}

function App() {
  return (
    <SearchProvider>
      <MainAppContent />
    </SearchProvider>
  )
}

export default App
