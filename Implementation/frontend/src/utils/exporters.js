export function downloadFile(content, fileName, contentType) {
  const blob = new Blob([content], { type: contentType });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = fileName;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

export function exportTokensCSV(tokens = []) {
  const headers = ['Index', 'Token', 'Lexeme', 'Type', 'Line', 'Column'];
  const rows = tokens.map((t, i) => [
    i + 1,
    `"${t.token || ''}"`,
    `"${(t.lexeme || '').replace(/"/g, '""')}"`,
    `"${t.type || ''}"`,
    t.line || 1,
    t.column || 1,
  ]);
  const csvContent = [headers.join(','), ...rows.map(r => r.join(','))].join('\n');
  downloadFile(csvContent, 'compiler_tokens.csv', 'text/csv;charset=utf-8;');
}

export function exportASTJSON(ast) {
  const content = JSON.stringify(ast || {}, null, 2);
  downloadFile(content, 'abstract_syntax_tree.json', 'application/json');
}

export function exportTACText(tac = [], optimizedTac = []) {
  let content = '=== THREE-ADDRESS CODE (TAC) ===\n\n';
  content += '--- Raw Intermediate Representation ---\n';
  tac.forEach((t, i) => {
    content += `${String(i).padStart(3, ' ')}: ${t.text} (line ${t.line})\n`;
  });
  content += '\n--- Optimized Intermediate Representation ---\n';
  optimizedTac.forEach((t, i) => {
    content += `${String(i).padStart(3, ' ')}: ${t.text} (line ${t.line})\n`;
  });
  downloadFile(content, 'intermediate_tac.txt', 'text/plain;charset=utf-8;');
}

export function exportAssemblyText(instructions = []) {
  let content = '; ====================================================\n';
  content += '; Smart Source-to-Instruction Compiler Pseudo-Assembly\n';
  content += '; ====================================================\n\n';
  instructions.forEach((i, idx) => {
    content += `${String(idx).padStart(3, ' ')}: ${i.text}\n`;
  });
  downloadFile(content, 'target_instructions.asm', 'text/plain;charset=utf-8;');
}

export function exportFullReportJSON(compilationResult, sourceCode) {
  const report = {
    generatedAt: new Date().toISOString(),
    sourceCode,
    statistics: compilationResult.statistics,
    timings: compilationResult.timings,
    stageStatus: compilationResult.stageStatus,
    tokensCount: compilationResult.tokens?.length || 0,
    ast: compilationResult.ast,
    symbolTable: compilationResult.symbolTable,
    tac: compilationResult.tac,
    optimizedTac: compilationResult.optimizedTac,
    optimizations: compilationResult.optimizations,
    instructions: compilationResult.instructions,
    errors: compilationResult.errors,
  };
  downloadFile(JSON.stringify(report, null, 2), 'compilation_full_report.json', 'application/json');
}
