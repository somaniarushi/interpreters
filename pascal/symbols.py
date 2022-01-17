class Symbol:
    '''
    An identifier of some entity in a program, like a
    variable, a subroutine, or a built-in type.
    '''
    def __init__(self, name, type=None):
        self.name = name
        self.type = type

class BuiltinTypeSymbol(Symbol):
    '''
    A type that is available out of the box,
    like INTEGER or REAL types.
    '''
    def __init__(self, name):
        super().__init__(name)

    def __repr__(self):
        return self.name

class VarSymbol(Symbol):
    def __init__(self, name, type):
        super().__init__(name, type)

    def __repr__(self):
        return f'{self.name}:{self.type}'

class SymbolTable(object):
    '''
    Tracks symbols in source code.
    '''
    def __init__(self):
        self._symbols = {}
        self._init_builtins()

    def _init_builtins(self):
        self.define(BuiltinTypeSymbol('INTEGER'))
        self.define(BuiltinTypeSymbol('REAL'))

    def __repr__(self):
        return f'Symbols: {[v for v in self._symbols.value()]}'

    def define(self, symbol):
        '''
        Defines a symbol into the table.
        '''
        self._symbols[symbol.name] = symbol

    def lookup(self, name):
        '''
        Looks up a name and returns the corresponding symbol
        '''
        return self._symbols.get(name)
