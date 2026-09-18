import React from 'react';
import { AlertTriangle, HelpCircle, ArrowRight } from 'lucide-react';

export default function ErrorPanel({ errors, onSelectLine }) {
  if (!errors || errors.length === 0) return null;

  return (
    <div className="error-panel">
      <div className="error-title">
        <AlertTriangle size={18} />
        <span>Compilation Diagnostics ({errors.length} {errors.length === 1 ? 'Error' : 'Errors'})</span>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
        {errors.map((err, idx) => (
          <div
            key={idx}
            className="error-item"
            onClick={() => onSelectLine && onSelectLine(err.line)}
            style={{ cursor: onSelectLine ? 'pointer' : 'default' }}
            title="Click to locate in editor"
          >
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <span style={{ fontWeight: 600, color: 'var(--accent-rose)' }}>
                {err.errorType || 'Compilation Error'}
              </span>
              <span className="error-meta">
                Line {err.line} : Col {err.column}
              </span>
            </div>

            <div className="error-msg">{err.message}</div>

            {err.possibleCause && (
              <div className="error-cause">
                <span style={{ fontWeight: 600, color: 'rgba(255,255,255,0.7)' }}>Tip: </span>
                {err.possibleCause}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
