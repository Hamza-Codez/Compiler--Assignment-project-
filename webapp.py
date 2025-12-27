from flask import Flask, render_template, request, jsonify
import os
import sys

# Ensure the Src directory is importable
ROOT = os.path.dirname(__file__)
SRC_DIR = os.path.join(ROOT, 'Src')
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer
from codegen import IntermediateCodeGenerator
from optimizer import ConstantFoldingOptimizer, CSEOptimizer

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compile', methods=['POST'])

def compile_code():
    print('>>> /compile endpoint called')
    sys.stdout.flush()
    print('Received /compile request')
    try:
        data = request.get_json() or {}
        source = data.get('source', '')


        print('Phase 1: Lexical')
        sys.stdout.flush()
        lexer = Lexer(source)
        tokens, symbol_table = lexer.tokenize()


        print('Phase 2: Syntax')
        sys.stdout.flush()
        parser = Parser(tokens)
        ast, parse_errors = parser.parse()
        print("Parser returned")
        sys.stdout.flush()


        print('Phase 3: Semantic')
        print('AST:', ast)
        sys.stdout.flush()
        semantic_errors = []
        if ast:
            try:
                analyzer = SemanticAnalyzer(ast)
                semantic_errors = analyzer.analyze()
                print('Semantic analysis complete')
            except Exception as e:
                print('Error during semantic analysis:', e)
                import traceback
                traceback.print_exc()
        sys.stdout.flush()


        print('Phase 4: IR')
        sys.stdout.flush()
        three_address_code = []
        if ast and not parse_errors and not semantic_errors:
            generator = IntermediateCodeGenerator(ast)
            three_address_code = generator.generate()


        print('Phase 5: Optimization')
        sys.stdout.flush()
        folded = ConstantFoldingOptimizer().optimize(three_address_code)
        optimized = CSEOptimizer().optimize(folded)

        response = {
            'tokens': tokens,
            'symbol_table': symbol_table,
            'ast': ast,
            'parse_errors': parse_errors,
            'semantic_errors': semantic_errors,
            'three_address_code': three_address_code,
            'optimized_code': optimized
        }
        return jsonify(response)
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        print('ERROR in /compile:', tb)
        return jsonify({'error': str(e), 'traceback': tb}), 500

if __name__ == '__main__':
    app.run(debug=False, port=5000, use_reloader=False)
