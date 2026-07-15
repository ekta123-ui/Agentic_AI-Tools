import ast
import operator as op
import math

# Supported Operators
OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.USub: op.neg,
}

# Supported Functions
FUNCTIONS = {
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "abs": abs,
    "round": round,
}


def calculator(expression: str):
    """
    Evaluate a mathematical expression safely using AST.
    """
    try:
        tree = ast.parse(expression, mode="eval")
        result = _evaluate(tree.body)
        return str(result)

    except Exception as e:
        return f"Calculator Error: {e}"


def execute(arguments: dict):
    """
    Execute function used by the Tool Registry.
    """

    expression = arguments.get("expression")

    if not expression:
        return "Calculator Error: Expression not provided."

    return calculator(expression)


def _evaluate(node):

    if isinstance(node, ast.Constant):
        return node.value

    elif isinstance(node, ast.BinOp):
        return OPERATORS[type(node.op)](
            _evaluate(node.left),
            _evaluate(node.right),
        )

    elif isinstance(node, ast.UnaryOp):
        return OPERATORS[type(node.op)](
            _evaluate(node.operand)
        )

    elif isinstance(node, ast.Call):

        if not isinstance(node.func, ast.Name):
            raise ValueError("Invalid Function")

        func_name = node.func.id

        if func_name not in FUNCTIONS:
            raise ValueError(f"Unsupported function: {func_name}")

        args = [_evaluate(arg) for arg in node.args]

        return FUNCTIONS[func_name](*args)

    raise ValueError(f"Unsupported expression: {ast.dump(node)}")


if __name__ == "__main__":

    print("=" * 40)
    print("Calculator Tool Test")
    print("=" * 40)

    tests = [
        {"expression": "25*18"},
        {"expression": "(245+89)/2"},
        {"expression": "sqrt(625)"},
        {"expression": "2**10"},
        {"expression": "100%7"},
        {"expression": "abs(-45)"},
        {"expression": "round(12.567,2)"},
        {"expression": "sin(0)"},
        {"expression": "cos(0)"},
        {"expression": "tan(0)"},
    ]

    for i, test in enumerate(tests, start=1):
        print(f"\nTest {i}")
        print("Expression :", test["expression"])
        print("Result     :", execute(test))