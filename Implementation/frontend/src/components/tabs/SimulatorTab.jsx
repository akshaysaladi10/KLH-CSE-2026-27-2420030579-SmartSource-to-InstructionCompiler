import React, { useState, useEffect } from 'react';
import { Play, SkipForward, SkipBack, RotateCcw, Cpu, Terminal, AlertTriangle, CircleDot, Pause, FastForward } from 'lucide-react';

export default function SimulatorTab({
  simulationData,
  instructions = [],
  breakpoints = [],
  onToggleBreakpoint,
  onRunSimulate,
}) {
  const [currentStepIndex, setCurrentStepIndex] = useState(0);

  const history = simulationData?.stepHistory || [];
  const maxSteps = history.length;

  useEffect(() => {
    if (history.length > 0) {
      setCurrentStepIndex(history.length - 1);
    } else {
      setCurrentStepIndex(0);
    }
  }, [simulationData]);

  if (!instructions || instructions.length === 0) {
    return (
      <div style={{ color: 'var(--text-muted)', textAlign: 'center', padding: '2rem' }}>
        No compiled instructions to simulate. Click "Compile" first.
      </div>
    );
  }

  if (!simulationData) {
    return (
      <div style={{ textAlign: 'center', padding: '3rem' }}>
        <Cpu size={40} color="var(--accent-cyan)" style={{ marginBottom: '1rem' }} />
        <h3 style={{ color: 'var(--text-main)', marginBottom: '0.5rem' }}>
          Target Virtual Machine Simulator &amp; Debugger
        </h3>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem', marginBottom: '1.5rem', maxWidth: '520px', margin: '0 auto 1.5rem' }}>
          Execute the generated pseudo-assembly step-by-step or run to breakpoints, inspecting 32-bit registers (R0-R7), condition flags (Z, S, GT, LT), memory slots, and console output.
        </p>
        <button className="btn btn-success" onClick={onRunSimulate}>
          <Play size={15} /> Launch Simulation
        </button>
      </div>
    );
  }

  const currentStep = history[currentStepIndex] || {
    step: 0,
    pc: 0,
    registers: simulationData.registers || {},
    memory: simulationData.memory || {},
    flags: simulationData.flags || {},
    output: simulationData.output || [],
  };

  const currentPc = currentStep.pc;
  const registers = currentStep.registers || {};
  const memory = currentStep.memory || {};
  const flags = currentStep.flags || simulationData.flags || { zero: false, sign: false, greater: false, less: false };
  const output = currentStep.output || [];

  return (
    <div>
      {/* Controls Bar */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.25rem', flexWrap: 'wrap', gap: '0.75rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <button
            className="btn btn-secondary"
            onClick={() => setCurrentStepIndex(0)}
            disabled={currentStepIndex <= 0}
            title="Reset to instruction 0"
            style={{ padding: '0.4rem 0.6rem' }}
          >
            <RotateCcw size={14} />
          </button>
          <button
            className="btn btn-secondary"
            onClick={() => setCurrentStepIndex((prev) => Math.max(0, prev - 1))}
            disabled={currentStepIndex <= 0}
            title="Step Back"
          >
            <SkipBack size={14} /> Back
          </button>
          <button
            className="btn btn-primary"
            onClick={() => setCurrentStepIndex((prev) => Math.min(maxSteps - 1, prev + 1))}
            disabled={currentStepIndex >= maxSteps - 1}
            title="Step Forward"
          >
            <SkipForward size={14} /> Step Next
          </button>
          <button
            className="btn btn-success"
            onClick={onRunSimulate}
            title="Run / Continue execution until breakpoint or halt"
          >
            <Play size={14} /> Continue
          </button>
          <button
            className="btn btn-secondary"
            onClick={() => setCurrentStepIndex(maxSteps - 1)}
            disabled={currentStepIndex >= maxSteps - 1}
            title="Fast Forward to End"
          >
            <FastForward size={14} /> End
          </button>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', fontSize: '0.85rem' }}>
          <span style={{ color: 'var(--text-faint)' }}>
            Step: <strong style={{ color: 'var(--accent-cyan)' }}>{currentStepIndex + 1}</strong> of {maxSteps}
          </span>
          <span style={{ color: 'var(--text-faint)' }}>
            Total Cycles: <strong style={{ color: 'var(--text-main)' }}>{simulationData.cycles}</strong>
          </span>
          {simulationData.hitBreakpoint && (
            <span style={{ color: '#ef4444', display: 'inline-flex', alignItems: 'center', gap: '0.3rem', fontWeight: 600 }}>
              <CircleDot size={14} /> Paused at Breakpoint PC {simulationData.breakpointPC}
            </span>
          )}
          {simulationData.warning && (
            <span style={{ color: 'var(--accent-amber)', display: 'inline-flex', alignItems: 'center', gap: '0.3rem' }}>
              <AlertTriangle size={14} /> {simulationData.warning}
            </span>
          )}
        </div>
      </div>

      {/* Simulator Layout */}
      <div className="sim-grid">
        {/* Assembly with PC pointer and clickable breakpoints */}
        <div className="sim-code-view">
          <div style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--text-faint)', fontSize: '0.75rem', textTransform: 'uppercase', marginBottom: '0.5rem', fontWeight: 600 }}>
            <span>Instruction Stream (PC Highlight)</span>
            <span>Click gutter to toggle BP</span>
          </div>

          <div style={{ maxHeight: '420px', overflowY: 'auto' }}>
            {instructions.map((instr, idx) => {
              const isCurrent = idx === currentPc;
              const hasBp = breakpoints.includes(idx);

              return (
                <div
                  key={idx}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    padding: '3px 6px',
                    borderRadius: '4px',
                    background: isCurrent ? 'rgba(56, 189, 248, 0.18)' : 'transparent',
                    borderLeft: isCurrent ? '3px solid var(--accent-cyan)' : '3px solid transparent',
                  }}
                >
                  {/* Breakpoint toggle button */}
                  <span
                    onClick={() => onToggleBreakpoint && onToggleBreakpoint(idx)}
                    style={{
                      width: '20px',
                      cursor: 'pointer',
                      textAlign: 'center',
                      color: hasBp ? '#ef4444' : 'rgba(255,255,255,0.15)',
                      userSelect: 'none',
                    }}
                    title={hasBp ? 'Remove Breakpoint' : 'Set Breakpoint'}
                  >
                    {hasBp ? '●' : '○'}
                  </span>

                  <span style={{ width: '30px', color: isCurrent ? 'var(--accent-cyan)' : 'var(--text-faint)', fontSize: '0.75rem' }}>
                    {isCurrent ? '▶' : ''}{idx}
                  </span>

                  <span
                    style={{
                      color: isCurrent ? '#ffffff' : '#cbd5e1',
                      fontWeight: isCurrent ? 'bold' : 'normal',
                      fontFamily: 'var(--code-font)',
                    }}
                  >
                    {instr.text}
                  </span>
                </div>
              );
            })}
          </div>
        </div>

        {/* State: Condition Flags, Registers, Memory, Console */}
        <div className="sim-state-panel">
          {/* Condition Flags */}
          <div style={{ background: 'var(--bg-panel)', border: '1px solid var(--border-subtle)', borderRadius: 'var(--radius-md)', padding: '0.75rem' }}>
            <div style={{ color: 'var(--text-faint)', fontSize: '0.75rem', textTransform: 'uppercase', marginBottom: '0.5rem', fontWeight: 600 }}>
              CPU Condition Flags
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '0.4rem' }}>
              <div className="reg-box" style={{ background: flags.zero ? 'rgba(56, 189, 248, 0.2)' : undefined, borderColor: flags.zero ? 'var(--accent-cyan)' : undefined }}>
                <div className="reg-name">ZERO (Z)</div>
                <div className="reg-val" style={{ color: flags.zero ? 'var(--accent-cyan)' : 'var(--text-faint)', fontSize: '0.8rem' }}>
                  {flags.zero ? '1 (SET)' : '0'}
                </div>
              </div>
              <div className="reg-box" style={{ background: flags.sign ? 'rgba(244, 63, 94, 0.2)' : undefined, borderColor: flags.sign ? 'var(--accent-rose)' : undefined }}>
                <div className="reg-name">SIGN (S)</div>
                <div className="reg-val" style={{ color: flags.sign ? 'var(--accent-rose)' : 'var(--text-faint)', fontSize: '0.8rem' }}>
                  {flags.sign ? '1 (NEG)' : '0'}
                </div>
              </div>
              <div className="reg-box" style={{ background: flags.greater ? 'rgba(16, 185, 129, 0.2)' : undefined, borderColor: flags.greater ? 'var(--accent-emerald)' : undefined }}>
                <div className="reg-name">GREATER</div>
                <div className="reg-val" style={{ color: flags.greater ? 'var(--accent-emerald)' : 'var(--text-faint)', fontSize: '0.8rem' }}>
                  {flags.greater ? '1 (GT)' : '0'}
                </div>
              </div>
              <div className="reg-box" style={{ background: flags.less ? 'rgba(245, 158, 11, 0.2)' : undefined, borderColor: flags.less ? 'var(--accent-amber)' : undefined }}>
                <div className="reg-name">LESS</div>
                <div className="reg-val" style={{ color: flags.less ? 'var(--accent-amber)' : 'var(--text-faint)', fontSize: '0.8rem' }}>
                  {flags.less ? '1 (LT)' : '0'}
                </div>
              </div>
            </div>
          </div>

          {/* Registers */}
          <div style={{ background: 'var(--bg-panel)', border: '1px solid var(--border-subtle)', borderRadius: 'var(--radius-md)', padding: '0.75rem' }}>
            <div style={{ color: 'var(--text-faint)', fontSize: '0.75rem', textTransform: 'uppercase', marginBottom: '0.6rem', fontWeight: 600 }}>
              CPU Registers (R0 - R7)
            </div>
            <div className="registers-grid">
              {Array.from({ length: 8 }).map((_, i) => {
                const rName = `R${i}`;
                const val = registers[rName] !== undefined ? registers[rName] : 0;
                return (
                  <div key={rName} className="reg-box">
                    <div className="reg-name">{rName}</div>
                    <div className="reg-val" style={{ color: val !== 0 ? 'var(--accent-cyan)' : 'var(--text-faint)' }}>
                      {String(val)}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Memory */}
          <div style={{ background: 'var(--bg-panel)', border: '1px solid var(--border-subtle)', borderRadius: 'var(--radius-md)', padding: '0.75rem' }}>
            <div style={{ color: 'var(--text-faint)', fontSize: '0.75rem', textTransform: 'uppercase', marginBottom: '0.6rem', fontWeight: 600 }}>
              Variable Memory State
            </div>
            {Object.keys(memory).length === 0 ? (
              <div style={{ color: 'var(--text-faint)', fontSize: '0.8rem', fontStyle: 'italic' }}>
                No variables written to memory yet.
              </div>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.35rem', maxHeight: '100px', overflowY: 'auto' }}>
                {Object.entries(memory).map(([k, v]) => (
                  <div key={k} style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', fontFamily: 'var(--code-font)' }}>
                    <span style={{ color: 'var(--accent-amber)' }}>{k}:</span>
                    <span style={{ color: '#86efac', fontWeight: 600 }}>{String(v)}</span>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Console Standard Output */}
          <div style={{ background: 'var(--bg-panel)', border: '1px solid var(--border-subtle)', borderRadius: 'var(--radius-md)', padding: '0.75rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', color: 'var(--text-faint)', fontSize: '0.75rem', textTransform: 'uppercase', marginBottom: '0.6rem', fontWeight: 600 }}>
              <Terminal size={13} />
              <span>Program Console Output</span>
            </div>
            <div style={{ background: '#080c14', borderRadius: 'var(--radius-sm)', padding: '0.5rem', minHeight: '60px', maxHeight: '100px', overflowY: 'auto', fontFamily: 'var(--code-font)', fontSize: '0.825rem', color: '#38bdf8' }}>
              {output.length === 0 ? (
                <span style={{ color: 'var(--text-faint)', fontStyle: 'italic' }}>[No output generated]</span>
              ) : (
                output.map((line, idx) => (
                  <div key={idx}>&gt; {line}</div>
                ))
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
