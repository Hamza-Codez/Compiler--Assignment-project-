class SemanticAnalyzer:
    def __init__(self, ast):
        self.ast = ast
        self.symbol_table = {}
        self.errors = []
        
    def analyze(self):
        self.visit(self.ast)
        return self.errors
    
    def visit(self, node):
        if node['type'] == 'program':
            for stmt in node['statements']:
                self.visit(stmt)
        elif node['type'] == 'declaration':
            var_name = node['var_name']
            if var_name in self.symbol_table:
                self.errors.append(f"Multiple declaration of variable '{var_name}'")
            else:
                self.symbol_table[var_name] = {
                    'type': node['var_type'],
                    'initialized': False
                }
        elif node['type'] == 'assignment':
            var_name = node['var_name']
            if var_name not in self.symbol_table:
                self.errors.append(f"Undeclared variable '{var_name}'")
            else:
                self.symbol_table[var_name]['initialized'] = True
                self.visit(node['expression'])
        elif node['type'] == 'print':
            var_name = node['var_name']
            if var_name not in self.symbol_table:
                self.errors.append(f"Undeclared variable '{var_name}' in print statement")
        elif node['type'] == 'binary_op':
            self.visit(node['left'])
            self.visit(node['right'])
        elif node['type'] == 'identifier':
            var_name = node['value']
            if var_name not in self.symbol_table:
                self.errors.append(f"Undeclared variable '{var_name}'")
    
