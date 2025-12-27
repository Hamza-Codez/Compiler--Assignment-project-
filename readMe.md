# SimpleLang Compiler Web Demo

**Submitted by:** Hamza Ahmad  
**BS CS**  
**Reg #: 2022-ag-7751**

---

## Project Overview
This project is a simple compiler for a toy language (SimpleLang) with a web-based frontend. It demonstrates all phases of compilation: lexical analysis, parsing, semantic analysis, intermediate code generation, and code optimization. The web UI allows you to enter code, compile it, and see tokens, AST, symbol table, three-address code, and optimized code.

---

## How to Run on Any Computer

### 1. Clone or Download the Project
- Copy the project folder to your computer (or clone from your repository if available).

### 2. Install Python (if not already installed)
- Download Python 3.10+ from https://www.python.org/downloads/
- Add Python to your PATH during installation.

### 3. Create and Activate a Virtual Environment (Recommended)
Open a terminal (Command Prompt or PowerShell) in the project folder:

```
python -m venv .venv
.\.venv\Scripts\activate  # On Windows
```

### 4. Install Required Packages
```
pip install flask
```

### 5. Start the Web Server
```
python webapp.py
```
Or, if using the venv:
```
.venv\Scripts\python.exe webapp.py
```

### 6. Open the Web UI
## Enter in your terminal to start fask server 
- .venv/Scripts/python.exe webapp.py 

- Go to [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.
- Enter SimpleLang code and click **Compile** to see all compiler phases.


---

## Project Structure
- `webapp.py` — Flask web server
- `templates/index.html` — Web UI
- `static/style.css` — UI styling
- `Src/lexer.py` — Lexical analyzer
- `Src/parser.py` — Parser
- `Src/semantic.py` — Semantic analyzer
- `Src/codegen.py` — Intermediate code generator
- `Src/optimizer.py` — Code optimizers

---

## Troubleshooting
- If you see errors about missing modules, run `pip install flask` again.
- If the server does not start, make sure you are in the correct folder and using the right Python version.
- If the web page does not load, check the terminal for errors and ensure the server is running.

---

## Author
Hamza Ahmad  
BS CS  
Reg #: 2022-ag-7751
