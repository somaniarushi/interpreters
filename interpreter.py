INTEGER, PLUS, EOF = 'INTEGER', 'PLUS', 'EOF'

class Token:
    def __init__(self, type, value):
        '''
        Accepts and saves the type and value of the token.
        '''
        self.type = type
        self.value = value

    def __repr__(self):
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

    def error(self):
        '''
        Raises parsing error.
        '''
        raise Exception('Error parsing input')

    def get_next_token(self):
        '''
        Tokenizer (AKA scanner or lexical analyzer).
        Breaks the text input into tokens and returns
        them one at a time.
        '''
        text = self.text

        # Reached end of file
        if self.pos > len(text) - 1:
            return Token(EOF, None)

        current_char = text[self.pos]

        if current_char.isdigit():
            token = Token(INTEGER, int(current_char))
            self.pos += 1
            return token

        elif current_char == '+':
            token = Token(PLUS, '+')
            self.pos += 1
            return token

        else:
            self.error()

    def eat(self, token_type):
        '''
        If the current token matches the passed in
        token type, eat it and update self.current_token
        Otherwise, raise error.
        '''
        if self.curent_token.type == token_type:
            self.curent_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        '''
        Returns the text and returns the expression.
        '''
        self.curent_token = self.get_next_token()

        left = self.curent_token
        self.eat(INTEGER)

        op = self.curent_token
        self.eat(PLUS)

        right = self.curent_token
        self.eat(INTEGER)

        result = left.value + right.value
        return result


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
