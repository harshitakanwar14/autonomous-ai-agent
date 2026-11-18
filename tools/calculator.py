
import ast
import operator


# Only allow safe mathematical operations
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos
}


def calculate(expression: str):

    if len(expression) > 200:
        raise ValueError("Expression is too long.")

    def evaluate(node):

        if isinstance(node, ast.Constant):
            if type(node.value) not in (int, float):
                raise ValueError("Only numbers are allowed.")
            return node.value

        elif isinstance(node, ast.BinOp):
            operation = OPERATORS.get(type(node.op))

            if operation is None:
                raise ValueError("Unsupported operation.")

            left = evaluate(node.left)
            right = evaluate(node.right)

            if isinstance(node.op, ast.Pow):
                if abs(right) > 100:
                    raise ValueError("Exponent too large.")

            result = operation(left, right)

            if isinstance(result, (int, float)):
                if abs(result) > 1e100:
                    raise ValueError("Result too large.")

            return result

        elif isinstance(node, ast.UnaryOp):
            operation = OPERATORS.get(type(node.op))

            if operation is None:
                raise ValueError("Unsupported operation.")

            return operation(evaluate(node.operand))

        else:
            raise ValueError("Invalid mathematical expression.")

    try:
        tree = ast.parse(expression, mode="eval")
        return evaluate(tree.body)

    except (SyntaxError, ZeroDivisionError, OverflowError):
        raise ValueError("Invalid mathematical expression.")
