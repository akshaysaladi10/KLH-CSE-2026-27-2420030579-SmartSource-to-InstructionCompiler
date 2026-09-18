import React, { useState } from 'react';
import { Cpu, Copy, Check, CircleDot } from 'lucide-react';

export default function AssemblyTab({
  instructions = [],
  breakpoints = [],
  onToggleBreakpoint,
  onSelectLine,
  onSelectInstruction,
  selectedInstructionId,
}) {
  const [copied, setCopied] = useState(false);

  if (!instructions || instructions.length === 0) {
    return (
      <div style={{ color: 'var(--text-muted)', textAlign: 'center', padding: '2rem' }}>
        No target instructions available. Click "Compile" to generate.
      </div>
    );
  }

  // Count distinct registers used
  const registers = new Set();
  instructions.forEach((i) => {
    if (i.arg1 && i.arg1.startsWith('R')) registers.add(i.arg1);
    if (i.arg2 && i.arg2.startsWith('R')) registers.add(i.arg2);
  });

  const fullAsmText = instructions.map((i) => i.text).join('\n');

  const handleCopy = () => {
    navigator.clipboard.writeText(fullAsmText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const getOpcodeColor = (op) => {
    switch (op) {
      case 'LOAD':
      case 'STORE':
      case 'MOV':
        return '#38bdf8';
      case 'ADD':
      case 'SUB':
      case 'MUL':
      case 'DIV':
      case 'MOD':
        return '#fbbf24';
      case 'CMP':
      case 'SETEQ':
      case 'SETNE':
      case 'SETLT':
      case 'SETGT':
        return '#ec4899';
      case 'JMP':
      case 'JZ':
      case 'JNZ':
      case 'JL':
      case 'JG':
      case 'JLE':
      case 'JGE':
        return '#a855f7';
      case 'LABEL':
        return '#c084fc';
      case 'PRINT':
        return '#10b981';
      case 'HALT':
        return '#f43f5e';
      default:
        return '#94a3b8';
    }
  };

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-muted)' }}>
          <Cpu size={16} color="var(--accent-cyan)" />
          <span style={{ fontSize: '0.9rem' }}>
            Pseudo-Assembly Output ({instructions.length} instructions)
          </span>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-faint)' }}>
            Allocated Registers: <strong style={{ color: 'var(--accent-cyan)' }}>{registers.size}</strong> ({Array.from(registers).sort().join(', ')})
          </span>
          <button
            className="btn btn-secondary"
            onClick={handleCopy}
            style={{ padding: '0.35rem 0.75rem', fontSize: '0.8rem' }}
          >
            {copied ? <Check size={14} color="#10b981" /> : <Copy size={14} />}
            {copied ? 'Copied' : 'Copy Assembly'}
          </button>
        </div>
      </div>

      <div style={{ fontSize: '0.78rem', color: 'var(--text-faint)', marginBottom: '0.75rem' }}>
        Tip: Click the left gutter to toggle <strong>Breakpoints</strong> for the VM Debugger, or click any instruction to highlight its originating source line.
      </div>

      <div className="pipeline-table-wrapper">
        <table className="pipeline-table">
          <thead>
            <tr>
              <th style={{ width: '40px', textAlign: 'center' }}>BP</th>
              <th style={{ width: '50px' }}>PC</th>
              <th style={{ width: '100px' }}>Opcode</th>
              <th>Operands</th>
              <th>Comment / Trace Context</th>
              <th style={{ width: '80px' }}>Src Line</th>
            </tr>
          </thead>
          <tbody>
            {instructions.map((instr, idx) => {
              const isLabel = instr.op === 'LABEL';
              const isHalt = instr.op === 'HALT';
              const hasBreakpoint = breakpoints.includes(idx);
              const isSelected = selectedInstructionId === (instr.instructionId ?? idx);

              return (
                <tr
                  key={idx}
                  onClick={() => {
                    if (onSelectInstruction) onSelectInstruction(instr);
                    if (onSelectLine) onSelectLine(instr.sourceLine);
                  }}
                  style={{
                    cursor: 'pointer',
                    background: isSelected
                      ? 'rgba(56, 189, 248, 0.12)'
                      : isLabel
                      ? 'rgba(168, 85, 247, 0.05)'
                      : isHalt
                      ? 'rgba(244, 63, 94, 0.05)'
                      : undefined,
                  }}
                  title="Click to highlight originating source line"
                >
                  {/* Breakpoint toggle */}
                  <td
                    style={{ textAlign: 'center', cursor: 'pointer' }}
                    onClick={(e) => {
                      e.stopPropagation();
                      if (onToggleBreakpoint) onToggleBreakpoint(idx);
                    }}
                    title={hasBreakpoint ? 'Remove Breakpoint' : 'Set Breakpoint'}
                  >
                    {hasBreakpoint ? (
                      <span style={{ color: '#ef4444', fontSize: '1.1rem', lineHeight: 1 }}>●</span>
                    ) : (
                      <span style={{ color: 'rgba(255,255,255,0.15)', fontSize: '0.8rem' }}>○</span>
                    )}
                  </td>

                  <td style={{ color: 'var(--text-faint)' }}>{idx}</td>
                  <td className="code-cell" style={{ fontWeight: 700, color: getOpcodeColor(instr.op) }}>
                    {instr.op}
                  </td>
                  <td className="code-cell" style={{ color: '#e2e8f0' }}>
                    {instr.arg2 ? `${instr.arg1}, ${instr.arg2}` : instr.arg1 || ''}
                  </td>
                  <td className="code-cell" style={{ color: 'var(--text-faint)', fontStyle: 'italic' }}>
                    {instr.comment ? `; ${instr.comment}` : ''}
                  </td>
                  <td className="code-cell" style={{ color: 'var(--accent-cyan)' }}>
                    {instr.sourceLine}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
