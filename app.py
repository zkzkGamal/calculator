from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field

import ast
import operator
import math

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
INDEX_HTML = STATIC_DIR / "index.html"

app = FastAPI(title="zkzk", version="1.0.0")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class CalculateRequest(BaseModel):
    expression: str = Field(..., min_length=1, max_length=500)


BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def evaluate_node(node):
    if isinstance(node, ast.Expression):
        return evaluate_node(node.body)

    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in BIN_OPS:
            raise ValueError(f"Unsupported operator: {op_type.__name__}")

        left = evaluate_node(node.left)
        right = evaluate_node(node.right)

        try:
            return BIN_OPS[op_type](left, right)
        except ZeroDivisionError as exc:
            raise ValueError("Division by zero") from exc
        except OverflowError as exc:
            raise ValueError("Result is too large") from exc

    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in UNARY_OPS:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

        return UNARY_OPS[op_type](evaluate_node(node.operand))

    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value

    raise ValueError(f"Unsupported expression element: {type(node).__name__}")


def safe_calculate(expression):
    expression = expression.strip()

    if not expression:
        raise ValueError("Expression is empty")

    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise ValueError("Invalid expression") from exc

    value = evaluate_node(tree)

    if isinstance(value, complex):
        raise ValueError("Complex numbers are not supported")

    if isinstance(value, float) and (math.isinf(value) or math.isnan(value)):
        raise ValueError("Result is not a finite number")

    return value


@app.get("/", response_class=FileResponse)
def index():
    return FileResponse(INDEX_HTML)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/calculate")
def calculate(payload: CalculateRequest):
    try:
        result = safe_calculate(payload.expression)
    except ValueError as exc:
        return JSONResponse(
            status_code=400,
            content={
                "error": str(exc),
                "result": None,
            },
        )

    if isinstance(result, float) and result.is_integer():
        result = int(result)

    return {
        "expression": payload.expression,
        "result": result,
    }
