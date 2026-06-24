import React, { useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Compass } from 'lucide-react'

interface SplashProps {
  onComplete: () => void
  show: boolean
}

export const Splash: React.FC<SplashProps> = ({ onComplete, show }) => {
  useEffect(() => {
    if (show) {
      const timer = setTimeout(() => {
        onComplete()
      }, 3000) // 3 seconds total splash time
      return () => clearTimeout(timer)
    }
  }, [show, onComplete])

  return (
    <AnimatePresence>
      {show && (
        <motion.div
          className="fixed inset-0 z-50 flex flex-col items-center justify-center bg-slate-950"
          initial={{ opacity: 1 }}
          exit={{ opacity: 0, transition: { duration: 0.8, ease: 'easeInOut' } }}
        >
          {/* Pulsing deep purple/indigo background glow */}
          <div className="absolute w-[300px] h-[300px] rounded-full bg-brand-500/10 blur-[80px]" />
          <div className="absolute w-[200px] h-[200px] rounded-full bg-brand-700/5 blur-[50px] translate-y-10" />

          <div className="relative flex flex-col items-center text-center px-4">
            {/* Spinning/pulsing compass logo */}
            <motion.div
              initial={{ scale: 0.3, rotate: -180, opacity: 0 }}
              animate={{ 
                scale: 1, 
                rotate: 0, 
                opacity: 1,
                transition: { type: 'spring', stiffness: 80, damping: 15, delay: 0.2 } 
              }}
              className="relative p-5 rounded-3xl bg-slate-900 border border-slate-800 shadow-2xl mb-6"
            >
              <Compass className="w-16 h-16 text-brand-500" strokeWidth={1.5} />
              <motion.div
                className="absolute inset-0 rounded-3xl border border-brand-500/30"
                animate={{ scale: [1, 1.15, 1], opacity: [0.5, 0, 0.5] }}
                transition={{ repeat: Infinity, duration: 2.5, ease: 'easeInOut' }}
              />
            </motion.div>

            {/* Application Title */}
            <motion.h1
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1, transition: { delay: 0.6, duration: 0.5 } }}
              className="text-4xl sm:text-5xl font-extrabold tracking-wider text-white font-sans bg-clip-text text-transparent bg-gradient-to-r from-white via-slate-200 to-slate-400"
            >
              VAGABOND
            </motion.h1>

            {/* Subtitle */}
            <motion.p
              initial={{ y: 15, opacity: 0 }}
              animate={{ y: 0, opacity: 1, transition: { delay: 0.9, duration: 0.5 } }}
              className="mt-3 text-sm sm:text-base text-slate-400 tracking-[0.2em] font-light uppercase"
            >
              Luxury Travel Discovery
            </motion.p>

            {/* Miniature Loading bar indicator */}
            <div className="mt-12 w-40 h-[2px] bg-slate-850 rounded-full overflow-hidden">
              <motion.div
                className="h-full bg-gradient-to-r from-brand-500 to-brand-700"
                initial={{ width: '0%' }}
                animate={{ width: '100%' }}
                transition={{ duration: 2.4, ease: 'easeInOut', delay: 0.3 }}
              />
            </div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}
export default Splash
