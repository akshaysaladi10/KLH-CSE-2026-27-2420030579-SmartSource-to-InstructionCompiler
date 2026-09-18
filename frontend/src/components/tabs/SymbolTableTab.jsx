import React from 'react';
import { Database, Check, X } from 'lucide-react';

export default function SymbolTableTab({ symbolTable = [], onSelectLine }) {
  if (!symbolTable || symbolTable.length === 0) {
    return (
      <div style={{ color: 'var(--text-muted)', textAlign: 'center', padding: '2rem' }}>
        No symbols found in the symbol table.
      </div>
    );
  }

  const getTypeBadgeColor = (type) => {
    switch (type) {
      case 'int': return '#38bdf8';
      case 'float': return '#f59e0b';
      case 'string': return '#10b981';
      case 'bool': return '#ec4899';
      default: return '#94a3b8';
    }
  };

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem', color: 'var(--text-muted)' }}>
        <Database size={16} color="var(--accent-amber)" />
        <span style={{ fontSize: '0.9rem' }}>
          Scoped Symbol Table ({symbolTable.length} recorded symbols)
        </span>
      </div>

      <div className="pipeline-table-wrapper">
        <table className="pipeline-table">
          <thead>
            <tr>
              <th style={{ width: '50px' }}>#</th>
              <th>Name</th>
              <th>Type</th>
              <th>Scope</th>
              <th>Initialized?</th>
              <th>Line</th>
              <th>Column</th>
              <th>Value / Notes</th>
            </tr>
          </thead>
          <tbody>
            {symbolTable.map((sym, idx) => (
              <tr
                key={idx}
                onClick={() => onSelectLine && onSelectLine(sym.line)}
                style={{ cursor: onSelectLine ? 'pointer' : 'default' }}
                title="Click to view declaration line"
              >
                <td style={{ color: 'var(--text-faint)' }}>{idx + 1}</td>
                <td className="code-cell" style={{ fontWeight: 600, color: 'var(--text-main)' }}>
                  {sym.name}
                </td>
                <td>
                  <span
                    className="badge"
                    style={{
                      background: `rgba(255,255,255,0.08)`,
                      color: getTypeBadgeColor(sym.type),
                      border: `1px solid ${getTypeBadgeColor(sym.type)}40`,
                    }}
                  >
                    {sym.type}
                  </span>
                </td>
                <td style={{ color: 'var(--text-muted)' }}>
                  {sym.scope}
                </td>
                <td>
                  {sym.isInitialized ? (
                    <span style={{ display: 'inline-flex', alignItems: 'center', gap: '0.25rem', color: 'var(--accent-emerald)', fontSize: '0.8rem' }}>
                      <Check size={14} /> Yes
                    </span>
                  ) : (
                    <span style={{ display: 'inline-flex', alignItems: 'center', gap: '0.25rem', color: 'var(--accent-rose)', fontSize: '0.8rem' }}>
                      <X size={14} /> No
                    </span>
                  )}
                </td>
                <td className="code-cell">{sym.line}</td>
                <td className="code-cell">{sym.column}</td>
                <td className="code-cell" style={{ color: 'var(--text-faint)' }}>
                  {sym.value}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
