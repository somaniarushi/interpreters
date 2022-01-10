############################ LEXER ###############################

INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, EOF = (
    'INTEGER', 'PLUS', 'MUL', 'DIV', 'MINUS', '(', ')', 'EOF'
)

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

            elif self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            elif self.current_char == '/':
                self.advance()
                return Token(DIV, '/')

            elif self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            elif self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            else:
                self.error()

        return Token(EOF, None)

################################## PARSER ###########################

class AST:
    pass

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Parser:
    def __init__(self, lexer):
        '''
        Accepts a string input from the client as text,
        and maintains an index into text and the
        current token instance.
        '''
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def eat(self, token_type):
        '''
        If the current token matches the passed in
        token type, eat it and update self.current_token
        Otherwise, raise error.
        '''
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        '''
        Returns the factor AST that is current_token and
        eats the current_token

        factor : INTEGER | ( expr )
        '''
        token = self.current_token
        if token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node

    def term(self):
        '''
        Returns the AST term starting at current_token and eats values as necessary

        term: factor ((MUL | DIV) factor) *
        '''
        node = self.factor()
        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == DIV:
                self.eat(DIV)
            node = BinOp(left=node, op=token, right=self.factor())
        return node

    def expr(self):
        '''
        Parses the text and returns the expression.

        expr: term ((PLUS | MINUS) term)*
        term: factor ((MUL | DIV) factor)*
        factor: INTEGER
        '''
        node = self.term()
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)
            node = BinOp(left=node, op=token, right=self.term())
        return node

    def parse(self):
        return self.expr()

############################# INTERPRETER ##########################

class NodeVisitor:
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))


class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser

    def visit_BinOp(self, node):
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == DIV:
            return self.visit(node.left) // self.visit(node.right)

    def visit_Num(self, node):
        return node.value

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)



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
