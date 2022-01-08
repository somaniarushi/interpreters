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
