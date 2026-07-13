import ast
import math

# Supported mathematical functions
FUNCTIONS = {
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log,
    "exp": math.exp,
    "abs": abs,
    "round": round,
}

# Supported operators
OPERATORS = {
    ast.Add: lambda x, y: x + y,
    ast.Sub: lambda x, y: x - y,
    ast.Mult: lambda x, y: x * y,
    ast.Div: lambda x, y: x / y,
    ast.Pow: lambda x, y: x ** y,
    ast.Mod: lambda x, y: x % y,
    ast.USub: lambda x: -x,
}


def calculator(expression: str):
    """
    Safely evaluate a mathematical expression.
    Example:
        calculator("2 + 3 * 4")
        calculator("sqrt(25)")
    """
    try:
        tree = ast.parse(expression, mode="eval")
        result = _evaluate(tree.body)
        return str(result)
    except Exception as e:
        return f"Calculator Error: {e}"


def _evaluate(node):
    # Numbers
    if isinstance(node, ast.Constant):
        return node.value

    # Binary operations (+, -, *, /, %, **)
    elif isinstance(node, ast.BinOp):
        operator = type(node.op)

        if operator not in OPERATORS:
            raise ValueError("Unsupported operator")

        return OPERATORS[operator](
            _evaluate(node.left),
            _evaluate(node.right)
        )

    # Unary operations (-5)
    elif isinstance(node, ast.UnaryOp):
        operator = type(node.op)

        if operator not in OPERATORS:
            raise ValueError("Unsupported unary operator")

        return OPERATORS[operator](
            _evaluate(node.operand)
        )

    # Function calls (sqrt(), sin(), etc.)
    elif isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Invalid function")

        func_name = node.func.id

        if func_name not in FUNCTIONS:
            raise ValueError(f"Unsupported function: {func_name}")

        args = [_evaluate(arg) for arg in node.args]
        return FUNCTIONS[func_name](*args)

    raise ValueError(f"Unsupported expression: {ast.dump(node)}")

if __name__ == "__main__":
    print(calculator("25*18"))
    print(calculator("sqrt(25)"))  # Output: 5.0