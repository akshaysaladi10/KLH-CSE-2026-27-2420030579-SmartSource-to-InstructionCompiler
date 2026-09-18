import React from 'react';
import { Layers, ArrowRight } from 'lucide-react';

export default function TacTab({ tac = [], onSelectLine }) {
  if (!tac || tac.length === 0) {
    return (
      <div style={{ color: 'var(--text-muted)', textAlign: 'center', padding: '2rem' }}>
        No Three-Address Code available. Click "Compile" to generate.
      </div>
    );
  }

  // Count distinct temporaries
  const temporaries = new Set();
  tac.forEach((t) => {
    if (t.result && t.result.startsWith('t')) temporaries.add(t.result);
    if (t.arg1 && t.arg1.startsWith('t')) temporaries.add(t.arg1);
    if (t.arg2 && t.arg2.startsWith('t')) temporaries.add(t.arg2);
  });

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-muted)' }}>
          <Layers size={16} color="var(--accent-blue)" />
          <span style={{ fontSize: '0.9rem' }}>
            Linear Three-Address Code Quadruples ({tac.length} instructions)
          </span>
        </div>
        <div style={{ fontSize: '0.8rem', color: 'var(--text-faint)' }}>
          Temporaries allocated: <strong style={{ color: 'var(--accent-cyan)' }}>{temporaries.size}</strong> ({Array.from(temporaries).slice(0, 8).join(', ')}{temporaries.size > 8 ? '...' : ''})
        </div>
      </div>

      <div className="pipeline-table-wrapper">
        <table className="pipeline-table">
          <thead>
            <tr>
              <th style={{ width: '60px' }}>Index</th>
              <th>TAC Instruction</th>
              <th>Opcode</th>
              <th>Arg 1</th>
              <th>Arg 2</th>
              <th>Result</th>
              <th style={{ width: '80px' }}>Src Line</th>
            </tr>
          </thead>
          <tbody>
            {tac.map((instr, idx) => {
              const isLabel = instr.op === 'label';
              const isJump = instr.op === 'goto' || instr.op === 'ifFalse' || instr.op === 'ifTrue';

              return (
                <tr
                  key={idx}
                  onClick={() => onSelectLine && onSelectLine(instr.line)}
                  style={{
                    cursor: onSelectLine ? 'pointer' : 'default',
                    background: isLabel ? 'rgba(168, 85, 247, 0.06)' : undefined,
                  }}
                  title="Click to view originating source line"
                >
                  <td style={{ color: 'var(--text-faint)' }}>{idx}</td>
                  <td
                    className="code-cell"
                    style={{
                      fontWeight: 600,
                      color: isLabel ? '#c084fc' : isJump ? '#38bdf8' : '#e2e8f0',
                    }}
                  >
                    {instr.text}
                  </td>
                  <td>
                    <span className="badge" style={{ background: 'rgba(255,255,255,0.06)', color: '#94a3b8' }}>
                      {instr.op}
                    </span>
                  </td>
                  <td className="code-cell" style={{ color: 'var(--text-muted)' }}>
                    {instr.arg1 || '-'}
                  </td>
                  <td className="code-cell" style={{ color: 'var(--text-muted)' }}>
                    {instr.arg2 || '-'}
                  </td>
                  <td className="code-cell" style={{ color: 'var(--accent-cyan)' }}>
                    {instr.result || '-'}
                  </td>
                  <td className="code-cell">{instr.line}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
