import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import Editor from './components/Editor';
import Dashboard from './components/Dashboard';
import TimingBar from './components/TimingBar';
import ErrorPanel from './components/ErrorPanel';
import HistoryDrawer from './components/HistoryDrawer';
import InstructionReferenceModal from './components/InstructionReferenceModal';
import StageExplainerModal from './components/StageExplainerModal';

import TokensTab from './components/tabs/TokensTab';
import AstTab from './components/tabs/AstTab';
import SymbolTableTab from './components/tabs/SymbolTableTab';
import TacTab from './components/tabs/TacTab';
import OptimizationTab from './components/tabs/OptimizationTab';
import AssemblyTab from './components/tabs/AssemblyTab';
import TraceTab from './components/tabs/TraceTab';
import SimulatorTab from './components/tabs/SimulatorTab';

import { SAMPLES } from './data/samples';
import {
  ListFilter,
  FolderTree,
  Database,
  Layers,
  Sparkles,
  Cpu,
  GitCommit,
  Terminal,
} from 'lucide-react';

export default function App() {
  const [samples, setSamples] = useState(SAMPLES);
  const [selectedSample, setSelectedSample] = useState('arithmetic');
  const [code, setCode] = useState(SAMPLES[0].code);

  const [compiling, setCompiling] = useState(false);
  const [compilationResult, setCompilationResult] = useState(null);
  const [simulationData, setSimulationData] = useState(null);

  const [activeTab, setActiveTab] = useState('trace');
  const [highlightLine, setHighlightLine] = useState(null);
  const [selectedInstruction, setSelectedInstruction] = useState(null);

  // Optimizer playground passes
  const [enabledPasses, setEnabledPasses] = useState([
    'constant_folding',
    'constant_propagation',
    'algebraic_simplification',
    'dead_code_elimination',
  ]);

  // Breakpoints in assembly (instruction indices)
  const [breakpoints, setBreakpoints] = useState([]);

  // Modals & Drawers state
  const [showHistory, setShowHistory] = useState(false);
  const [showIsaRef, setShowIsaRef] = useState(false);
  const [showExplainer, setShowExplainer] = useState(false);

  // Local storage compilation history
  const [history, setHistory] = useState(() => {
    try {
      const saved = localStorage.getItem('compiler_compilation_history');
      return saved ? JSON.parse(saved) : [];
    } catch (e) {
      return [];
    }
  });

  // Compile on first mount with initial sample
  useEffect(() => {
    handleCompile(SAMPLES[0].code, enabledPasses);
  }, []);

  const handleSelectSample = (sampleId) => {
    setSelectedSample(sampleId);
    const sample = samples.find((s) => s.id === sampleId);
    if (sample) {
      setCode(sample.code);
      setSimulationData(null);
      handleCompile(sample.code, enabledPasses);
    }
  };

  const handleCompile = async (codeToCompile = code, passesToUse = enabledPasses) => {
    setCompiling(true);
    setSimulationData(null);
    try {
      const res = await fetch('/api/compile', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          source: codeToCompile,
          enabledPasses: passesToUse,
        }),
      });
      const data = await res.json();
      setCompilationResult(data);

      // Record to local compilation history
      const historyItem = {
        id: Date.now(),
        timestamp: new Date().toLocaleTimeString(),
        source: codeToCompile,
        success: data.success,
        tokensCount: data.statistics?.tokensCount || 0,
        instructionsCount: data.statistics?.targetInstructionsCount || 0,
        optimizationsCount: data.statistics?.optimizationsCount || 0,
      };

      setHistory((prev) => {
        const updated = [historyItem, ...prev.slice(0, 24)];
        try {
          localStorage.setItem('compiler_compilation_history', JSON.stringify(updated));
        } catch (e) {}
        return updated;
      });
    } catch (err) {
      console.error('Failed to compile:', err);
    } finally {
      setCompiling(false);
    }
  };

  const handleTogglePass = (passKey) => {
    const next = enabledPasses.includes(passKey)
      ? enabledPasses.filter((p) => p !== passKey)
      : [...enabledPasses, passKey];
    setEnabledPasses(next);
    handleCompile(code, next);
  };

  const handleToggleBreakpoint = (instructionIdx) => {
    setBreakpoints((prev) =>
      prev.includes(instructionIdx)
        ? prev.filter((b) => b !== instructionIdx)
        : [...prev, instructionIdx]
    );
  };

  const handleSimulate = async (customBreakpoints = breakpoints) => {
    if (!compilationResult?.instructions?.length) return;

    try {
      const res = await fetch('/api/simulate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          instructions: compilationResult.instructions,
          breakpoints: customBreakpoints,
          maxCycles: 10000,
        }),
      });
      const data = await res.json();
      setSimulationData(data);
      setActiveTab('simulator');
    } catch (err) {
      console.error('Failed to simulate:', err);
    }
  };

  const handleClear = () => {
    setCode('');
    setSelectedSample('');
    setCompilationResult(null);
    setSimulationData(null);
    setHighlightLine(null);
    setSelectedInstruction(null);
    setBreakpoints([]);
  };

  const handleSelectLine = (line) => {
    setHighlightLine(line);
  };

  const handleSelectInstruction = (instr) => {
    setSelectedInstruction(instr);
    if (instr?.sourceLine) {
      setHighlightLine(instr.sourceLine);
    }
  };

  const handleLoadHistoryCode = (historyItem) => {
    setCode(historyItem.source);
    setShowHistory(false);
    handleCompile(historyItem.source, enabledPasses);
  };

  const handleClearHistory = () => {
    setHistory([]);
    try {
      localStorage.removeItem('compiler_compilation_history');
    } catch (e) {}
  };

  const stats = compilationResult?.statistics;

  return (
    <div className="app-container">
      <Header
        samples={samples}
        selectedSample={selectedSample}
        onSelectSample={handleSelectSample}
        onCompile={() => handleCompile(code, enabledPasses)}
        onClear={handleClear}
        onSimulate={() => handleSimulate(breakpoints)}
        compiling={compiling}
        compilationResult={compilationResult}
        sourceCode={code}
        historyCount={history.length}
        onOpenHistory={() => setShowHistory(true)}
        onOpenIsaRef={() => setShowIsaRef(true)}
        onOpenExplainer={() => setShowExplainer(true)}
      />

      {/* Stage Timings Bar */}
      {compilationResult?.timings && (
        <TimingBar
          timings={compilationResult.timings}
          totalMs={stats?.totalTimeMs || 0}
        />
      )}

      <div className="workspace-grid">
        {/* Left Side: Source Code Editor */}
        <Editor
          code={code}
          onChange={(newVal) => setCode(newVal)}
          onCompile={() => handleCompile(code, enabledPasses)}
          highlightLine={highlightLine}
          errors={compilationResult?.errors || []}
        />

        {/* Right Side: Compiler Pipeline Explorer */}
        <div className="pipeline-pane">
          <Dashboard statistics={stats} />

          {/* Error Diagnostics Panel */}
          {compilationResult?.errors && compilationResult.errors.length > 0 && (
            <div style={{ padding: '0.75rem 1.25rem 0' }}>
              <ErrorPanel
                errors={compilationResult.errors}
                onSelectLine={handleSelectLine}
              />
            </div>
          )}

          {/* Pipeline Stage Tabs Navigation */}
          <div className="tabs-nav">
            <button
              className={`tab-btn ${activeTab === 'tokens' ? 'active' : ''}`}
              onClick={() => setActiveTab('tokens')}
            >
              <ListFilter size={14} />
              <span>1. Tokens</span>
              {stats?.tokensCount > 0 && <span className="tab-count">{stats.tokensCount}</span>}
            </button>

            <button
              className={`tab-btn ${activeTab === 'ast' ? 'active' : ''}`}
              onClick={() => setActiveTab('ast')}
            >
              <FolderTree size={14} />
              <span>2. AST</span>
              {stats?.astNodesCount > 0 && <span className="tab-count">{stats.astNodesCount}</span>}
            </button>

            <button
              className={`tab-btn ${activeTab === 'symbols' ? 'active' : ''}`}
              onClick={() => setActiveTab('symbols')}
            >
              <Database size={14} />
              <span>3. Symbol Table</span>
              {stats?.symbolsCount > 0 && <span className="tab-count">{stats.symbolsCount}</span>}
            </button>

            <button
              className={`tab-btn ${activeTab === 'tac' ? 'active' : ''}`}
              onClick={() => setActiveTab('tac')}
            >
              <Layers size={14} />
              <span>4. Intermediate (TAC)</span>
              {stats?.tacInstructionsCount > 0 && (
                <span className="tab-count">{stats.tacInstructionsCount}</span>
              )}
            </button>

            <button
              className={`tab-btn ${activeTab === 'opt' ? 'active' : ''}`}
              onClick={() => setActiveTab('opt')}
            >
              <Sparkles size={14} />
              <span>5. Optimization</span>
              {stats?.optimizationsCount > 0 && (
                <span className="tab-count">{stats.optimizationsCount}</span>
              )}
            </button>

            <button
              className={`tab-btn ${activeTab === 'assembly' ? 'active' : ''}`}
              onClick={() => setActiveTab('assembly')}
            >
              <Cpu size={14} />
              <span>6. Target Assembly</span>
              {stats?.targetInstructionsCount > 0 && (
                <span className="tab-count">{stats.targetInstructionsCount}</span>
              )}
            </button>

            <button
              className={`tab-btn ${activeTab === 'trace' ? 'active' : ''}`}
              onClick={() => setActiveTab('trace')}
            >
              <GitCommit size={14} />
              <span>7. Trace Matrix</span>
              {compilationResult?.traceMatrix?.length > 0 && (
                <span className="tab-count">{compilationResult.traceMatrix.length}</span>
              )}
            </button>

            <button
              className={`tab-btn ${activeTab === 'simulator' ? 'active' : ''}`}
              onClick={() => setActiveTab('simulator')}
            >
              <Terminal size={14} />
              <span>8. VM Simulator</span>
              {simulationData && (
                <span className="tab-count" style={{ color: '#10b981' }}>Live</span>
              )}
            </button>
          </div>

          {/* Active Tab View */}
          <div className="tab-content">
            {activeTab === 'tokens' && (
              <TokensTab
                tokens={compilationResult?.tokens}
                onSelectLine={handleSelectLine}
              />
            )}

            {activeTab === 'ast' && (
              <AstTab
                ast={compilationResult?.ast}
                onSelectLine={handleSelectLine}
              />
            )}

            {activeTab === 'symbols' && (
              <SymbolTableTab
                symbolTable={compilationResult?.symbolTable}
                onSelectLine={handleSelectLine}
              />
            )}

            {activeTab === 'tac' && (
              <TacTab
                tac={compilationResult?.tac}
                onSelectLine={handleSelectLine}
              />
            )}

            {activeTab === 'opt' && (
              <OptimizationTab
                tac={compilationResult?.tac}
                optimizedTac={compilationResult?.optimizedTac}
                optimizations={compilationResult?.optimizations}
                enabledPasses={enabledPasses}
                onTogglePass={handleTogglePass}
                onReoptimize={() => handleCompile(code, enabledPasses)}
                onSelectLine={handleSelectLine}
              />
            )}

            {activeTab === 'assembly' && (
              <AssemblyTab
                instructions={compilationResult?.instructions}
                breakpoints={breakpoints}
                onToggleBreakpoint={handleToggleBreakpoint}
                onSelectLine={handleSelectLine}
                onSelectInstruction={handleSelectInstruction}
                selectedInstructionId={selectedInstruction?.instructionId}
              />
            )}

            {activeTab === 'trace' && (
              <TraceTab
                traceMatrix={compilationResult?.traceMatrix}
                onSelectLine={handleSelectLine}
                selectedLine={highlightLine}
              />
            )}

            {activeTab === 'simulator' && (
              <SimulatorTab
                simulationData={simulationData}
                instructions={compilationResult?.instructions}
                breakpoints={breakpoints}
                onToggleBreakpoint={handleToggleBreakpoint}
                onRunSimulate={() => handleSimulate(breakpoints)}
              />
            )}
          </div>
        </div>
      </div>

      {/* Interactive Modals & Drawers */}
      <HistoryDrawer
        isOpen={showHistory}
        onClose={() => setShowHistory(false)}
        history={history}
        onLoadCode={handleLoadHistoryCode}
        onClearHistory={handleClearHistory}
      />

      <InstructionReferenceModal
        isOpen={showIsaRef}
        onClose={() => setShowIsaRef(false)}
      />

      <StageExplainerModal
        isOpen={showExplainer}
        onClose={() => setShowExplainer(false)}
      />
    </div>
  );
}

