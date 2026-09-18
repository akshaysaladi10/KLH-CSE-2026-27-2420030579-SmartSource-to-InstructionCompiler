import React, { useState } from 'react';
import { X, GraduationCap, ArrowRight } from 'lucide-react';
import { STAGE_EXPLAINERS } from '../data/stageExplainers';

export default function StageExplainerModal({ isOpen, onClose }) {
  const [selectedStage, setSelectedStage] = useState('lexer');

  if (!isOpen) return null;

  const current = STAGE_EXPLAINERS[selectedStage] || STAGE_EXPLAINERS.lexer;
  const stages = Object.keys(STAGE_EXPLAINERS);

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      background: 'rgba(0, 0, 0, 0.75)',
      backdropFilter: 'blur(6px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 100,
      padding: '1.5rem',
    }}>
      <div style={{
        background: 'var(--bg-panel)',
        border: '1px solid var(--border-subtle)',
        borderRadius: 'var(--radius-lg)',
        width: '100%',
        maxWidth: '850px',
        maxHeight: '85vh',
        display: 'flex',
        flexDirection: 'column',
        boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.5)',
        overflow: 'hidden',
      }}>
        {/* Header */}
        <div style={{
          padding: '1rem 1.5rem',
          borderBottom: '1px solid var(--border-subtle)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          background: 'rgba(15, 23, 42, 0.6)',
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            <GraduationCap size={18} color="var(--accent-purple)" />
            <h3 style={{ fontSize: '1.05rem', fontWeight: 600, color: 'var(--text-main)' }}>
              Compiler Pipeline Stage-by-Stage Educational Guide
            </h3>
          </div>
          <button
            onClick={onClose}
            style={{
              background: 'transparent',
              border: 'none',
              color: 'var(--text-muted)',
              cursor: 'pointer',
              padding: '4px',
              display: 'flex',
              borderRadius: '4px',
            }}
          >
            <X size={18} />
          </button>
        </div>

        {/* Stage Tabs */}
        <div style={{
          display: 'flex',
          overflowX: 'auto',
          background: 'rgba(0,0,0,0.25)',
          borderBottom: '1px solid var(--border-subtle)',
          padding: '0.4rem 1rem 0 1rem',
          gap: '0.3rem',
        }}>
          {stages.map((key) => {
            const isSel = selectedStage === key;
            return (
              <button
                key={key}
                onClick={() => setSelectedStage(key)}
                style={{
                  padding: '0.45rem 0.85rem',
                  border: 'none',
                  borderBottom: isSel ? '2px solid var(--accent-purple)' : '2px solid transparent',
                  background: isSel ? 'rgba(168, 85, 247, 0.12)' : 'transparent',
                  color: isSel ? '#c084fc' : 'var(--text-muted)',
                  fontSize: '0.8rem',
                  fontWeight: 600,
                  cursor: 'pointer',
                  borderRadius: '4px 4px 0 0',
                  textTransform: 'capitalize',
                  whiteSpace: 'nowrap',
                }}
              >
                {key}
              </button>
            );
          })}
        </div>

        {/* Stage Content */}
        <div style={{ padding: '1.5rem', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          <div>
            <h2 style={{ fontSize: '1.25rem', color: 'var(--text-main)', marginBottom: '0.4rem' }}>
              {current.title}
            </h2>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
            <div style={{ background: 'var(--bg-card)', padding: '1rem', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)' }}>
              <div style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--accent-cyan)', textTransform: 'uppercase', marginBottom: '0.35rem' }}>
                What It Does
              </div>
              <p style={{ fontSize: '0.85rem', color: '#cbd5e1', lineHeight: 1.5 }}>
                {current.what}
              </p>
            </div>

            <div style={{ background: 'var(--bg-card)', padding: '1rem', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)' }}>
              <div style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--accent-emerald)', textTransform: 'uppercase', marginBottom: '0.35rem' }}>
                Why It Exists
              </div>
              <p style={{ fontSize: '0.85rem', color: '#cbd5e1', lineHeight: 1.5 }}>
                {current.why}
              </p>
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
            <div style={{ background: 'var(--bg-card)', padding: '1rem', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)' }}>
              <div style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--accent-amber)', textTransform: 'uppercase', marginBottom: '0.35rem' }}>
                Input Data Representation
              </div>
              <p style={{ fontSize: '0.825rem', fontFamily: 'var(--code-font)', color: '#f8fafc', lineHeight: 1.5 }}>
                {current.input}
              </p>
            </div>

            <div style={{ background: 'var(--bg-card)', padding: '1rem', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)' }}>
              <div style={{ fontSize: '0.75rem', fontWeight: 600, color: '#ec4899', textTransform: 'uppercase', marginBottom: '0.35rem' }}>
                Output Data Representation
              </div>
              <p style={{ fontSize: '0.825rem', fontFamily: 'var(--code-font)', color: '#f8fafc', lineHeight: 1.5 }}>
                {current.output}
              </p>
            </div>
          </div>

          <div style={{ background: 'rgba(0,0,0,0.35)', padding: '1rem', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)' }}>
            <div style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-faint)', textTransform: 'uppercase', marginBottom: '0.4rem' }}>
              Concrete Example
            </div>
            <div style={{ fontSize: '0.85rem', fontFamily: 'var(--code-font)', color: '#93c5fd' }}>
              {current.example}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
