# Target Instruction Set Architecture (ISA) Manual

This document details the educational 32-bit register-based virtual machine instruction set architecture used as the compilation target in the **Smart Source-to-Instruction Compiler**.

---

## 1. Machine Architecture Overview

The target machine is a deterministic, register-based educational CPU simulation.

### 1.1 Registers
The processor features eight general-purpose 32-bit registers:
- `R0`, `R1`, `R2`, `R3`, `R4`, `R5`, `R6`, `R7`

Convention:
- `R0` – `R5`: General computational registers, allocated deterministically by the register allocator.
- `R6` – `R7`: Spill / scratch registers used for memory transfers or complex compound operations.

### 1.2 Program Counter (PC)
The `PC` register holds the zero-based index of the instruction to be executed next. Execution starts at `PC = 0` and terminates when a `HALT` opcode is reached or cycle limit is exceeded.

### 1.3 Condition Flags
Arithmetic and comparison instructions update four hardware status flags:
- **`Z` (Zero Flag)**: Set to `true` if the result of an operation or `CMP` is equal to 0.
- **`S` (Sign / Negative Flag)**: Set to `true` if the result is negative (< 0).
- **`GT` (Greater Than Flag)**: Set to `true` if operand 1 > operand 2 in `CMP`.
- **`LT` (Less Than Flag)**: Set to `true` if operand 1 < operand 2 in `CMP`.

### 1.4 Memory
- Memory is organized as named memory cells corresponding to source variable identifiers and allocated spill locations.
- Variables retain their typed values (`int`, `float`, `bool`, `string`).

---

## 2. Complete Opcode Reference

| Opcode | Syntax | Semantics | Condition Flags Updated | Description |
|:---|:---|:---|:---|:---|
| **LOAD** | `LOAD Rd, [src]` | `Rd = Memory[src]` or literal constant | None | Loads a value from variable/literal into destination register `Rd`. |
| **STORE** | `STORE [dest], Rs` | `Memory[dest] = Rs` | None | Stores value from register `Rs` into memory variable `dest`. |
| **MOV** | `MOV Rd, Rs` | `Rd = Rs` | None | Copies contents of register `Rs` into register `Rd`. |
| **ADD** | `ADD Rd, Rs` | `Rd = Rd + Rs` | `Z`, `S` | Adds `Rs` to `Rd`, storing sum in `Rd`. |
| **SUB** | `SUB Rd, Rs` | `Rd = Rd - Rs` | `Z`, `S` | Subtracts `Rs` from `Rd`, storing difference in `Rd`. |
| **MUL** | `MUL Rd, Rs` | `Rd = Rd * Rs` | `Z`, `S` | Multiplies `Rd` by `Rs`, storing product in `Rd`. |
| **DIV** | `DIV Rd, Rs` | `Rd = Rd / Rs` | `Z`, `S` | Divides `Rd` by `Rs` (integer/float division). Traps on 0. |
| **MOD** | `MOD Rd, Rs` | `Rd = Rd % Rs` | `Z`, `S` | Computes remainder `Rd % Rs`. |
| **CMP** | `CMP R1, R2` | `diff = R1 - R2` | `Z`, `S`, `GT`, `LT` | Compares `R1` and `R2`, setting flags accordingly. |
| **SETEQ** | `SETEQ Rd` | `Rd = (Z == true) ? 1 : 0` | None | Sets `Rd` to 1 if Zero flag is set, 0 otherwise. |
| **SETNE** | `SETNE Rd` | `Rd = (Z == false) ? 1 : 0` | None | Sets `Rd` to 1 if Zero flag is clear, 0 otherwise. |
| **SETLT** | `SETLT Rd` | `Rd = (LT == true) ? 1 : 0` | None | Sets `Rd` to 1 if Less-Than flag is set, 0 otherwise. |
| **SETGT** | `SETGT Rd` | `Rd = (GT == true) ? 1 : 0` | None | Sets `Rd` to 1 if Greater-Than flag is set, 0 otherwise. |
| **JMP** | `JMP label` | `PC = Target(label)` | None | Unconditional jump to destination `label`. |
| **JZ** | `JZ label` | `if (Z) PC = Target(label)` | None | Jump to `label` if Zero flag is set (equal to 0). |
| **JNZ** | `JNZ label` | `if (!Z) PC = Target(label)` | None | Jump to `label` if Zero flag is clear (not equal to 0). |
| **JL** | `JL label` | `if (LT) PC = Target(label)` | None | Jump to `label` if Less-Than flag is set. |
| **JG** | `JG label` | `if (GT) PC = Target(label)` | None | Jump to `label` if Greater-Than flag is set. |
| **JLE** | `JLE label` | `if (LT \|\| Z) PC = Target(label)` | None | Jump to `label` if Less-Than or Equal. |
| **JGE** | `JGE label` | `if (GT \|\| Z) PC = Target(label)` | None | Jump to `label` if Greater-Than or Equal. |
| **PRINT** | `PRINT Rs` | `Console.append(Rs)` | None | Outputs value in register `Rs` or memory cell to console. |
| **HALT** | `HALT` | Terminates VM execution | None | Stops instruction fetch/decode cycle. |

---

## 3. Instruction Encoding and Representation

Each instruction in memory and transmission is represented as a structured object:
```json
{
  "instructionId": 14,
  "op": "ADD",
  "arg1": "R0",
  "arg2": "R1",
  "comment": "t0 = a + b",
  "sourceLine": 4,
  "tacId": 3,
  "text": "ADD R0, R1"
}
```

---

## 4. End-to-End Assembly Example

### Source Program
```c
int a = 10;
int b = 20;
int c = a + b;
print c;
```

### Generated Assembly
```assembly
 0: LOAD R0, 10
 1: STORE a, R0
 2: LOAD R1, 20
 3: STORE b, R1
 4: LOAD R0, a
 5: LOAD R1, b
 6: ADD R0, R1
 7: STORE c, R0
 8: PRINT c
 9: HALT
```

### Execution Trace
- Cycle 1: `R0 = 10`, `PC = 1`
- Cycle 2: `Memory['a'] = 10`, `PC = 2`
- Cycle 3: `R1 = 20`, `PC = 3`
- Cycle 4: `Memory['b'] = 20`, `PC = 4`
- Cycle 5: `R0 = 10`, `PC = 5`
- Cycle 6: `R1 = 20`, `PC = 6`
- Cycle 7: `R0 = 30`, Flags `{ Z: false, S: false, GT: true, LT: false }`, `PC = 7`
- Cycle 8: `Memory['c'] = 30`, `PC = 8`
- Cycle 9: `Console Output: "30"`, `PC = 9`
- Cycle 10: Machine halts successfully.
