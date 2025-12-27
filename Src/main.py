# main.py - Complete Mini Compiler

import sys
from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer
from codegen import IntermediateCodeGenerator
from optimizer import ConstantFoldingOptimizer, CSEOptimizer

class SimpleLangCompiler:
    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []
        self.ast = None
        self.errors = []
        self.symbol_table = {}
        self.three_address_code = []
        self.optimized_code = []
        
    def compile(self):
        print("=== SimpleLang Compiler ===\n")
        
        # Phase 1: Lexical Analysis
        print("1. Lexical Analysis:")
        lexer = Lexer(self.source_code)
        self.tokens, self.symbol_table = lexer.tokenize()
        print(f"   Tokens generated: {len(self.tokens)}")
        print(f"   Symbol table: {self.symbol_table}\n")
        
        # Phase 2: Syntax Analysis
        print("2. Syntax Analysis:")
        parser = Parser(self.tokens)
        self.ast, parse_errors = parser.parse()
        if parse_errors:
            print(f"   Syntax errors: {parse_errors}")
            return False
        print("   AST built successfully\n")
        
        # Phase 3: Semantic Analysis
        print("3. Semantic Analysis:")
        analyzer = SemanticAnalyzer(self.ast)
        semantic_errors = analyzer.analyze()
        if semantic_errors:
            print(f"   Semantic errors: {semantic_errors}")
            return False
        print("   No semantic errors\n")
        
        # Phase 4: Intermediate Code Generation
        print("4. Intermediate Code Generation:")
        generator = IntermediateCodeGenerator(self.ast)
        self.three_address_code = generator.generate()
        print("   Three-address code:")
        for code in self.three_address_code:
            print(f"     {code}")
        print()
        
        # Phase 5: Code Optimization
        print("5. Code Optimization:")
        # Apply constant folding
        cf_optimizer = ConstantFoldingOptimizer()
        folded_code = cf_optimizer.optimize(self.three_address_code)
        
        # Apply CSE
        cse_optimizer = CSEOptimizer()
        self.optimized_code = cse_optimizer.optimize(folded_code)
        
        print("   Optimized code:")
        for code in self.optimized_code:
            print(f"     {code}")
        print()
        
        return True

def main():
    if len(sys.argv) > 1:
        # Read from file
        with open(sys.argv[1], 'r') as f:
            source_code = f.read()
    else:
        # Interactive mode
        print("Enter SimpleLang code (Ctrl+D to finish):")
        source_code = sys.stdin.read()
    
    compiler = SimpleLangCompiler(source_code)
    success = compiler.compile()
    
    if success:
        print("Compilation successful!")
    else:
        print("Compilation failed with errors.")

if __name__ == "__main__":
    main()