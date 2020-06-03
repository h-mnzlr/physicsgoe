# begin lexer.py

# TODO: replace tokenizer with a generator in lexer class without RegEx
import re
from .algebraic_function_grammar import calculation_operator_dict
from .algebraic_function_grammar import linking_operator_dict
from .algebraic_function_grammar import linking_operator_order
from .algebraic_function_grammar import bracket_operators
from .algebraic_function_grammar import Constant, Parameter

# Lexer-Class to interpret a String to tokens of a given grammar


class Lexer:
    '''
    '''

    def __init__(self, strg=None, tokens=None):
        self.pos = 0
        if tokens:
            self.tokens = tokens
        else:
            self.tokens = tokenize_string(strg)

    def parameter_list(self):
        rv_ls = []
        for token in self.tokens:
            if token[0] == Parameter and token[1] not in rv_ls:
                rv_ls.append(token[1])
        return rv_ls

    def __iter__(self):
        return self

    def __next__(self):
        # print('next')
        self.pos += 1

        if self.pos <= len(self.tokens):
            return self.tokens[self.pos - 1]
        else:
            raise StopIteration

    def __str__(self):
        strg = 'Lexer:\n'
        for index, token in enumerate(self.tokens):
            if index == self.pos:
                strg += '>'
            strg += f'\t{token}\n'
        return strg[:-1]


def tokenize_string(strg):
    '''Take a string and return a corresponding list of tokens.'''
    # strg = strg.replace(' ', '')
    tokens = []
    regex = r'('
    for op in all_operators():
        regex += escape_string_regex(op) + r'|'
    regex += r'[a-z]|[A-Z]|[0-9]+\.[0-9]+|\.[0-9]+|[0-9]+\.|[0-9]+)'
    regex.replace(' ', '')
    pattern = re.compile(r'' + regex)
    for match in pattern.finditer(strg):
        span = match.span()
        token = token_class_type(strg[span[0]:span[1]])
        tokens.append(token)
    return tokens


def token_class_type(identifier):
    '''Take the identifier of a token and return the corresponding token.'''
    if identifier in bracket_operators[0]:
        return ('LBRACKET', identifier)
    elif identifier in bracket_operators[1]:
        return ('RBRACKET', identifier)
    elif identifier in linking_operator_dict:
        return (linking_operator_dict[identifier], identifier)
    elif identifier in calculation_operator_dict:
        return (calculation_operator_dict[identifier], identifier)
    elif identifier.isalpha():
        return (Parameter, identifier)
    elif identifier[0].isdigit() or (identifier[0] == '.' and identifier[1].isdigit()):
        return (Constant, float(identifier))
    else:
        raise TypeError('Identifier not found: String might be invalid')


def all_operators():
    '''Return a list of every identifier for a token sorted by length.'''
    ls = []
    for brackets in bracket_operators:
        for op in brackets:
            ls.append(op)
    for key in linking_operator_dict:
        ls.append(key)
    for key in calculation_operator_dict:
        ls.append(key)
    return sorted(ls, key=len)[::-1]


def escape_string_regex(strg):
    '''Escape all characters of a string by ReGEx-Convention.'''
    rv_strg = ''
    for char in strg:
        c = escape_char_regex(char)
        rv_strg += escape_char_regex(char)
    return rv_strg


def escape_char_regex(char):
    '''Escape a single character if necessary using the ReGEx-Convention.'''
    if char in _regex_must_be_escaped:
        return '\\' + char
    else:
        return char


# Vital constants for runtime computation - not to be changed

_regex_must_be_escaped = ['.', '^', '$', '*', '+',
                          '-', '?', '(', ')', '{',
                          '}', '\\', '[', ']']

# end lexer.py
