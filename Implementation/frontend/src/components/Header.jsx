import React, { useState } from 'react';
import {
  Play,
  RotateCcw,
  Cpu,
  Download,
  History,
  BookOpen,
  HelpCircle,
  ChevronDown,
  Code2,
  FileSpreadsheet,
  FileCode,
  FileText,
  FileJson,
} from 'lucide-react';
import {
  exportTokensCSV,
  exportASTJSON,
  exportTACText,
  exportAssemblyText,
  exportFullReportJSON,
} from '../utils/exporters';

export default function Header({
  samples,
  selectedSample,
  onSelectSample,
  onCompile,
  onClear,
  onSimulate,
  compiling,
  compilationResult,
  sourceCode,
  historyCount = 0,
  onOpenHistory,
  onOpenIsaRef,
  onOpenExplainer,
}) {
  const [exportOpen, setExportOpen] = useState(false);
  const status = compilationResult?.statistics?.status;
  const hasErrors = compilationResult?.statistics?.hasErrors;
  const hasResult = !!compilationResult;

  const handleExport = (type) => {
    setExportOpen(false);
    if (!compilationResult) return;
    switch (type) {
      case 'tokens-csv':
        exportTokensCSV(compilationResult.tokens || []);
        break;
      case 'ast-json':
        exportASTJSON(compilationResult.ast);
        break;
      case 'tac-txt':
        exportTACText(compilationResult.tac || [], compilationResult.optimizedTac || []);
        break;
      case 'asm-txt':
        exportAssemblyText(compilationResult.instructions || []);
        break;
      case 'report-json':
        exportFullReportJSON(compilationResult, sourceCode);
        break;
      default:
        break;
    }
  };

  return (
    <header className="app-header">
      <div className="brand-section">
        <div className="brand-icon">
          <Code2 size={22} />
        </div>
        <div>
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <span className="brand-title">Smart Source-to-Instruction Compiler</span>
            <span className="brand-badge">Academic Edition</span>
          </div>
          <p style={{ fontSize: '0.72rem', color: 'var(--text-faint)' }}>
            Full Pipeline: Lexer &rarr; AST &rarr; Semantics &rarr; TAC &rarr; Optimizer &rarr; Target ISA &rarr; Traceability
          </p>
        </div>
      </div>

      <div className="header-controls">
        <select
          className="sample-select"
          value={selectedSample}
          onChange={(e) => onSelectSample(e.target.value)}
          title="Load built-in educational examples"
        >
          <option value="" disabled>Select Sample Program...</option>
          {samples.map((s) => (
            <option key={s.id} value={s.id}>
              {s.title} ({s.category})
            </option>
          ))}
        </select>

        <button
          className="btn btn-secondary"
          onClick={onClear}
          title="Clear editor code"
        >
          <RotateCcw size={15} />
          Clear
        </button>

        <button
          className="btn btn-primary"
          onClick={onCompile}
          disabled={compiling}
          title="Compile source program through all stages (Ctrl+Enter)"
        >
          <Play size={15} />
          {compiling ? 'Compiling...' : 'Compile'}
        </button>

        <button
          className="btn btn-success"
          onClick={onSimulate}
          disabled={compiling || !compilationResult?.instructions?.length || hasErrors}
          title="Step and execute target pseudo-assembly in VM"
        >
          <Cpu size={15} />
          Execute VM
        </button>

        {/* Real Export Dropdown */}
        <div className="dropdown-container">
          <button
            className="btn btn-secondary"
            onClick={() => setExportOpen(!exportOpen)}
            disabled={!hasResult}
            title="Export compilation artifacts (CSV, JSON, Assembly)"
          >
            <Download size={15} />
            Export
            <ChevronDown size={13} />
          </button>

          {exportOpen && (
            <div className="dropdown-menu">
              <button
                className="dropdown-item"
                onClick={() => handleExport('tokens-csv')}
              >
                <FileSpreadsheet size={14} style={{ color: '#38bdf8' }} />
                Tokens (CSV)
              </button>
              <button
                className="dropdown-item"
                onClick={() => handleExport('ast-json')}
              >
                <FileCode size={14} style={{ color: '#a855f7' }} />
                Abstract Syntax Tree (JSON)
              </button>
              <button
                className="dropdown-item"
                onClick={() => handleExport('tac-txt')}
              >
                <FileText size={14} style={{ color: '#f59e0b' }} />
                Intermediate Code TAC (TXT)
              </button>
              <button
                className="dropdown-item"
                onClick={() => handleExport('asm-txt')}
              >
                <FileCode size={14} style={{ color: '#10b981' }} />
                Target Assembly (ASM)
              </button>
              <div className="dropdown-divider" />
              <button
                className="dropdown-item"
                onClick={() => handleExport('report-json')}
              >
                <FileJson size={14} style={{ color: '#3b82f6' }} />
                Full Compilation Report (JSON)
              </button>
            </div>
          )}
        </div>

        {/* History Drawer Trigger */}
        <button
          className="btn btn-secondary"
          onClick={onOpenHistory}
          title="View compilation run history"
          style={{ position: 'relative' }}
        >
          <History size={15} />
          History
          {historyCount > 0 && (
            <span
              style={{
                marginLeft: '0.25rem',
                fontSize: '0.68rem',
                padding: '0.1rem 0.35rem',
                borderRadius: '9999px',
                background: 'rgba(56, 189, 248, 0.2)',
                color: '#38bdf8',
                fontWeight: 600,
              }}
            >
              {historyCount}
            </span>
          )}
        </button>

        {/* Target ISA Reference Modal Trigger */}
        <button
          className="btn btn-secondary"
          onClick={onOpenIsaRef}
          title="Browse 8-register pseudo-machine instruction set architecture (ISA)"
        >
          <BookOpen size={15} />
          ISA Ref
        </button>

        {/* Educational Stage Guide Modal Trigger */}
        <button
          className="btn btn-secondary"
          onClick={onOpenExplainer}
          title="Educational Guide: Learn what each compiler stage accomplishes"
        >
          <HelpCircle size={15} />
          Learn
        </button>
      </div>
    </header>
  );
}

