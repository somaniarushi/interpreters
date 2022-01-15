# Learning to make interpreters!
Inspired by ruslanspivak's excellent articles on how interpreters function.

In this repository, you will find:
- making a simple calculator parser in `calc.py`
  - addition, subtraction, multiplication and division support with integers
  - associativity and precedence support
  - parenthetical expression support
  - unary operation support
  - basic error handling with `quit` instruction
- AST support!
  - Lexer -> Parser -> Interpreter pipeline
- a Pascal interpreter split across  `lexer.py`, `parser.py` and `interpreter.py`
  - Grammar defined by `grammar.lark`
  - Example cases in `inputs/`

