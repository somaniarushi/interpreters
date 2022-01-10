from constants import *
from lexers import Lexer
from parsers import Parser
from interpreters import Interpreter


def main():
    while True:
        try:
            text = input('pys> ')
        except EOFError:
            break
        if not text:
            continue
        if text == 'quit':
            print('pyscal says bye!')
            break
        try:
            lexer = Lexer(text)
            parser = Parser(lexer)
            interpreter = Interpreter(parser)
            result = interpreter.interpret()
            print(result)
        except Exception as e:
            print(f'Error: {e} \n Exiting pyscal...')
            break

if __name__ == '__main__':
    main()
