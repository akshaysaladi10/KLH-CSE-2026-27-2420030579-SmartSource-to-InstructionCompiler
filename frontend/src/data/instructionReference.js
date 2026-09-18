export const INSTRUCTION_SET_REFERENCE = [
  {
    opcode: 'LOAD',
    syntax: 'LOAD R_dest, src',
    purpose: 'Loads a constant literal or memory variable into a designated target register.',
    example: 'LOAD R0, 10\nLOAD R1, count',
    category: 'Data Transfer'
  },
  {
    opcode: 'STORE',
    syntax: 'STORE mem_var, R_src',
    purpose: 'Stores the contents of a source register into a variable slot in memory.',
    example: 'STORE sum, R0',
    category: 'Data Transfer'
  },
  {
    opcode: 'MOV',
    syntax: 'MOV R_dest, R_src_or_val',
    purpose: 'Copies a value or register directly into another register without memory access.',
    example: 'MOV R2, R0',
    category: 'Data Transfer'
  },
  {
    opcode: 'ADD',
    syntax: 'ADD R_dest, operand',
    purpose: 'Adds operand value or register to R_dest. For strings, performs concatenation.',
    example: 'ADD R0, R1\nADD R0, 5',
    category: 'Arithmetic'
  },
  {
    opcode: 'SUB',
    syntax: 'SUB R_dest, operand',
    purpose: 'Subtracts operand value or register from R_dest and stores result in R_dest.',
    example: 'SUB R0, 1',
    category: 'Arithmetic'
  },
  {
    opcode: 'MUL',
    syntax: 'MUL R_dest, operand',
    purpose: 'Multiplies R_dest by operand and stores product in R_dest.',
    example: 'MUL R0, R1',
    category: 'Arithmetic'
  },
  {
    opcode: 'DIV',
    syntax: 'DIV R_dest, operand',
    purpose: 'Divides R_dest by operand (integer or floating-point division based on types).',
    example: 'DIV R0, 2',
    category: 'Arithmetic'
  },
  {
    opcode: 'MOD',
    syntax: 'MOD R_dest, operand',
    purpose: 'Computes remainder of R_dest divided by operand.',
    example: 'MOD R0, 2',
    category: 'Arithmetic'
  },
  {
    opcode: 'CMP',
    syntax: 'CMP R_left, operand_right',
    purpose: 'Compares two values and sets condition flags: Zero (Z), Sign (S), Greater (GT), Less (LT).',
    example: 'CMP R0, 10',
    category: 'Comparison'
  },
  {
    opcode: 'SETEQ',
    syntax: 'SETEQ R_dest',
    purpose: 'Sets register R_dest to 1 if Zero flag is set (operands were equal), else 0.',
    example: 'SETEQ R0',
    category: 'Comparison'
  },
  {
    opcode: 'SETNE',
    syntax: 'SETNE R_dest',
    purpose: 'Sets register R_dest to 1 if Zero flag is cleared (operands were not equal), else 0.',
    example: 'SETNE R0',
    category: 'Comparison'
  },
  {
    opcode: 'SETLT',
    syntax: 'SETLT R_dest',
    purpose: 'Sets register R_dest to 1 if Less flag is set (left < right), else 0.',
    example: 'SETLT R0',
    category: 'Comparison'
  },
  {
    opcode: 'SETGT',
    syntax: 'SETGT R_dest',
    purpose: 'Sets register R_dest to 1 if Greater flag is set (left > right), else 0.',
    example: 'SETGT R0',
    category: 'Comparison'
  },
  {
    opcode: 'JMP',
    syntax: 'JMP label',
    purpose: 'Unconditional jump: sets program counter (PC) to target label.',
    example: 'JMP L_loop_start',
    category: 'Control Flow'
  },
  {
    opcode: 'JZ / JE',
    syntax: 'JZ label',
    purpose: 'Conditional jump if Zero flag is set (or condition evaluates to false / 0).',
    example: 'JZ L_exit',
    category: 'Control Flow'
  },
  {
    opcode: 'JNZ / JNE',
    syntax: 'JNZ label',
    purpose: 'Conditional jump if Zero flag is cleared (condition evaluates to true / non-zero).',
    example: 'JNZ L_continue',
    category: 'Control Flow'
  },
  {
    opcode: 'JL',
    syntax: 'JL label',
    purpose: 'Conditional jump if Less flag is set.',
    example: 'JL L_less_target',
    category: 'Control Flow'
  },
  {
    opcode: 'JG',
    syntax: 'JG label',
    purpose: 'Conditional jump if Greater flag is set.',
    example: 'JG L_greater_target',
    category: 'Control Flow'
  },
  {
    opcode: 'PRINT',
    syntax: 'PRINT R_src_or_val',
    purpose: 'Outputs the operand or register contents to the virtual machine standard console.',
    example: 'PRINT R0',
    category: 'I/O'
  },
  {
    opcode: 'HALT',
    syntax: 'HALT',
    purpose: 'Terminates program execution in the target virtual machine.',
    example: 'HALT',
    category: 'Control Flow'
  }
];
