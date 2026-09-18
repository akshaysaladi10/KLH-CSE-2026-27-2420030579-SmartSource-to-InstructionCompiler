import React from 'react';
import { CheckCircle2, XCircle, Clock, Zap, Hash, GitCommit, Binary } from 'lucide-react';

export default function Dashboard({ statistics }) {
  if (!statistics) {
    return (
      <div className="dashboard-bar">
        <div style={{ color: 'var(--text-faint)', fontSize: '0.8rem', padding: '0.2rem' }}>
          Ready to compile. Press "Compile" or select a sample program.
        </div>
      </div>
    );
  }

  const {
    sourceLines = 0,
    tokensCount = 0,
    astNodesCount = 0,
    symbolsCount = 0,
    tacInstructionsCount = 0,
    optimizedTacCount = 0,
    optimizationsCount = 0,
    targetInstructionsCount = 0,
    compilationTimeMs = 0,
    status = 'Ready',
    hasErrors = false,
  } = statistics;

  return (
    <div className="dashboard-bar">
      <div className="metric-card" style={{ borderColor: hasErrors ? 'rgba(244, 63, 94, 0.4)' : 'rgba(16, 185, 129, 0.4)' }}>
        <span className="metric-label">Status</span>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem', marginTop: '0.1rem' }}>
          {hasErrors ? (
            <XCircle size={15} color="var(--accent-rose)" />
          ) : (
            <CheckCircle2 size={15} color="var(--accent-emerald)" />
          )}
          <span
            style={{
              fontSize: '0.825rem',
              fontWeight: 600,
              color: hasErrors ? 'var(--accent-rose)' : 'var(--accent-emerald)',
            }}
          >
            {hasErrors ? 'Failed' : 'Success'}
          </span>
        </div>
      </div>

      <div className="metric-card">
        <span className="metric-label">Source Lines</span>
        <span className="metric-value">{sourceLines}</span>
      </div>

      <div className="metric-card">
        <span className="metric-label">Tokens</span>
        <span className="metric-value" style={{ color: '#c084fc' }}>{tokensCount}</span>
      </div>

      <div className="metric-card">
        <span className="metric-label">AST Nodes</span>
        <span className="metric-value" style={{ color: '#38bdf8' }}>{astNodesCount}</span>
      </div>

      <div className="metric-card">
        <span className="metric-label">Symbols</span>
        <span className="metric-value" style={{ color: '#fbbf24' }}>{symbolsCount}</span>
      </div>

      <div className="metric-card">
        <span className="metric-label">TAC Instructions</span>
        <span className="metric-value">{tacInstructionsCount}</span>
      </div>

      <div className="metric-card">
        <span className="metric-label">Optimizations</span>
        <span className="metric-value" style={{ color: '#10b981' }}>{optimizationsCount}</span>
      </div>

      <div className="metric-card">
        <span className="metric-label">Target Instructions</span>
        <span className="metric-value" style={{ color: '#3b82f6' }}>{targetInstructionsCount}</span>
      </div>

      <div className="metric-card">
        <span className="metric-label">Compile Time</span>
        <span className="metric-value" style={{ fontSize: '0.95rem', color: 'var(--text-muted)' }}>
          {compilationTimeMs}ms
        </span>
      </div>
    </div>
  );
}
