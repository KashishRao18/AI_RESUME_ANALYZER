import React, { useRef, useState } from 'react'

export default function UploadPanel({ file, onFileSelected }) {
  const inputRef = useRef(null)
  const [dragging, setDragging] = useState(false)

  const handleFiles = (files) => {
    if (files && files[0]) onFileSelected(files[0])
  }

  return (
    <div>
      <label className="text-[11px] font-mono tracking-wide text-parchment-300/50 uppercase">
        Exhibit A — Resume
      </label>
      <div
        onClick={() => inputRef.current?.click()}
        onDragOver={(e) => { e.preventDefault(); setDragging(true) }}
        onDragLeave={() => setDragging(false)}
        onDrop={(e) => {
          e.preventDefault()
          setDragging(false)
          handleFiles(e.dataTransfer.files)
        }}
        className={`mt-2 cursor-pointer rounded-lg border-2 border-dashed transition-colors px-5 py-8 text-center
          ${dragging ? 'border-brass-400 bg-brass-500/5' : 'border-ink-700 hover:border-brass-500/50'}`}
      >
        <input
          ref={inputRef}
          type="file"
          accept=".pdf,.docx,.txt"
          className="hidden"
          onChange={(e) => handleFiles(e.target.files)}
        />
        {file ? (
          <div>
            <p className="font-display text-parchment-100 text-lg">{file.name}</p>
            <p className="text-parchment-300/40 text-xs mt-1 font-mono">
              {(file.size / 1024).toFixed(0)} KB — click to replace
            </p>
          </div>
        ) : (
          <div>
            <p className="text-parchment-200 text-sm">
              Drop a resume here, or <span className="text-brass-400 underline underline-offset-2">browse</span>
            </p>
            <p className="text-parchment-300/40 text-xs mt-1 font-mono">PDF · DOCX · TXT</p>
          </div>
        )}
      </div>
    </div>
  )
}
