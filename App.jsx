import React, { useState } from 'react'
import UploadPanel from './components/UploadPanel.jsx'
import ScoreGauge from './components/ScoreGauge.jsx'
import SkillGroup from './components/SkillGroup.jsx'

const API_BASE = import.meta.env.VITE_API_BASE || ''

export default function App() {
  const [file, setFile] = useState(null)
  const [jobDescription, setJobDescription] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [result, setResult] = useState(null)

  const canAnalyze = file && jobDescription.trim().length > 20 && !loading

  const handleAnalyze = async () => {
    if (!canAnalyze) return
    setLoading(true)
    setError(null)
    setResult(null)

    const formData = new FormData()
    formData.append('resume', file)
    formData.append('job_description', jobDescription)

    try {
      const res = await fetch(`${API_BASE}/api/analyze`, {
        method: 'POST',
        body: formData,
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.error || 'Something went wrong')
      setResult(data)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen relative bg-ink-900 text-parchment-100">
      <div className="grain-overlay" />
      <div className="relative z-10 max-w-6xl mx-auto px-6 py-10">
        {/* Header */}
        <header className="flex items-end justify-between border-b border-ink-700 pb-6 mb-10">
          <div>
            <p className="font-mono text-[11px] tracking-[0.15em] text-brass-400/80 mb-2">
              CASE FILE NO. 001
            </p>
            <h1 className="font-display text-4xl text-parchment-100">
              Docket <span className="text-parchment-300/40 font-normal text-2xl">— resume review, made legible</span>
            </h1>
          </div>
          <p className="hidden md:block font-mono text-xs text-parchment-300/40 max-w-[220px] text-right">
            Upload a resume, paste the job posting, get a scored verdict on fit.
          </p>
        </header>

        <div className="grid md:grid-cols-[380px_1fr] gap-8">
          {/* Intake panel */}
          <section className="bg-ink-800 border border-ink-700 rounded-xl p-6 h-fit">
            <p className="font-display text-xl text-parchment-100 mb-1">Intake</p>
            <p className="text-parchment-300/40 text-sm mb-6">Submit both exhibits to open a review.</p>

            <UploadPanel file={file} onFileSelected={setFile} />

            <div className="mt-6">
              <label className="text-[11px] font-mono tracking-wide text-parchment-300/50 uppercase">
                Exhibit B — Job description
              </label>
              <textarea
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                rows={10}
                placeholder="Paste the job posting here…"
                className="mt-2 w-full bg-ink-900 border border-ink-700 rounded-lg p-3 text-sm text-parchment-100 placeholder:text-parchment-300/30 focus:outline-none focus:border-brass-500/60 resize-none"
              />
            </div>

            <button
              onClick={handleAnalyze}
              disabled={!canAnalyze}
              className={`mt-5 w-full rounded-lg py-3 font-display text-lg tracking-wide transition-colors
                ${canAnalyze
                  ? 'bg-brass-500 hover:bg-brass-400 text-ink-950 cursor-pointer'
                  : 'bg-ink-700 text-parchment-300/30 cursor-not-allowed'}`}
            >
              {loading ? 'Reviewing…' : 'Open review'}
            </button>

            {error && (
              <p className="mt-3 text-rust-400 text-sm rise-in">{error}</p>
            )}
          </section>

          {/* Verdict panel */}
          <section className="bg-ink-800 border border-ink-700 rounded-xl p-6 min-h-[520px]">
            {!result && !loading && (
              <div className="h-full flex flex-col items-center justify-center text-center py-24">
                <div className="w-16 h-16 rounded-full border-2 border-dashed border-ink-700 flex items-center justify-center mb-4">
                  <span className="font-display text-2xl text-parchment-300/30">?</span>
                </div>
                <p className="text-parchment-300/40 max-w-xs text-sm">
                  Submit a resume and job description to open the verdict panel.
                </p>
              </div>
            )}

            {loading && (
              <div className="h-full flex flex-col items-center justify-center py-24">
                <div className="w-10 h-10 border-2 border-brass-500 border-t-transparent rounded-full animate-spin mb-4" />
                <p className="text-parchment-300/50 font-mono text-sm">Reading the record…</p>
              </div>
            )}

            {result && !loading && (
              <div className="rise-in">
                <div className="flex flex-col sm:flex-row gap-8 items-center sm:items-start border-b border-ink-700 pb-8 mb-8">
                  <ScoreGauge score={result.score} />
                  <div className="flex-1">
                    <p className="font-mono text-[11px] tracking-wide text-parchment-300/40 uppercase mb-2">
                      Verdict summary {result.used_genai && <span className="text-brass-400">· Claude-assisted</span>}
                    </p>
                    <p className="font-display text-xl text-parchment-100 leading-snug mb-4">
                      {result.summary}
                    </p>
                    <div className="flex gap-6 text-sm font-mono text-parchment-300/50">
                      <span>{result.matched_count} of {result.required_count} required skills matched</span>
                    </div>
                    {result.contact_info?.name && (
                      <p className="mt-3 text-xs font-mono text-parchment-300/30">
                        Candidate on file: {result.contact_info.name}
                      </p>
                    )}
                  </div>
                </div>

                <div className="grid sm:grid-cols-2 gap-8 mb-8">
                  <SkillGroup
                    title="Matched skills"
                    grouped={result.matched_grouped}
                    tone="matched"
                    emptyText="No overlapping skills found."
                  />
                  <SkillGroup
                    title="Missing skills"
                    grouped={result.missing_grouped}
                    tone="missing"
                    emptyText="Nothing missing — full coverage."
                  />
                </div>

                {result.bonus_skills?.length > 0 && (
                  <div className="mb-8">
                    <h4 className="font-display text-lg text-parchment-100 mb-3">Bonus skills on record</h4>
                    <div className="flex flex-wrap gap-2">
                      {result.bonus_skills.map((s) => (
                        <span key={s} className="text-sm px-3 py-1 rounded-full border bg-brass-500/10 text-brass-400 border-brass-500/40">
                          {s}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                <div>
                  <h4 className="font-display text-lg text-parchment-100 mb-3">Recommendations</h4>
                  <ul className="space-y-2">
                    {result.suggestions?.map((s, i) => (
                      <li key={i} className="flex gap-3 text-sm text-parchment-200">
                        <span className="text-brass-400 font-mono">{String(i + 1).padStart(2, '0')}</span>
                        <span>{s}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            )}
          </section>
        </div>

        <footer className="mt-10 text-center text-parchment-300/25 text-xs font-mono">
          Runs locally — nothing leaves your machine unless GenAI enrichment is enabled.
        </footer>
      </div>
    </div>
  )
}
