import React from 'react';
import { Clock, Zap } from 'lucide-react';

export default function TimingBar({ timings, totalMs }) {
  if (!timings) return null;

  const stages = [
    { key: 'lexer', label: 'Lexer', color: '#c084fc' },
    { key: 'parser', label: 'Parser', color: '#38bdf8' },
    { key: 'semantic', label: 'Semantic', color: '#fbbf24' },
    { key: 'tac', label: 'TAC', color: '#60a5fa' },
    { key: 'optimizer', label: 'Optimizer', color: '#10b981' },
    { key: 'codegen', label: 'Codegen', color: '#ec4899' },
    { key: 'trace', label: 'Trace', color: '#a78bfa' },
  ];

  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      gap: '1rem',
      padding: '0.4rem 1.25rem',
      background: 'rgba(15, 23, 42, 0.9)',
      borderBottom: '1px solid var(--border-subtle)',
      fontSize: '0.75rem',
      overflowX: 'auto',
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem', color: 'var(--text-muted)', whiteSpace: 'nowrap' }}>
        <Clock size={13} color="var(--accent-cyan)" />
        <span style={{ fontWeight: 600 }}>Stage Timings:</span>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem', flex: 1 }}>
        {stages.map(({ key, label, color }) => {
          const val = timings[key] !== undefined ? timings[key] : 0.0;
          return (
            <div key={key} style={{ display: 'inline-flex', alignItems: 'center', gap: '0.3rem', whiteSpace: 'nowrap' }}>
              <span style={{ color: 'var(--text-faint)', fontSize: '0.7rem' }}>{label}:</span>
              <span style={{ fontFamily: 'var(--code-font)', color, fontWeight: 600 }}>
                {val.toFixed(2)}ms
              </span>
            </div>
          );
        })}
      </div>

      <div style={{ display: 'inline-flex', alignItems: 'center', gap: '0.35rem', color: 'var(--text-muted)', whiteSpace: 'nowrap' }}>
        <Zap size={13} color="var(--accent-emerald)" />
        <span>Total: <strong style={{ color: 'var(--accent-emerald)', fontFamily: 'var(--code-font)' }}>{totalMs}ms</strong></span>
      </div>
    </div>
  );
}
