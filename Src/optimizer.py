class ConstantFoldingOptimizer:
    def optimize(self, three_address_code):
        optimized_code = []
        constant_table = {}
        
        for instruction in three_address_code:
            if '=' in instruction:
                left, right = instruction.split('=')
                left = left.strip()
                right = right.strip()
                
                # Check if right side is a constant expression
                try:
                    # Try to evaluate the expression
                    result = eval(right, {}, constant_table)
                    constant_table[left] = result
                    optimized_code.append(f"{left} = {result}")
                except:
                    # Not a constant expression, keep as is
                    optimized_code.append(instruction)
            else:
                optimized_code.append(instruction)
        
        return optimized_code


class CSEOptimizer:
    def optimize(self, three_address_code):
        optimized_code = []
        expression_map = {}  # Maps expressions to temporary variables
        for instruction in three_address_code:
            if '=' in instruction:
                temp, expr = instruction.split('=')
                temp = temp.strip()
                expr = expr.strip()
                if expr in expression_map:
                    # This expression was already computed
                    optimized_code.append(f"{temp} = {expression_map[expr]}")
                else:
                    # First time seeing this expression
                    expression_map[expr] = temp
                    optimized_code.append(instruction)
            else:
                optimized_code.append(instruction)
        return optimized_code


if __name__ == "__main__":
    # Example: Constant folding
    original_code = [
        "t1 = 5 + 3",
        "t2 = t1 * 2",
        "x = t2",
        "y = x + 1"
    ]
    optimizer = ConstantFoldingOptimizer()
    optimized = optimizer.optimize(original_code)
    print("Original:", original_code)
    print("Optimized:", optimized)

    # Example: CSE
    original_code = [
        "t1 = a + b",
        "t2 = a + b",  # Common subexpression
        "t3 = t1 * 2",
        "t4 = a + b"   # Another common subexpression
    ]
    optimizer = CSEOptimizer()
    optimized = optimizer.optimize(original_code)
    print("Original:", original_code)
    print("Optimized:", optimized)

    # This line seems to be a mistake as it's not valid Python code and not related to the optimizers
    # E:/TUA/Assignment/.venv/Scripts/python.exe e:/TUA/Assignment/webapp.py




