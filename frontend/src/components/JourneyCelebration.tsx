import React, { useEffect } from 'react'
import { motion } from 'framer-motion'
import confetti from 'canvas-confetti'
import { Compass, Sparkles, Navigation, RotateCcw } from 'lucide-react'
import { useSearch } from '../context/SearchContext'

export const JourneyCelebration: React.FC = () => {
  const { journeyDestination, directions, setJourneyDestination, setActiveView } = useSearch()

  useEffect(() => {
    if (!journeyDestination) return

    // Launch beautiful confetti cascade
    const duration = 4 * 1000
    const end = Date.now() + duration

    const frame = () => {
      confetti({
        particleCount: 4,
        angle: 60,
        spread: 55,
        origin: { x: 0 },
        colors: ['#8b5cf6', '#10b981', '#fbbf24']
      })
      confetti({
        particleCount: 4,
        angle: 120,
        spread: 55,
        origin: { x: 1 },
        colors: ['#8b5cf6', '#10b981', '#fbbf24']
      })

      if (Date.now() < end) {
        requestAnimationFrame(frame)
      }
    }

    frame()
  }, [journeyDestination])

  if (!journeyDestination) return null

  const handleReturn = () => {
    setJourneyDestination(null)
    setActiveView('results')
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950 px-4 overflow-hidden select-none">
      {/* Background neon glows */}
      <div className="absolute w-[400px] h-[400px] rounded-full bg-emerald-500/10 blur-[100px] -translate-x-32 -translate-y-20 pointer-events-none" />
      <div className="absolute w-[300px] h-[300px] rounded-full bg-brand-500/10 blur-[80px] translate-x-32 translate-y-20 pointer-events-none" />
      
      {/* Floating stars/particles in background */}
      <div className="absolute inset-0 bg-[radial-gradient(#ffffff_0.5px,transparent_0.5px)] [background-size:32px_32px] opacity-10 pointer-events-none" />

      {/* Main card */}
      <motion.div
        initial={{ opacity: 0, scale: 0.9, y: 30 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        transition={{ type: 'spring', damping: 20, stiffness: 100 }}
        className="w-full max-w-xl p-8 md:p-12 rounded-3xl glass-panel shadow-2xl relative text-center border border-slate-800"
      >
        {/* Glowing border ring decoration */}
        <div className="absolute inset-0 rounded-3xl border border-emerald-500/20 pointer-events-none" />

        {/* Success Icon */}
        <motion.div
          initial={{ rotate: -180, scale: 0.2 }}
          animate={{ rotate: 0, scale: 1 }}
          transition={{ type: 'spring', delay: 0.2, damping: 12 }}
          className="relative inline-flex p-5 rounded-3xl bg-slate-900 border border-slate-800 mb-8"
        >
          <Compass className="w-14 h-14 text-emerald-400 animate-float" strokeWidth={1.5} />
          <motion.div
            className="absolute -top-1 -right-1"
            animate={{ scale: [1, 1.2, 1], rotate: [0, 15, 0] }}
            transition={{ repeat: Infinity, duration: 2 }}
          >
            <Sparkles className="w-6 h-6 text-amber-400 fill-amber-400" />
          </motion.div>
        </motion.div>

        {/* Title */}
        <motion.h1
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="text-3xl md:text-4xl font-extrabold text-white tracking-wide font-sans mb-3"
        >
          Happy Journey!
        </motion.h1>

        {/* Subtitle */}
        <motion.p
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="text-xs text-emerald-400 font-bold uppercase tracking-widest mb-6"
        >
          Adventure Activated
        </motion.p>

        {/* Detail message card */}
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7 }}
          className="p-5 md:p-6 rounded-2xl bg-slate-950/50 border border-slate-850 text-slate-300 font-light mb-8 max-w-md mx-auto"
        >
          <p className="text-sm md:text-base leading-relaxed">
            Your destination to <span className="font-bold text-white text-emerald-200">{journeyDestination.name}</span> is ready! 
            Safe travels on your explore itinerary.
          </p>
          {directions && (
            <div className="flex justify-center items-center space-x-4 mt-4 pt-4 border-t border-slate-900 text-xs font-semibold text-slate-400">
              <span>Distance: <strong className="text-white">{directions.distance}</strong></span>
              <span className="w-1.5 h-1.5 rounded-full bg-slate-800" />
              <span>Drive Time: <strong className="text-white">{directions.duration}</strong></span>
            </div>
          )}
        </motion.div>

        {/* Launch actions */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.9 }}
          className="flex flex-col sm:flex-row gap-4 justify-center items-center"
        >
          {/* Back button */}
          <button
            onClick={handleReturn}
            className="w-full sm:w-auto flex items-center justify-center space-x-2 px-6 py-3.5 rounded-xl border border-slate-800 hover:border-slate-700 bg-slate-900/40 text-slate-400 hover:text-white text-sm font-semibold transition-all duration-300 transform active:scale-95"
          >
            <RotateCcw className="w-4 h-4" />
            <span>Modify Selection</span>
          </button>

          {/* Open Google Maps Directions button */}
          {directions?.navigation_url && (
            <a
              href={directions.navigation_url}
              target="_blank"
              rel="noopener noreferrer"
              className="w-full sm:w-auto flex items-center justify-center space-x-2 px-6 py-3.5 rounded-xl bg-gradient-to-r from-brand-600 to-brand-700 hover:from-brand-500 hover:to-brand-600 text-white text-sm font-semibold shadow-lg shadow-brand-500/10 hover:shadow-brand-500/25 transition-all duration-300 transform active:scale-95"
            >
              <Navigation className="w-4 h-4 fill-white" />
              <span>Open in Google Maps</span>
            </a>
          )}
        </motion.div>
      </motion.div>
    </div>
  )
}
export default JourneyCelebration
