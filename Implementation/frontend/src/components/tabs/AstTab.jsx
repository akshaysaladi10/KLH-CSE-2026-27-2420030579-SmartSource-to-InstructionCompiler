import React, { useState } from 'react';
import { ChevronRight, ChevronDown, FolderTree, Eye, EyeOff } from 'lucide-react';

function TreeNode({ node, depth = 0, onSelectLine }) {
  const [collapsed, setCollapsed] = useState(false);
  const hasChildren = node.children && node.children.length > 0;

  const nodeColor = () => {
    switch (node.type) {
      case 'Program': return '#a855f7';
      case 'VarDecl': return '#38bdf8';
      case 'Assignment': return '#3b82f6';
      case 'BinaryExpr': return '#f59e0b';
      case 'UnaryExpr': return '#fb7185';
      case 'LiteralExpr': return '#10b981';
      case 'VariableExpr': return '#60a5fa';
      case 'IfStmt': return '#ec4899';
      case 'WhileStmt': return '#8b5cf6';
      case 'PrintStmt': return '#14b8a6';
      default: return '#94a3b8';
    }
  };

  return (
    <div className="ast-node">
      <div
        className="ast-node-header"
        onClick={() => {
          if (hasChildren) setCollapsed(!collapsed);
          if (node.line && onSelectLine) onSelectLine(node.line);
        }}
      >
        {hasChildren && (
          <span style={{ color: 'var(--text-faint)', display: 'inline-flex' }}>
            {collapsed ? <ChevronRight size={14} /> : <ChevronDown size={14} />}
          </span>
        )}

        <span
          className="ast-type-tag"
          style={{ color: nodeColor(), fontWeight: 600 }}
        >
          {node.type || 'Node'}
        </span>

        <span style={{ color: '#cbd5e1' }}>
          {node.label || node.name || node.value || ''}
        </span>

        {node.line && (
          <span style={{ fontSize: '0.7rem', color: 'var(--text-faint)', marginLeft: '0.4rem' }}>
            [L:{node.line}]
          </span>
        )}
      </div>

      {hasChildren && !collapsed && (
        <div style={{ display: 'flex', flexDirection: 'column' }}>
          {node.children.map((child, idx) => (
            <TreeNode
              key={idx}
              node={child}
              depth={depth + 1}
              onSelectLine={onSelectLine}
            />
          ))}
        </div>
      )}
    </div>
  );
}

export default function AstTab({ ast, onSelectLine }) {
  if (!ast) {
    return (
      <div style={{ color: 'var(--text-muted)', textAlign: 'center', padding: '2rem' }}>
        No Abstract Syntax Tree available. Click "Compile" to generate.
      </div>
    );
  }

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-muted)' }}>
          <FolderTree size={16} color="var(--accent-purple)" />
          <span style={{ fontSize: '0.9rem' }}>Interactive AST Visualizer</span>
        </div>
        <span style={{ fontSize: '0.8rem', color: 'var(--text-faint)' }}>
          Click nodes to expand/collapse and locate in editor
        </span>
      </div>

      <div className="ast-tree-container">
        <TreeNode node={ast} onSelectLine={onSelectLine} />
      </div>
    </div>
  );
}
