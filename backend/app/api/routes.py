from fastapi import APIRouter, HTTPException
from typing import List

from .schemas import (
    CompileRequest,
    CompileResponse,
    SimulateRequest,
    SimulateResponse,
    SampleProgram,
)
from ..compiler.pipeline import CompilerPipeline
from ..compiler.target import TargetInstruction, TargetVMSimulator

router = APIRouter(prefix="/api")

pipeline = CompilerPipeline()

SAMPLE_PROGRAMS: List[SampleProgram] = [
    SampleProgram(
        id="arithmetic",
        title="1. Arithmetic Basics",
        category="Basic",
        description="Simple variable declarations, assignment, and addition.",
        code="""// Example 1: Arithmetic Basics
int a = 10;
int b = 20;
int c;
c = a + b;
print c;
"""
    ),
    SampleProgram(
        id="expression",
        title="2. Expression & Precedence",
        category="Expressions",
        description="Complex expression demonstrating arithmetic operator precedence (* before +).",
        code="""// Example 2: Operator Precedence
int a = 10;
int b = 20;
int c;
c = a + b * 2;
print c;
"""
    ),
    SampleProgram(
        id="conditional",
        title="3. Conditional Branching",
        category="Control Flow",
        description="If-else statement comparing variables and branching execution.",
        code="""// Example 3: Conditional Branching
int a = 15;
int b = 20;
int c;
if (a > b) {
    c = a;
} else {
    c = b;
}
print c;
"""
    ),
    SampleProgram(
        id="loop",
        title="4. While Loop Accumulator",
        category="Control Flow",
        description="While loop computing sum of numbers from 0 to 9.",
        code="""// Example 4: While Loop Accumulator
int i = 0;
int sum = 0;
while (i < 10) {
    sum = sum + i;
    i = i + 1;
}
print sum;
"""
    ),
    SampleProgram(
        id="optimization",
        title="5. Optimization Showcase",
        category="Optimization",
        description="Demonstrates Constant Folding (10+20), Constant Propagation, Algebraic Simplification (y+0, z*1), and Dead Code Elimination.",
        code="""// Example 5: Compiler Optimization Showcase
int x = 10 + 20;
int y = x + 0;
int z = y * 1;
int unused = 999;
int result = z * 2;
print result;
"""
    ),
    SampleProgram(
        id="factorial",
        title="6. Factorial Algorithm",
        category="Algorithms",
        description="Calculates 5! (factorial of 5) using an iterative while loop.",
        code="""// Example 6: Factorial of 5 (5! = 120)
int n = 5;
int fact = 1;
while (n > 1) {
    fact = fact * n;
    n = n - 1;
}
print fact;
"""
    ),
    SampleProgram(
        id="for_loop",
        title="7. For Loop Iteration",
        category="Control Flow",
        description="For loop iterating from 1 to 5 to compute product.",
        code="""// Example 7: For Loop Iteration
int prod = 1;
for (int i = 1; i <= 5; i = i + 1) {
    prod = prod * i;
}
print prod;
"""
    ),
    SampleProgram(
        id="fibonacci",
        title="8. Fibonacci Sequence",
        category="Algorithms",
        description="Computes the 7th Fibonacci number iteratively.",
        code="""// Example 8: 7th Fibonacci Number
int n = 7;
int a = 0;
int b = 1;
int i = 2;
while (i <= n) {
    int next = a + b;
    a = b;
    b = next;
    i = i + 1;
}
print b;
"""
    ),
]


@router.post("/compile", response_model=CompileResponse)
def compile_source(request: CompileRequest):
    try:
        result = pipeline.compile(
            request.source,
            enabled_passes=request.enabledPasses,
        )
        return CompileResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Compiler pipeline error: {str(e)}")


@router.post("/simulate", response_model=SimulateResponse)
def simulate_instructions(request: SimulateRequest):
    try:
        target_objs: List[TargetInstruction] = []
        for idx, d in enumerate(request.instructions):
            target_objs.append(
                TargetInstruction(
                    op=d.get("op", ""),
                    arg1=d.get("arg1"),
                    arg2=d.get("arg2"),
                    comment=d.get("comment"),
                    source_line=d.get("sourceLine", 1),
                    instruction_id=d.get("instructionId", idx),
                )
            )

        sim = TargetVMSimulator(max_cycles=request.maxCycles or 10000)
        sim_result = sim.run(target_objs, breakpoints=request.breakpoints)
        return SimulateResponse(**sim_result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Simulation error: {str(e)}")


@router.get("/examples", response_model=List[SampleProgram])
def get_examples():
    return SAMPLE_PROGRAMS


@router.get("/health")
def health_check():
    return {"status": "healthy", "service": "Smart Source-to-Instruction Compiler"}
