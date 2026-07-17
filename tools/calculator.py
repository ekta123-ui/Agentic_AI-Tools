import ast
import operator as op
import math
import re

# ==========================
# Supported Operators
# ==========================
OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.USub: op.neg,
}

# ==========================
# Supported Functions
# ==========================
FUNCTIONS = {
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "abs": abs,
    "round": round,
}


# ==========================
# Calculator Function
# ==========================
def calculator(expression: str):
    """
    Safely evaluate a mathematical expression using AST.
    """
    try:
        tree = ast.parse(expression, mode="eval")
        result = _evaluate(tree.body)
        return str(result)

    except Exception as e:
        return f"Calculator Error: {e}"


# ==========================
# Natural Language Converter
# ==========================
def convert_to_expression(text: str):

    text = text.lower().strip()

    # Remove punctuation
    text = text.replace("?", "")
    text = text.replace(",", "")

    # Remove common words
    remove_words = [
        "what is",
        "calculate",
        "please",
        "can you",
        "could you",
        "find",
        "tell me",
    ]

    for word in remove_words:
        text = text.replace(word, "")

    text = text.strip()

    # --------------------
    # Sum
    # --------------------
    match = re.search(r"sum of (\d+) and (\d+)", text)
    if match:
        return f"{match.group(1)}+{match.group(2)}"

    match = re.search(r"add (\d+) and (\d+)", text)
    if match:
        return f"{match.group(1)}+{match.group(2)}"

    match = re.search(r"(\d+)\s*plus\s*(\d+)", text)
    if match:
        return f"{match.group(1)}+{match.group(2)}"

    # --------------------
    # Subtraction
    # --------------------
    match = re.search(r"subtract (\d+) from (\d+)", text)
    if match:
        return f"{match.group(2)}-{match.group(1)}"

    match = re.search(r"(\d+)\s*minus\s*(\d+)", text)
    if match:
        return f"{match.group(1)}-{match.group(2)}"

    # --------------------
    # Multiplication
    # --------------------
    match = re.search(r"multiply (\d+) by (\d+)", text)
    if match:
        return f"{match.group(1)}*{match.group(2)}"

    match = re.search(r"product of (\d+) and (\d+)", text)
    if match:
        return f"{match.group(1)}*{match.group(2)}"

    match = re.search(r"(\d+)\s*times\s*(\d+)", text)
    if match:
        return f"{match.group(1)}*{match.group(2)}"

    # --------------------
    # Division
    # --------------------
    match = re.search(r"divide (\d+) by (\d+)", text)
    if match:
        return f"{match.group(1)}/{match.group(2)}"

    match = re.search(r"(\d+)\s*divided by\s*(\d+)", text)
    if match:
        return f"{match.group(1)}/{match.group(2)}"

    # --------------------
    # Modulus
    # --------------------
    match = re.search(r"(\d+)\s*mod\s*(\d+)", text)
    if match:
        return f"{match.group(1)}%{match.group(2)}"

    match = re.search(r"remainder of (\d+) and (\d+)", text)
    if match:
        return f"{match.group(1)}%{match.group(2)}"

    # --------------------
    # Square Root
    # --------------------
    match = re.search(r"square root of (\d+)", text)
    if match:
        return f"sqrt({match.group(1)})"

    # --------------------
    # Power
    # --------------------
    match = re.search(r"(\d+)\s*to the power of\s*(\d+)", text)
    if match:
        return f"{match.group(1)}**{match.group(2)}"

    # If no pattern matches,
    # return the original text.
    return text
# ==========================
# Execute Function
# ==========================
def execute(arguments: dict):
    """
    Execute function used by the Tool Registry.
    """

    expression = arguments.get("expression")

    if not expression:
        return "Calculator Error: Expression not provided."

    # Convert natural language into math expression
    expression = convert_to_expression(expression)

    result = calculator(expression)

    # Format a human-readable reply based on the operator
    if "+" in expression:
        parts = expression.split("+")
        return f"The sum of {parts[0].strip()} + {parts[1].strip()} is {result}"
    elif "-" in expression:
        parts = expression.split("-")
        return f"The difference of {parts[0].strip()} - {parts[1].strip()} is {result}"
    elif "*" in expression and "**" not in expression:
        parts = expression.split("*")
        return f"The product of {parts[0].strip()} * {parts[1].strip()} is {result}"
    elif "/" in expression:
        parts = expression.split("/")
        return f"The division of {parts[0].strip()} / {parts[1].strip()} is {result}"
    elif "%" in expression:
        parts = expression.split("%")
        return f"The remainder of {parts[0].strip()} % {parts[1].strip()} is {result}"
    elif "**" in expression:
        parts = expression.split("**")
        return f"The power of {parts[0].strip()} ^ {parts[1].strip()} is {result}"
    elif expression.startswith("sqrt("):
        return f"The square root is {result}"
    else:
        return f"The result is {result}"


# ==========================
# AST Evaluation
# ==========================
def _evaluate(node):

    # Numbers
    if isinstance(node, ast.Constant):
        return node.value

    # Binary Operations
    elif isinstance(node, ast.BinOp):

        if type(node.op) not in OPERATORS:
            raise ValueError("Unsupported Operator")

        return OPERATORS[type(node.op)](
            _evaluate(node.left),
            _evaluate(node.right),
        )

    # Unary Operations
    elif isinstance(node, ast.UnaryOp):

        if type(node.op) not in OPERATORS:
            raise ValueError("Unsupported Unary Operator")

        return OPERATORS[type(node.op)](
            _evaluate(node.operand)
        )

    # Function Calls
    elif isinstance(node, ast.Call):

        if not isinstance(node.func, ast.Name):
            raise ValueError("Invalid Function")

        func_name = node.func.id

        if func_name not in FUNCTIONS:
            raise ValueError(
                f"Unsupported function: {func_name}"
            )

        args = [_evaluate(arg) for arg in node.args]

        return FUNCTIONS[func_name](*args)

    raise ValueError(
        f"Unsupported expression: {ast.dump(node)}"
    )


# ==========================
# Testing
# ==========================
if __name__ == "__main__":

    print("=" * 50)
    print("Calculator Tool Test")
    print("=" * 50)

    tests = [

        # Normal Expressions
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

        # Natural Language
        {"expression": "sum of 3 and 4"},
        {"expression": "add 10 and 20"},
        {"expression": "subtract 5 from 20"},
        {"expression": "multiply 6 by 8"},
        {"expression": "divide 100 by 4"},
        {"expression": "square root of 625"},
        {"expression": "2 plus 5"},
        {"expression": "20 minus 6"},
        {"expression": "9 times 8"},
        {"expression": "100 divided by 5"},
        {"expression": "15 mod 4"},
        {"expression": "5 to the power of 3"},

        # Questions
        {"expression": "What is the sum of 50 and 25?"},
        {"expression": "Calculate 10 plus 15"},
        {"expression": "Can you divide 81 by 9?"},
        {"expression": "Please multiply 11 by 11"},
        {"expression": "Find square root of 144"},
        {"expression": "Tell me 15 minus 5"},
    ]

    for i, test in enumerate(tests, start=1):

        print("\n" + "-" * 50)
        print(f"Test {i}")
        print("Input :", test["expression"])
        print("Output:", execute(test))

    print("\n" + "=" * 50)
    print("All Tests Completed")
    print("=" * 50)