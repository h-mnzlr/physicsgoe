# begin parser.py

from .lexer import Lexer
from .algebraic_function_grammar import linking_operator_order
from .algebraic_function_grammar import linking_operator_dict
from .algebraic_function_grammar import calculation_operator_dict
from .algebraic_function_grammar import Constant, Parameter

# Parser-Class that uses a Lexer to interpret a String into a function object


def parse(s):
    return Parser(s).parse()


class Parser:

    # expr -> statement
    # expr -> expr (op expr)*
    # statement -> num
    # statement -> parameter
    # statement -> func statement
    # statement -> LPAREN expr RPAREN

    def __init__(self, strg=None, lexer=None):
        self.strg = strg
        if strg:
            self.lexer = Lexer(strg)
        else:
            self.lexer = lexer
        self.curr_token = next(self.lexer)

    def parse(self):
        return self.expr()

    def next_token(self):
        try:
            return next(self.lexer)
        except StopIteration:
            return ('END', 'eof')

    def eat(self, class_type):
        # print(f'eating {class_type}, token: {self.curr_token}')
        # print(self.lexer)
        if self.curr_token[0] == class_type:
            self.curr_token = self.next_token()
        else:
            raise TypeError(f'''Bad Input: expected {class_type} and got
            {self.curr_token[0]} while parsing {self.strg}.''')

    def expr(self, depth=0):
        # print(f'evaluating expression at token: {self.curr_token}, depth: {depth}')
        if depth < len(linking_operator_order) - 1:
            node = self.expr(depth + 1)
        else:
            node = self.statement()

        while self.curr_token[1] in linking_operator_order[depth]:
            for op_str in linking_operator_order[depth]:
                # print(f'looking for {op_str}')
                op_class = linking_operator_dict[op_str]
                if self.curr_token[0] == op_class:
                    # print(f'found {op_str}')

                    self.eat(op_class)
                    node = op_class(node, self.expr(depth - 1))
        return node

    def statement(self):
        # print(f'evaluating statement at token: {self.curr_token}')
        token = self.curr_token
        if token[0] in (Constant, Parameter):
            self.eat(token[0])
            node = token[0](token[1])
        elif token[1] in calculation_operator_dict:
            self.eat(token[0])
            node = token[0](self.statement())
        elif token[0] == 'LBRACKET':
            self.eat('LBRACKET')
            node = self.expr()
            self.eat('RBRACKET')
        else:
            raise TypeError(f'Couldn\'t understand token: {token}')
        return node

# end parser.py
