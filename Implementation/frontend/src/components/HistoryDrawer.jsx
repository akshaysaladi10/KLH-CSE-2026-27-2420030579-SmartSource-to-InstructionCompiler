import React from 'react';
import { History, X, Trash2, ArrowUpRight, CheckCircle2, XCircle } from 'lucide-react';

export default function HistoryDrawer({
  isOpen,
  onClose,
  history = [],
  onLoadCode,
  onClearHistory,
}) {
  if (!isOpen) return null;

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      right: 0,
      bottom: 0,
      width: '420px',
      background: 'var(--bg-panel)',
      borderLeft: '1px solid var(--border-subtle)',
      zIndex: 90,
      display: 'flex',
      flexDirection: 'column',
      boxShadow: '-10px 0 25px -5px rgba(0, 0, 0, 0.5)',
    }}>
      {/* Header */}
      <div style={{
        padding: '1rem 1.25rem',
        borderBottom: '1px solid var(--border-subtle)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        background: 'rgba(15, 23, 42, 0.6)',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <History size={16} color="var(--accent-cyan)" />
          <h4 style={{ fontSize: '0.95rem', fontWeight: 600, color: 'var(--text-main)' }}>
            Compilation History ({history.length})
          </h4>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          {history.length > 0 && (
            <button
              onClick={onClearHistory}
              title="Clear all saved compilations"
              style={{
                background: 'transparent',
                border: 'none',
                color: 'var(--text-faint)',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '0.2rem',
                fontSize: '0.75rem',
              }}
            >
              <Trash2 size={13} /> Clear
            </button>
          )}
          <button
            onClick={onClose}
            style={{
              background: 'transparent',
              border: 'none',
              color: 'var(--text-muted)',
              cursor: 'pointer',
              display: 'flex',
              padding: '2px',
            }}
          >
            <X size={18} />
          </button>
        </div>
      </div>

      {/* History List */}
      <div style={{ padding: '1rem', overflowY: 'auto', flex: 1, display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
        {history.length === 0 ? (
          <div style={{ color: 'var(--text-faint)', textAlign: 'center', padding: '3rem 1rem', fontSize: '0.85rem' }}>
            No compilation history yet. Compiling programs will automatically save them here.
          </div>
        ) : (
          history.map((item, idx) => (
            <div
              key={idx}
              style={{
                background: 'var(--bg-card)',
                border: '1px solid var(--border-subtle)',
                borderRadius: 'var(--radius-sm)',
                padding: '0.75rem',
                display: 'flex',
                flexDirection: 'column',
                gap: '0.4rem',
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                  {item.success ? (
                    <CheckCircle2 size={13} color="var(--accent-emerald)" />
                  ) : (
                    <XCircle size={13} color="var(--accent-rose)" />
                  )}
                  <span style={{ fontSize: '0.75rem', fontWeight: 600, color: item.success ? 'var(--accent-emerald)' : 'var(--accent-rose)' }}>
                    {item.success ? 'Success' : 'Failed'}
                  </span>
                </div>
                <span style={{ fontSize: '0.7rem', color: 'var(--text-faint)' }}>
                  {new Date(item.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })}
                </span>
              </div>

              <div style={{
                background: '#080c14',
                padding: '0.4rem 0.5rem',
                borderRadius: '4px',
                fontFamily: 'var(--code-font)',
                fontSize: '0.75rem',
                color: '#cbd5e1',
                maxHeight: '60px',
                overflow: 'hidden',
                textOverflow: 'ellipsis',
                whiteSpace: 'pre',
              }}>
                {item.codeSnippet || '// code'}
              </div>

              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginTop: '0.2rem' }}>
                <span style={{ fontSize: '0.72rem', color: 'var(--text-faint)' }}>
                  {item.targetCount || 0} instrs | {item.lines || 0} lines
                </span>
                <button
                  onClick={() => {
                    onLoadCode(item.fullCode);
                    onClose();
                  }}
                  style={{
                    background: 'rgba(56, 189, 248, 0.12)',
                    border: '1px solid rgba(56, 189, 248, 0.3)',
                    color: 'var(--accent-cyan)',
                    padding: '0.25rem 0.6rem',
                    borderRadius: '4px',
                    fontSize: '0.72rem',
                    fontWeight: 600,
                    cursor: 'pointer',
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '0.25rem',
                  }}
                >
                  <ArrowUpRight size={12} /> Load to Editor
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
