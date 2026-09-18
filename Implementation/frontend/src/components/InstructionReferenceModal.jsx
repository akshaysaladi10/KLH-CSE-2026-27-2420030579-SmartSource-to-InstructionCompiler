import React, { useState } from 'react';
import { X, Search, BookOpen } from 'lucide-react';
import { INSTRUCTION_SET_REFERENCE } from '../data/instructionReference';

export default function InstructionReferenceModal({ isOpen, onClose }) {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');

  if (!isOpen) return null;

  const categories = ['All', 'Data Transfer', 'Arithmetic', 'Comparison', 'Control Flow', 'I/O'];

  const filtered = INSTRUCTION_SET_REFERENCE.filter((item) => {
    const matchesSearch =
      item.opcode.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.purpose.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.syntax.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCat = selectedCategory === 'All' || item.category === selectedCategory;
    return matchesSearch && matchesCat;
  });

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
        {/* Modal Header */}
        <div style={{
          padding: '1rem 1.5rem',
          borderBottom: '1px solid var(--border-subtle)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          background: 'rgba(15, 23, 42, 0.6)',
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            <BookOpen size={18} color="var(--accent-cyan)" />
            <h3 style={{ fontSize: '1.05rem', fontWeight: 600, color: 'var(--text-main)' }}>
              Target Instruction Set Architecture (ISA) Reference
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

        {/* Filter Controls */}
        <div style={{
          padding: '1rem 1.5rem',
          borderBottom: '1px solid var(--border-subtle)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: '1rem',
          background: 'rgba(0, 0, 0, 0.2)',
        }}>
          <div style={{ position: 'relative', flex: 1 }}>
            <Search size={14} style={{ position: 'absolute', left: '10px', top: '10px', color: 'var(--text-faint)' }} />
            <input
              type="text"
              placeholder="Search instructions by opcode or purpose..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              style={{
                width: '100%',
                padding: '0.45rem 0.8rem 0.45rem 2rem',
                background: 'var(--bg-card)',
                border: '1px solid var(--border-subtle)',
                borderRadius: 'var(--radius-sm)',
                color: 'var(--text-main)',
                fontSize: '0.825rem',
                outline: 'none',
              }}
            />
          </div>

          <div style={{ display: 'flex', gap: '0.35rem' }}>
            {categories.map((cat) => (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                style={{
                  padding: '0.35rem 0.7rem',
                  borderRadius: 'var(--radius-sm)',
                  border: '1px solid',
                  borderColor: selectedCategory === cat ? 'var(--accent-cyan)' : 'var(--border-subtle)',
                  background: selectedCategory === cat ? 'rgba(56, 189, 248, 0.15)' : 'transparent',
                  color: selectedCategory === cat ? 'var(--accent-cyan)' : 'var(--text-muted)',
                  fontSize: '0.75rem',
                  cursor: 'pointer',
                  fontWeight: 500,
                }}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>

        {/* Content List */}
        <div style={{ padding: '1.25rem', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
          {filtered.map((item, idx) => (
            <div
              key={idx}
              style={{
                background: 'var(--bg-card)',
                border: '1px solid var(--border-subtle)',
                borderRadius: 'var(--radius-sm)',
                padding: '0.85rem 1.15rem',
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.35rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
                  <span style={{ fontWeight: 700, fontFamily: 'var(--code-font)', color: 'var(--accent-cyan)', fontSize: '0.95rem' }}>
                    {item.opcode}
                  </span>
                  <span style={{ fontFamily: 'var(--code-font)', color: 'var(--text-muted)', fontSize: '0.825rem' }}>
                    {item.syntax}
                  </span>
                </div>
                <span className="badge" style={{ background: 'rgba(255,255,255,0.06)', color: 'var(--text-faint)' }}>
                  {item.category}
                </span>
              </div>

              <div style={{ color: '#cbd5e1', fontSize: '0.85rem', marginBottom: '0.4rem' }}>
                {item.purpose}
              </div>

              <div style={{ background: 'rgba(0,0,0,0.3)', padding: '0.4rem 0.6rem', borderRadius: '4px', fontFamily: 'var(--code-font)', fontSize: '0.78rem', color: '#93c5fd', whiteSpace: 'pre-wrap' }}>
                {item.example}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
