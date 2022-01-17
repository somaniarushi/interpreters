from pascal.constants import *

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

'''
Keywords that are built-in and therefore cannot be made variables.
'''
RESERVED_KEYWORDS = {
    'PROGRAM': Token('PROGRAM', 'PROGRAM'),
    'VAR': Token('VAR', 'VAR'),
    'DIV': Token('INTEGER_DIV', 'DIV'),
    'INTEGER': Token('INTEGER', 'INTEGER'),
    'REAL': Token('REAL', 'REAL'),
    'BEGIN': Token('BEGIN', 'BEGIN'),
    'END': Token('END', 'END'),
}


class Lexer:
    def __init__(self, text):
        '''
        Accepts a string input from the client as text,
        and maintains an index into text, the current char and the
        current token instance.
        '''
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        '''
        Raises parsing error.
        '''
        raise Exception('Invalid character')

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

    def skip_comment(self):
        '''
        Assumes that an opening curly bracket has been found
        and advances pointer to blosing curly bracket
        '''
        while self.current_char != '}':
            if self.current_char is None:
                self.error()
            self.advance()
        self.advance() # skipping the closing curly brace as well

    def peek(self):
        '''
        Returns the next element of the input buffer,
        or None if EOF.
        '''
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def _id(self):
        '''
        Handles identifiers and reserved keywords.
        '''
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()
        token = RESERVED_KEYWORDS.get(result, Token(ID, result))
        return token


    def number(self):
        '''
        Return the number consumed from the input — multi-digit integer or float.
        The pointer and current_char is updated
        '''
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        if self.current_char == '.': # float
            result += self.current_char
            self.advance()

            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()

            token = Token('REAL_CONST', float(result))
        else: # integer
            token = Token('INTEGER_CONST', int(result))

        return token

    def get_next_token(self):
        '''
        Tokenizer (AKA scanner or lexical analyzer).
        Breaks the text input into tokens and returns
        them one at a time.
        '''
        # while we haven't reached end of file
        while self.current_char is not None:

            current_char = self.current_char

            # whitespace
            if current_char.isspace():
                self.skip_whitespace()
                continue

            # comment
            elif current_char == '{':
                self.advance() # TODO: is this necessary
                self.skip_comment()
                continue

            # keyword
            elif self.current_char.isalpha():
                return self._id()

            # number
            elif current_char.isdigit():
                return self.number()

            # assignment operator
            elif self.current_char == ':' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(ASSIGN, ':=')

            # semi-colon
            elif self.current_char == ';':
                self.advance()
                return Token(SEMI, ';')

            # colon
            elif self.current_char == ':':
                self.advance()
                return Token(COLON, ':')

            # comma
            elif self.current_char == ',':
                self.advance()
                return Token(COMMA, ',')

            # plus
            elif current_char == '+':
                token = Token(PLUS, '+')
                self.advance()
                return token

            # minus
            elif current_char == '-':
                token = Token(MINUS, '-')
                self.advance()
                return token

            # multiply
            elif self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            # float division
            elif self.current_char == '/':
                self.advance()
                return Token(FLOAT_DIV, '/')

            # lparen
            elif self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            # rparen
            elif self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            # dot
            elif self.current_char == '.':
                self.advance()
                return Token(DOT, '.')

            else:
                self.error()

        return Token(EOF, None)
