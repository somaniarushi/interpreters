INTEGER, PLUS, EOF = 'INTEGER', 'PLUS', 'EOF'

class Token:
    def __init__(self, type, value):
        '''
        Accepts and saves the type and value of the token.
        '''
        self.type = type
        self.value = value

    def __str__(self):
        '''
        String representation of an object.
        '''
        return f'Token({self.type}, {self.value})'


class Interpreter:
    def __init__(self, text):
        '''
        Accepts a string input from the client as text,
        and maintains an index into text and the
        current token instance.
        '''
        self.text = text
        self.pos = 0
        self.curent_token = None

    def get_next_token(self):
        '''
        Tokenizer (AKA scanner or lexical analyzer).
        Breaks the text input into tokens and returns
        them one at a time.
        '''
        text = self.text


    def expr(self):
        '''
        Returns the text and returns the expression.
        '''
        return self.text


def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)

if __name__ == '__main__':
    main()
