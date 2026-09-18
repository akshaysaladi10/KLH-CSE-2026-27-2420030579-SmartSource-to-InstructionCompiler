import React from 'react';
import { Sparkles, ArrowRight, CheckCircle, Zap, RefreshCw, Sliders } from 'lucide-react';

export default function OptimizationTab({
  tac = [],
  optimizedTac = [],
  optimizations = [],
  enabledPasses,
  onTogglePass,
  onReoptimize,
  onSelectLine,
}) {
  if (!tac || tac.length === 0) {
    return (
      <div style={{ color: 'var(--text-muted)', textAlign: 'center', padding: '2rem' }}>
        No optimization data available. Click "Compile" to generate.
      </div>
    );
  }

  const reduction =
    tac.length > 0
      ? Math.round(((tac.length - optimizedTac.length) / tac.length) * 100)
      : 0;

  const passes = [
    { id: 'constant_folding', label: 'Constant Folding', desc: '10 + 20 -> 30' },
    { id: 'constant_propagation', label: 'Constant Propagation', desc: 'x = 10; y = x + 5 -> y = 15' },
    { id: 'algebraic_simplification', label: 'Algebraic Simplification', desc: 'x + 0 -> x, x * 1 -> x, x * 0 -> 0' },
    { id: 'dead_code_elimination', label: 'Dead Code Elimination', desc: 'Removes unused temporaries & dead jump branches' },
  ];

  return (
    <div>
      {/* Optimization Playground Controls */}
      <div style={{
        background: 'var(--bg-panel)',
        border: '1px solid var(--border-subtle)',
        borderRadius: 'var(--radius-md)',
        padding: '0.85rem 1.15rem',
        marginBottom: '1.25rem',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.65rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-muted)' }}>
            <Sliders size={16} color="var(--accent-cyan)" />
            <span style={{ fontSize: '0.9rem', fontWeight: 600, color: 'var(--text-main)' }}>
              Optimization Playground (Selective Pass Toggling)
            </span>
          </div>
          <button
            className="btn btn-secondary"
            onClick={onReoptimize}
            style={{ padding: '0.35rem 0.75rem', fontSize: '0.78rem' }}
          >
            <RefreshCw size={13} /> Re-Optimize
          </button>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '0.6rem' }}>
          {passes.map((p) => {
            const isChecked = !enabledPasses || enabledPasses.includes(p.id);
            return (
              <label
                key={p.id}
                style={{
                  display: 'flex',
                  alignItems: 'flex-start',
                  gap: '0.5rem',
                  background: isChecked ? 'rgba(56, 189, 248, 0.08)' : 'rgba(255, 255, 255, 0.03)',
                  border: '1px solid',
                  borderColor: isChecked ? 'rgba(56, 189, 248, 0.25)' : 'var(--border-subtle)',
                  borderRadius: 'var(--radius-sm)',
                  padding: '0.45rem 0.65rem',
                  cursor: 'pointer',
                }}
              >
                <input
                  type="checkbox"
                  checked={isChecked}
                  onChange={() => onTogglePass && onTogglePass(p.id)}
                  style={{ marginTop: '3px', cursor: 'pointer' }}
                />
                <div>
                  <div style={{ fontSize: '0.8rem', fontWeight: 600, color: isChecked ? 'var(--text-main)' : 'var(--text-faint)' }}>
                    {p.label}
                  </div>
                  <div style={{ fontSize: '0.7rem', color: 'var(--text-faint)' }}>
                    {p.desc}
                  </div>
                </div>
              </label>
            );
          })}
        </div>
      </div>

      {/* Overview Analytics Bar */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.25rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-muted)' }}>
          <Zap size={16} color="var(--accent-emerald)" />
          <span style={{ fontSize: '0.9rem' }}>
            Optimization Results ({optimizations.length} transformations applied)
          </span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', fontSize: '0.85rem' }}>
          <span>
            Original: <strong style={{ color: 'var(--text-main)' }}>{tac.length}</strong> instrs
          </span>
          <ArrowRight size={14} color="var(--text-faint)" />
          <span>
            Optimized: <strong style={{ color: 'var(--accent-emerald)' }}>{optimizedTac.length}</strong> instrs
          </span>
          <span
            className="badge"
            style={{
              background: reduction > 0 ? 'rgba(16, 185, 129, 0.15)' : 'rgba(255, 255, 255, 0.06)',
              color: reduction > 0 ? '#10b981' : 'var(--text-faint)',
              border: `1px solid ${reduction > 0 ? 'rgba(16, 185, 129, 0.3)' : 'transparent'}`,
            }}
          >
            {reduction > 0 ? `-${reduction}% Reduction` : '0% Reduction'}
          </span>
        </div>
      </div>

      {/* Side by Side Diff */}
      <div className="diff-container">
        <div className="diff-column">
          <div className="diff-header">
            <span style={{ color: 'var(--text-muted)' }}>Before Optimization (Raw TAC)</span>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-faint)' }}>{tac.length} lines</span>
          </div>
          <div className="diff-body">
            {tac.map((instr, idx) => (
              <div
                key={idx}
                onClick={() => onSelectLine && onSelectLine(instr.line)}
                style={{ cursor: onSelectLine ? 'pointer' : 'default', padding: '2px 4px', borderRadius: '3px' }}
                title="Click to view source line"
              >
                <span style={{ color: 'var(--text-faint)', marginRight: '1rem', userSelect: 'none' }}>
                  {String(idx).padStart(2, ' ')}
                </span>
                <span style={{ color: '#cbd5e1' }}>{instr.text}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="diff-column">
          <div className="diff-header">
            <span style={{ color: 'var(--accent-emerald)' }}>After Optimization (Pass Complete)</span>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-faint)' }}>{optimizedTac.length} lines</span>
          </div>
          <div className="diff-body">
            {optimizedTac.map((instr, idx) => (
              <div
                key={idx}
                onClick={() => onSelectLine && onSelectLine(instr.line)}
                style={{ cursor: onSelectLine ? 'pointer' : 'default', padding: '2px 4px', borderRadius: '3px' }}
                title="Click to view source line"
              >
                <span style={{ color: 'var(--text-faint)', marginRight: '1rem', userSelect: 'none' }}>
                  {String(idx).padStart(2, ' ')}
                </span>
                <span style={{ color: '#86efac' }}>{instr.text}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Applied Transformations List */}
      <div style={{ marginTop: '1.5rem' }}>
        <h4 style={{ fontSize: '0.85rem', textTransform: 'uppercase', color: 'var(--text-faint)', marginBottom: '0.75rem', letterSpacing: '0.04em' }}>
          Transformation Log ({optimizations.length} actions)
        </h4>

        {optimizations.length === 0 ? (
          <div style={{ color: 'var(--text-muted)', fontSize: '0.85rem', background: 'var(--bg-panel)', padding: '1rem', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-subtle)' }}>
            Code is already in canonical optimal form or selected passes produced no modifications.
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            {optimizations.map((opt, idx) => (
              <div
                key={idx}
                onClick={() => onSelectLine && onSelectLine(opt.line)}
                style={{
                  background: 'var(--bg-panel)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: 'var(--radius-sm)',
                  padding: '0.65rem 1rem',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  cursor: onSelectLine ? 'pointer' : 'default',
                }}
              >
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <span
                      className="badge"
                      style={{
                        background:
                          opt.pass === 'Constant Folding'
                            ? 'rgba(56, 189, 248, 0.15)'
                            : opt.pass === 'Constant Propagation'
                            ? 'rgba(168, 85, 247, 0.15)'
                            : opt.pass === 'Algebraic Simplification'
                            ? 'rgba(245, 158, 11, 0.15)'
                            : 'rgba(244, 63, 94, 0.15)',
                        color:
                          opt.pass === 'Constant Folding'
                            ? '#38bdf8'
                            : opt.pass === 'Constant Propagation'
                            ? '#c084fc'
                            : opt.pass === 'Algebraic Simplification'
                            ? '#fbbf24'
                            : '#fb7185',
                      }}
                    >
                      {opt.pass}
                    </span>
                    <span style={{ fontSize: '0.85rem', color: 'var(--text-main)' }}>
                      {opt.description}
                    </span>
                  </div>
                  <div style={{ fontSize: '0.78rem', color: 'var(--text-faint)', marginTop: '0.3rem', fontFamily: 'var(--code-font)' }}>
                    <span style={{ color: '#f87171', textDecoration: 'line-through' }}>{opt.before}</span>
                    <span style={{ margin: '0 0.5rem', color: 'var(--text-faint)' }}>&rarr;</span>
                    <span style={{ color: '#4ade80' }}>{opt.after}</span>
                  </div>
                </div>

                <span style={{ fontSize: '0.75rem', color: 'var(--text-faint)', fontFamily: 'var(--code-font)' }}>
                  Line {opt.line}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
