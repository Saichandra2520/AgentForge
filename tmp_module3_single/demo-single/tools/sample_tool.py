"""Example tool for the generated single-agent project."""

from __future__ import annotations

import ast
import operator as op

from langchain_core.tools import tool

_ALLOWED_OPERATORS: dict[type[ast.AST], object] = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.USub: op.neg,
    ast.UAdd: op.pos,
}


def _safe_eval(node: ast.AST) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)

    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPERATORS:
        left = _safe_eval(node.left)
        right = _safe_eval(node.right)
        return _ALLOWED_OPERATORS[type(node.op)](left, right)

    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_OPERATORS:
        operand = _safe_eval(node.operand)
        return _ALLOWED_OPERATORS[type(node.op)](operand)

    raise ValueError("Only arithmetic expressions are supported.")


@tool
def calculator(expression: str) -> str:
    """Evaluate a basic arithmetic expression."""
    try:
        parsed = ast.parse(expression, mode="eval")
        value = _safe_eval(parsed.body)
        if value.is_integer():
            return str(int(value))
        return str(value)
    except Exception as exc:  # pragma: no cover - defensive conversion for tool output
        return f"Calculation error: {exc}"