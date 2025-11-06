import ast
import asyncio
import operator
import re
from concurrent.futures import ThreadPoolExecutor

from crewai.tools import BaseTool


class CalculatorTool(BaseTool):
    name: str = "Calculator tool"
    description: str = (
        "Useful to perform any mathematical calculations, like sum, minus, "
        "multiplication, division, etc. "
        "The input to this tool should be a mathematical expression, "
        "a couple examples are `200*7` or `5000/2*10`."
    )

    async def _arun(self, operation: str) -> float:
        await asyncio.sleep(0)  # Simulate async context
        return self._calculate(operation)

    def run_async_code(self, operation: str) -> float:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(self._arun(operation))
        loop.close()
        return result

    def _run(self, operation: str) -> float:
        with ThreadPoolExecutor() as executor:
            future = executor.submit(self.run_async_code, operation)
            result = future.result()
        return result

    def _calculate(self, operation: str) -> float:
        try:
            allowed_operators = {
                ast.Add: operator.add,
                ast.Sub: operator.sub,
                ast.Mult: operator.mul,
                ast.Div: operator.truediv,
                ast.Pow: operator.pow,
                ast.Mod: operator.mod,
                ast.USub: operator.neg,
                ast.UAdd: operator.pos,
            }
            if not re.match(r"^[0-9+\-*/().% ]+$", operation):
                raise ValueError("Invalid characters in mathematical expression")
            tree = ast.parse(operation, mode="eval")

            def _eval_node(node):
                if isinstance(node, ast.Expression):
                    return _eval_node(node.body)
                elif isinstance(node, ast.Constant):  # Python 3.8+
                    return node.value
                elif isinstance(node, ast.Num):  # Python < 3.8
                    return node.n
                elif isinstance(node, ast.BinOp):
                    left = _eval_node(node.left)
                    right = _eval_node(node.right)
                    op = allowed_operators.get(type(node.op))
                    if op is None:
                        raise ValueError(
                            f"Unsupported operator: {type(node.op).__name__}"
                        )
                    return op(left, right)
                elif isinstance(node, ast.UnaryOp):
                    operand = _eval_node(node.operand)
                    op = allowed_operators.get(type(node.op))
                    if op is None:
                        raise ValueError(
                            f"Unsupported operator: {type(node.op).__name__}"
                        )
                    return op(operand)
                else:
                    raise ValueError(f"Unsupported node type: {type(node).__name__}")

            result = _eval_node(tree)
            return result  # type: ignore
        except (SyntaxError, ValueError, ZeroDivisionError, TypeError) as e:
            raise ValueError(f"Calculation error: {str(e)}") from e
        except Exception as e:
            raise ValueError("Invalid mathematical expression") from e


if __name__ == "__main__":
    calc_tool = CalculatorTool()
    test_expressions = [
        "2+2",
        "10/2*5",
        "(3+7)*2",
        "100-25*2",
        "2**8",
        "10%3",
    ]
    print("Synchronous test:")
    for expr in test_expressions:
        try:
            result = calc_tool._run(expr)
            print(f"{expr} = {result}")
        except Exception as e:
            print(f"Error evaluating '{expr}': {e}")

    print("\nAsync test:")

    async def async_test():
        for expr in test_expressions:
            try:
                result = await calc_tool._arun(expr)
                print(f"{expr} = {result}")
            except Exception as e:
                print(f"Error evaluating '{expr}': {e}")

    asyncio.run(async_test())
