import React from 'react'

const TONE_STYLES = {
  matched: 'bg-sage-500/10 text-sage-400 border-sage-500/40',
  missing: 'bg-rust-500/10 text-rust-400 border-rust-500/40',
  bonus: 'bg-brass-500/10 text-brass-400 border-brass-500/40',
}

export default function SkillGroup({ title, grouped, tone, emptyText }) {
  const categories = Object.keys(grouped || {})
  const hasAny = categories.length > 0

  return (
    <div className="rise-in">
      <h4 className="font-display text-lg text-parchment-100 mb-3">{title}</h4>
      {!hasAny && (
        <p className="text-parchment-300/40 text-sm italic">{emptyText}</p>
      )}
      <div className="space-y-3">
        {categories.map((cat) => (
          <div key={cat}>
            <p className="text-[11px] font-mono text-parchment-300/40 mb-1.5">{cat}</p>
            <div className="flex flex-wrap gap-2">
              {grouped[cat].map((skill) => (
                <span
                  key={skill}
                  className={`text-sm px-3 py-1 rounded-full border ${TONE_STYLES[tone]}`}
                >
                  {skill}
                </span>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
