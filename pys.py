from pascal.constants import *
from pascal.lexers import Lexer
from pascal.parsers import Parser
from pascal.interpreters import Interpreter
from visualizer.visualizer import ASTVisualizer
from visualizer.viztools import VizParser, VizLexer


def main():
    import sys
    text = open(sys.argv[1], 'r').read()
    visualize = False
    if len(sys.argv) > 2:
        if sys.argv[2] == '--visualize':
            visualize = True

    if visualize:
        lexer = VizLexer(text)
        parser = VizParser(lexer)
        visualizer = ASTVisualizer(parser)
        visualizer.visualize()
    else:
        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        result = interpreter.interpret()
        print(interpreter.GLOBAL_SCOPE)

    # while True:
    #     try:
    #         text = input('pys> ')
    #     except EOFError:
    #         break
    #     if not text:
    #         continue
    #     if text == 'quit':
    #         print('pyscal says bye!')
    #         break
    #     try:
    #         lexer = Lexer(text)
    #         parser = Parser(lexer)
    #         interpreter = Interpreter(parser)
    #         result = interpreter.interpret()
    #         print(result)
    #     except Exception as e:
    #         print(f'Error: {e} \n Exiting pyscal...')
    #         break

if __name__ == '__main__':
    main()
