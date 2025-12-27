import re

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.position = 0
        self.current_char = self.source_code[self.position] if source_code else None
        self.symbol_table = {}
        
    # Token types
    KEYWORDS = {'int', 'float', 'if', 'else', 'print'}
    OPERATORS = {'+', '-', '*', '/', '=', '>', '<', '==', '!='}
    DELIMITERS = {';', ',', '(', ')', '{', '}'}
    
    def advance(self):
        self.position += 1
        if self.position >= len(self.source_code):
            self.current_char = None
        else:
            self.current_char = self.source_code[self.position]
    
    def get_next_token(self):
        while self.current_char and self.current_char.isspace():
            self.advance()
            
        if not self.current_char:
            return None
            
        # Identifiers and keywords
        if self.current_char.isalpha() or self.current_char == '_':
            identifier = ''
            while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
                identifier += self.current_char
                self.advance()
                
            if identifier in self.KEYWORDS:
                return ('KEYWORD', identifier)
            else:
                # Add to symbol table
                if identifier not in self.symbol_table:
                    self.symbol_table[identifier] = {'type': None, 'value': None}
                return ('IDENTIFIER', identifier)
        
        # Numbers
        if self.current_char.isdigit():
            number = ''
            while self.current_char and (self.current_char.isdigit() or self.current_char == '.'):
                number += self.current_char
                self.advance()
            return ('CONSTANT', float(number) if '.' in number else int(number))
        
        # Operators
        if self.current_char in self.OPERATORS:
            op = self.current_char
            self.advance()
            # Check for double character operators
            if op in ('=', '!', '<', '>') and self.current_char == '=':
                op += self.current_char
                self.advance()
            return ('OPERATOR', op)
        
        # Delimiters
        if self.current_char in self.DELIMITERS:
            delim = self.current_char
            self.advance()
            return ('DELIMITER', delim)
        
        # Unknown character
        char = self.current_char
        self.advance()
        return ('UNKNOWN', char)
    
    def tokenize(self):
        tokens = []
        while True:
            token = self.get_next_token()
            if not token:
                break
            tokens.append(token)
        return tokens, self.symbol_table

