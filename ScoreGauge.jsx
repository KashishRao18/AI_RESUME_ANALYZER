import React, { useEffect, useState } from 'react'

export default function ScoreGauge({ score }) {
  const [display, setDisplay] = useState(0)
  const radius = 78
  const circumference = 2 * Math.PI * radius

  useEffect(() => {
    let frame
    let start
    const duration = 900
    const from = 0
    function tick(ts) {
      if (!start) start = ts
      const progress = Math.min((ts - start) / duration, 1)
      const eased = 1 - Math.pow(1 - progress, 3)
      setDisplay(Math.round(from + (score - from) * eased))
      if (progress < 1) frame = requestAnimationFrame(tick)
    }
    frame = requestAnimationFrame(tick)
    return () => cancelAnimationFrame(frame)
  }, [score])

  const offset = circumference - (display / 100) * circumference

  const tone =
    score >= 80 ? 'text-sage-400' : score >= 50 ? 'text-brass-400' : 'text-rust-400'
  const ring =
    score >= 80 ? '#5B9279' : score >= 50 ? '#C9A227' : '#B4553F'
  const label = score >= 80 ? 'Strong match' : score >= 50 ? 'Partial match' : 'Weak match'
  const rotation = score >= 80 ? '-rotate-6' : score >= 50 ? 'rotate-3' : '-rotate-3'

  return (
    <div className="flex flex-col items-center gap-4">
      <div className="relative w-[180px] h-[180px]">
        <svg width="180" height="180" viewBox="0 0 180 180" className="-rotate-90">
          <circle cx="90" cy="90" r={radius} stroke="#2A3B4C" strokeWidth="10" fill="none" />
          <circle
            cx="90"
            cy="90"
            r={radius}
            stroke={ring}
            strokeWidth="10"
            fill="none"
            strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            style={{ transition: 'stroke-dashoffset 0.1s linear' }}
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className={`font-display text-5xl ${tone}`}>{display}</span>
          <span className="text-parchment-300/50 text-xs font-mono tracking-wide">/ 100</span>
        </div>
      </div>
      <div
        className={`stamp-animate ${rotation} border-[3px] ${
          score >= 80 ? 'border-sage-500 text-sage-400' : score >= 50 ? 'border-brass-500 text-brass-400' : 'border-rust-500 text-rust-400'
        } rounded-sm px-4 py-1 font-display text-lg tracking-wide`}
      >
        {label.toUpperCase()}
      </div>
    </div>
  )
}
