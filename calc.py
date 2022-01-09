INTEGER, PLUS, MINUS, EOF = 'INTEGER', 'PLUS', 'MINUS', 'EOF'

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
        self.current_token = None
        self.current_char = self.text[self.pos]

    def error(self):
        '''
        Raises parsing error.
        '''
        raise Exception('Error parsing input')

    def advance(self):
        '''
        Advance the self.pos pointer, and
        update self.current_char
        '''
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None # EOF
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        '''
        Advances through the string over
        all whitespace starting at current_char
        '''
        # while we see a space and we haven't reached
        # the end of the file
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        '''
        Return the integer consumed from the input.
        The pointer and current_char is updated
        '''
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        '''
        Tokenizer (AKA scanner or lexical analyzer).
        Breaks the text input into tokens and returns
        them one at a time.
        '''
        # while we haven't reached end of file
        while self.current_char is not None:

            current_char = self.current_char

            if current_char.isspace():
                self.skip_whitespace()
                continue

            elif current_char.isdigit():
                token = Token(INTEGER, self.integer())
                return token

            elif current_char == '+':
                token = Token(PLUS, '+')
                self.advance()
                return token

            elif current_char == '-':
                token = Token(MINUS, '-')
                self.advance()
                return token

            else:
                self.error()

        return Token(EOF, None)

    def eat(self, token_type):
        '''
        If the current token matches the passed in
        token type, eat it and update self.current_token
        Otherwise, raise error.
        '''
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def term(self):
        '''
        Returns the INTEGER token value that is current_token and
        eats the current_token
        '''
        token = self.current_token
        self.eat(INTEGER)
        return token.value

    def expr(self):
        '''
        Returns the text and returns the expression.
        '''
        self.current_token = self.get_next_token()
        result = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
                result = result + self.term()
            elif token.type == MINUS:
                self.eat(MINUS)
                result = result - self.term()

        # if self.current_token.type != EOF:
        #   self.error()

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
