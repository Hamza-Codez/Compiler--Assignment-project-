from lexer import Lexer


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.current_token = self.tokens[self.position] if tokens else None
        self.errors = []
        
    def advance(self):
        self.position += 1
        if self.position >= len(self.tokens):
            self.current_token = None
        else:
            self.current_token = self.tokens[self.position]
    
    def match(self, expected_type, expected_value=None):
        if self.current_token and self.current_token[0] == expected_type:
            if expected_value is None or self.current_token[1] == expected_value:
                token = self.current_token
                self.advance()
                return token
        return None
    
    def parse_program(self):
        """program → statement_list"""
        statements = self.parse_statement_list()
        return {'type': 'program', 'statements': statements}
    
    def parse_statement_list(self):
        """statement_list → statement | statement statement_list"""
        print('Entering parse_statement_list, current_token:', self.current_token)
        statements = []
        while self.current_token and self.current_token[0] != 'EOF':
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        print('Exiting parse_statement_list, statements:', len(statements))
        return statements
    
    def parse_statement(self):
        """statement → declaration | assignment | print_stmt | conditional"""
        print('In parse_statement, current_token:', self.current_token)
        # Skip stray semicolons to prevent infinite loop
        if self.current_token and self.current_token == ('DELIMITER', ';'):
            self.advance()
            return None
        if self.match('KEYWORD', 'int') or self.match('KEYWORD', 'float'):
            self.position -= 1  # Go back
            return self.parse_declaration()
        elif self.current_token and self.current_token[0] == 'IDENTIFIER':
            return self.parse_assignment()
        elif self.match('KEYWORD', 'print'):
            return self.parse_print()
        elif self.match('KEYWORD', 'if'):
            return self.parse_conditional()
        return None
    
    def parse_declaration(self):
        """declaration → 'int' IDENTIFIER ';' | 'float' IDENTIFIER ';'"""
        type_token = self.match('KEYWORD')
        if not type_token:
            self.errors.append("Expected type keyword (int/float)")
            return None
            
        id_token = self.match('IDENTIFIER')
        if not id_token:
            self.errors.append("Expected identifier after type")
            return None
            
        if not self.match('DELIMITER', ';'):
            self.errors.append("Expected ';' after declaration")
            return None
            
        return {'type': 'declaration', 'var_type': type_token[1], 'var_name': id_token[1]}
    
    def parse_assignment(self):
        """assignment → IDENTIFIER '=' expression ';'"""
        id_token = self.match('IDENTIFIER')
        if not id_token:
            return None
            
        if not self.match('OPERATOR', '='):
            self.errors.append("Expected '=' in assignment")
            return None
            
        expr = self.parse_expression()
        if not expr:
            self.errors.append("Expected expression after '='")
            return None
            
        if not self.match('DELIMITER', ';'):
            self.errors.append("Expected ';' after assignment")
            return None
            
        return {'type': 'assignment', 'var_name': id_token[1], 'expression': expr}
    
    def parse_expression(self):
        """expression → term | expression ADD_OP term"""
        node = self.parse_term()
        
        while self.current_token and self.current_token[1] in ('+', '-'):
            operator = self.match('OPERATOR')
            right = self.parse_term()
            node = {'type': 'binary_op', 'operator': operator[1], 'left': node, 'right': right}
            
        return node
    
    def parse_term(self):
        """term → factor | term MUL_OP factor"""
        node = self.parse_factor()
        
        while self.current_token and self.current_token[1] in ('*', '/'):
            operator = self.match('OPERATOR')
            right = self.parse_factor()
            node = {'type': 'binary_op', 'operator': operator[1], 'left': node, 'right': right}
            
        return node
    
    def parse_factor(self):
        """factor → IDENTIFIER | CONSTANT | '(' expression ')'"""
        if self.match('DELIMITER', '('):
            node = self.parse_expression()
            if not self.match('DELIMITER', ')'):
                self.errors.append("Expected ')'")
            return node
        elif token := self.match('IDENTIFIER'):
            return {'type': 'identifier', 'value': token[1]}
        elif token := self.match('CONSTANT'):
            return {'type': 'constant', 'value': token[1]}
        else:
            self.errors.append("Expected identifier, constant, or '('")
            return None
    
    def parse_print(self):
        """print_stmt → 'print' '(' IDENTIFIER ')' ';'"""
        if not self.match('DELIMITER', '('):
            self.errors.append("Expected '(' after print")
            return None
            
        id_token = self.match('IDENTIFIER')
        if not id_token:
            self.errors.append("Expected identifier in print statement")
            return None
            
        if not self.match('DELIMITER', ')'):
            self.errors.append("Expected ')' after identifier")
            return None
            
        if not self.match('DELIMITER', ';'):
            self.errors.append("Expected ';' after print statement")
            return None
            
        return {'type': 'print', 'var_name': id_token[1]}
    
    def parse_conditional(self):
        """conditional → 'if' '(' condition ')' '{' statement_list '}'"""
        if not self.match('DELIMITER', '('):
            self.errors.append("Expected '(' after if")
            return None
            
        condition = self.parse_condition()
        if not condition:
            self.errors.append("Expected condition")
            return None
            
        if not self.match('DELIMITER', ')'):
            self.errors.append("Expected ')' after condition")
            return None
            
        if not self.match('DELIMITER', '{'):
            self.errors.append("Expected '{' after if condition")
            return None
            
        statements = []
        while self.current_token and self.current_token[1] != '}':
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
                
        if not self.match('DELIMITER', '}'):
            self.errors.append("Expected '}' to close if block")
            return None
            
        return {'type': 'conditional', 'condition': condition, 'statements': statements}
    
    def parse_condition(self):
        """condition → expression REL_OP expression"""
        left = self.parse_expression()
        if not left:
            return None
            
        rel_op = self.match('OPERATOR')
        if not rel_op or rel_op[1] not in ('>', '<', '==', '!='):
            self.errors.append("Expected relational operator")
            return None
            
        right = self.parse_expression()
        if not right:
            return None
            
        return {'type': 'condition', 'left': left, 'operator': rel_op[1], 'right': right}
    
    def parse(self):
        ast = self.parse_program()
        return ast, self.errors

