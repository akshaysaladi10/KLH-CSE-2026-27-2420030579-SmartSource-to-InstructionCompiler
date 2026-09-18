import React, { useRef, useEffect } from 'react';
import { Terminal, FileCode, Layers } from 'lucide-react';

export default function Editor({
  code,
  onChange,
  onCompile,
  highlightLine,
  errors = [],
}) {
  const textareaRef = useRef(null);
  const gutterRef = useRef(null);

  const lines = code.split('\n');
  const lineCount = Math.max(lines.length, 1);

  // Sync scrolling between textarea and line number gutter
  const handleScroll = () => {
    if (textareaRef.current && gutterRef.current) {
      gutterRef.current.scrollTop = textareaRef.current.scrollTop;
    }
  };

  // Handle Tab key and Ctrl+Enter shortcut
  const handleKeyDown = (e) => {
    if (e.key === 'Tab') {
      e.preventDefault();
      const start = e.target.selectionStart;
      const end = e.target.selectionEnd;
      const val = e.target.value;
      const newVal = val.substring(0, start) + '    ' + val.substring(end);
      onChange(newVal);
      setTimeout(() => {
        if (textareaRef.current) {
          textareaRef.current.selectionStart = textareaRef.current.selectionEnd = start + 4;
        }
      }, 0);
    } else if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      e.preventDefault();
      onCompile();
    }
  };

  // Set of lines containing errors
  const errorLines = new Set(errors.map((err) => err.line));

  return (
    <div className="editor-pane">
      <div className="editor-toolbar">
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
          <FileCode size={16} color="var(--accent-cyan)" />
          <span>Source Code Editor</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-faint)' }}>
            {lines.length} lines | {code.length} chars
          </span>
          <span style={{ fontSize: '0.72rem', background: 'rgba(255,255,255,0.06)', padding: '0.15rem 0.45rem', borderRadius: '4px' }}>
            Ctrl+Enter to Compile
          </span>
        </div>
      </div>

      <div className="editor-content-area">
        <div className="editor-gutter" ref={gutterRef}>
          {Array.from({ length: lineCount }).map((_, i) => {
            const lineNo = i + 1;
            const hasError = errorLines.has(lineNo);
            const isHighlighted = highlightLine === lineNo;

            return (
              <div
                key={i}
                style={{
                  color: hasError
                    ? 'var(--accent-rose)'
                    : isHighlighted
                    ? 'var(--accent-cyan)'
                    : 'inherit',
                  fontWeight: hasError || isHighlighted ? 'bold' : 'normal',
                  background: isHighlighted ? 'rgba(56, 189, 248, 0.15)' : 'transparent',
                }}
                title={hasError ? `Error on line ${lineNo}` : undefined}
              >
                {hasError ? '● ' : ''}
                {lineNo}
              </div>
            );
          })}
        </div>

        <textarea
          ref={textareaRef}
          className="editor-textarea"
          value={code}
          onChange={(e) => onChange(e.target.value)}
          onScroll={handleScroll}
          onKeyDown={handleKeyDown}
          placeholder="// Enter high-level language code here..."
          spellCheck="false"
        />
      </div>
    </div>
  );
}
