import React, { useState } from 'react';
import { GitCommit, ArrowRight, CornerDownRight } from 'lucide-react';

export default function TraceTab({ traceMatrix = [], onSelectLine, selectedLine }) {
  if (!traceMatrix || traceMatrix.length === 0) {
    return (
      <div style={{ color: 'var(--text-muted)', textAlign: 'center', padding: '2rem' }}>
        No traceability matrix available. Click "Compile" to generate.
      </div>
    );
  }

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.25rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-muted)' }}>
          <GitCommit size={16} color="var(--accent-cyan)" />
          <span style={{ fontSize: '0.9rem' }}>
            Full Pipeline Traceability Matrix ({traceMatrix.length} active statements)
          </span>
        </div>
        <div style={{ fontSize: '0.78rem', color: 'var(--text-faint)' }}>
          Source &rarr; AST &rarr; TAC &rarr; Target Assembly cross-mapping
        </div>
      </div>

      <div className="trace-grid">
        {traceMatrix.map((item, idx) => {
          const isSelected = selectedLine === item.sourceLine;

          return (
            <div
              key={idx}
              className={`trace-card ${isSelected ? 'active' : ''}`}
              onClick={() => onSelectLine && onSelectLine(item.sourceLine)}
            >
              {/* Line badge */}
              <div>
                <span
                  style={{
                    fontSize: '0.75rem',
                    fontWeight: 700,
                    fontFamily: 'var(--code-font)',
                    color: isSelected ? 'var(--accent-cyan)' : 'var(--text-faint)',
                    background: isSelected ? 'rgba(56, 189, 248, 0.15)' : 'rgba(255, 255, 255, 0.05)',
                    padding: '0.25rem 0.5rem',
                    borderRadius: '4px',
                    display: 'inline-block',
                  }}
                >
                  Line {item.sourceLine}
                </span>
              </div>

              {/* Source code */}
              <div>
                <span style={{ fontSize: '0.7rem', textTransform: 'uppercase', color: 'var(--text-faint)', display: 'block', marginBottom: '0.2rem' }}>
                  Source Code
                </span>
                <span className="code-cell" style={{ color: '#f8fafc', fontWeight: 600 }}>
                  {item.sourceCode || '(blank)'}
                </span>
              </div>

              {/* Intermediate TAC */}
              <div>
                <span style={{ fontSize: '0.7rem', textTransform: 'uppercase', color: 'var(--text-faint)', display: 'block', marginBottom: '0.2rem' }}>
                  Three-Address Code (TAC)
                </span>
                {item.tacInstructions && item.tacInstructions.length > 0 ? (
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '0.2rem' }}>
                    {item.tacInstructions.map((t, tIdx) => (
                      <div key={tIdx} className="code-cell" style={{ color: '#93c5fd', fontSize: '0.8rem' }}>
                        {t.text}
                      </div>
                    ))}
                  </div>
                ) : (
                  <span style={{ fontSize: '0.8rem', color: 'var(--text-faint)' }}>-</span>
                )}
              </div>

              {/* Target Instructions */}
              <div>
                <span style={{ fontSize: '0.7rem', textTransform: 'uppercase', color: 'var(--text-faint)', display: 'block', marginBottom: '0.2rem' }}>
                  Target Instructions
                </span>
                {item.targetInstructions && item.targetInstructions.length > 0 ? (
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '0.2rem' }}>
                    {item.targetInstructions.map((asm, aIdx) => (
                      <div key={aIdx} className="code-cell" style={{ color: '#86efac', fontSize: '0.8rem' }}>
                        {asm.text}
                      </div>
                    ))}
                  </div>
                ) : (
                  <span style={{ fontSize: '0.8rem', color: 'var(--text-faint)' }}>-</span>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
