class IntermediateCodeGenerator:
    def __init__(self, ast):
        self.ast = ast
        self.three_address_code = []
        self.temp_counter = 0
        
    def new_temp(self):
        self.temp_counter += 1
        return f"t{self.temp_counter}"
    
    def generate(self):
        self.visit(self.ast)
        return self.three_address_code
    
    def visit(self, node):
        if node['type'] == 'program':
            for stmt in node['statements']:
                self.visit(stmt)
        elif node['type'] == 'declaration':
            # Declarations don't generate code in three-address form
            pass
        elif node['type'] == 'assignment':
            expr_result = self.visit_expression(node['expression'])
            self.three_address_code.append(f"{node['var_name']} = {expr_result}")
        elif node['type'] == 'print':
            self.three_address_code.append(f"print {node['var_name']}")
        elif node['type'] == 'conditional':
            condition_result = self.visit_condition(node['condition'])
            self.three_address_code.append(f"if {condition_result} goto L{self.temp_counter}")
            for stmt in node['statements']:
                self.visit(stmt)
            self.three_address_code.append(f"L{self.temp_counter}:")
    
    def visit_expression(self, node):
        if node['type'] == 'constant':
            return str(node['value'])
        elif node['type'] == 'identifier':
            return node['value']
        elif node['type'] == 'binary_op':
            left = self.visit_expression(node['left'])
            right = self.visit_expression(node['right'])
            temp = self.new_temp()
            self.three_address_code.append(f"{temp} = {left} {node['operator']} {right}")
            return temp
    
    def visit_condition(self, node):
        left = self.visit_expression(node['left'])
        right = self.visit_expression(node['right'])
        return f"{left} {node['operator']} {right}"

