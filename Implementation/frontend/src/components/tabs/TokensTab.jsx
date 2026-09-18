import React, { useState } from 'react';
import { Search } from 'lucide-react';

export default function TokensTab({ tokens = [], onSelectLine }) {
  const [filter, setFilter] = useState('');

  const filteredTokens = tokens.filter((t) => {
    if (!filter) return true;
    const q = filter.toLowerCase();
    return (
      t.token.toLowerCase().includes(q) ||
      t.lexeme.toLowerCase().includes(q) ||
      t.type.toLowerCase().includes(q)
    );
  });

  const getBadgeClass = (category) => {
    switch (category) {
      case 'Keyword':
        return 'badge-keyword';
      case 'Identifier':
        return 'badge-identifier';
      case 'Literal':
        return 'badge-literal';
      case 'Operator':
        return 'badge-operator';
      case 'Delimiter':
      case 'Separator':
        return 'badge-delimiter';
      default:
        return 'badge';
    }
  };

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1rem' }}>
        <div style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>
          Total Tokens: <strong style={{ color: 'var(--text-main)' }}>{tokens.length}</strong>
        </div>
        <div style={{ position: 'relative', width: '240px' }}>
          <Search size={14} style={{ position: 'absolute', left: '10px', top: '10px', color: 'var(--text-faint)' }} />
          <input
            type="text"
            placeholder="Search tokens..."
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            style={{
              width: '100%',
              padding: '0.45rem 0.8rem 0.45rem 2rem',
              background: 'var(--bg-panel)',
              border: '1px solid var(--border-subtle)',
              borderRadius: 'var(--radius-sm)',
              color: 'var(--text-main)',
              fontSize: '0.825rem',
              outline: 'none',
            }}
          />
        </div>
      </div>

      <div className="pipeline-table-wrapper">
        <table className="pipeline-table">
          <thead>
            <tr>
              <th style={{ width: '60px' }}>#</th>
              <th>Token</th>
              <th>Lexeme</th>
              <th>Type / Category</th>
              <th style={{ width: '80px' }}>Line</th>
              <th style={{ width: '80px' }}>Column</th>
            </tr>
          </thead>
          <tbody>
            {filteredTokens.map((t, idx) => (
              <tr
                key={idx}
                onClick={() => onSelectLine && onSelectLine(t.line)}
                style={{ cursor: onSelectLine ? 'pointer' : 'default' }}
                title="Click to view line in source code"
              >
                <td style={{ color: 'var(--text-faint)' }}>{idx + 1}</td>
                <td className="code-cell" style={{ fontWeight: 600, color: 'var(--accent-cyan)' }}>
                  {t.token}
                </td>
                <td className="code-cell" style={{ color: '#f8fafc' }}>
                  {t.lexeme === '' ? '<EOF>' : t.lexeme}
                </td>
                <td>
                  <span className={`badge ${getBadgeClass(t.type)}`}>
                    {t.type}
                  </span>
                </td>
                <td className="code-cell">{t.line}</td>
                <td className="code-cell">{t.column}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
