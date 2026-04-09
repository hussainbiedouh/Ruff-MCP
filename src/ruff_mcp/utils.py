"""Utility functions for running ruff CLI."""
import subprocess
import os

RUFF_EXE = r"C:\Users\Hussain\.config\opencode\tools\ruff.exe"

def ruff_check(path: str, fix: bool = False, output_format: str = "text") -> str:
    """Run ruff check on files or directories."""
    cmd = [RUFF_EXE, "check", path]
    if fix:
        cmd.append("--fix")
    cmd.extend(["--output-format", output_format])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout + result.stderr

def ruff_format(path: str, check: bool = False, diff: bool = False) -> str:
    """Format Python code with ruff."""
    cmd = [RUFF_EXE, "format", path]
    if check:
        cmd.append("--check")
    if diff:
        cmd.append("--diff")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout + result.stderr

def ruff_fix(path: str, unsafe: bool = False) -> str:
    """Auto-fix linting issues with ruff."""
    cmd = [RUFF_EXE, "check", path, "--fix"]
    if unsafe:
        cmd.append("--unsafe-fixes")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout + result.stderr