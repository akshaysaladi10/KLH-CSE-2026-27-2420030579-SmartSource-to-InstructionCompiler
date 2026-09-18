from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator


class CompileRequest(BaseModel):
    source: str = Field(..., description="High-level source code to compile")
    enabledPasses: Optional[List[str]] = Field(
        default=None,
        description="List of enabled optimization passes (constant_folding, constant_propagation, algebraic_simplification, dead_code_elimination)",
    )

    @field_validator("source")
    def validate_source_length(cls, v: str) -> str:
        if len(v) > 100_000:
            raise ValueError("Source code size exceeds maximum allowable limit (100,000 characters).")
        return v


class CompileResponse(BaseModel):
    success: bool
    statistics: Dict[str, Any]
    timings: Optional[Dict[str, float]] = None
    stageStatus: Optional[Dict[str, str]] = None
    tokens: List[Dict[str, Any]]
    ast: Optional[Dict[str, Any]] = None
    symbolTable: List[Dict[str, Any]]
    tac: List[Dict[str, Any]]
    optimizedTac: List[Dict[str, Any]]
    optimizations: List[Dict[str, Any]]
    instructions: List[Dict[str, Any]]
    traceMatrix: List[Dict[str, Any]]
    errors: List[Dict[str, Any]]


class SimulateRequest(BaseModel):
    instructions: List[Dict[str, Any]] = Field(..., description="Target assembly instructions to execute")
    breakpoints: Optional[List[int]] = Field(default=None, description="Instruction indexes to break on")
    maxCycles: Optional[int] = Field(default=10000, description="Max cycles for safety")


class SimulateResponse(BaseModel):
    success: bool
    cycles: int
    warning: Optional[str] = None
    hitBreakpoint: Optional[bool] = False
    breakpointPC: Optional[int] = None
    output: List[str]
    registers: Dict[str, Any]
    memory: Dict[str, Any]
    flags: Optional[Dict[str, bool]] = None
    stepHistory: List[Dict[str, Any]]


class SampleProgram(BaseModel):
    id: str
    title: str
    category: str
    description: str
    code: str
