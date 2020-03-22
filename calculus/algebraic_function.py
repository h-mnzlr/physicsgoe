##### Start algebraicFunction.py - importing necessary modules ################

import math
import re


##### Some Structure giving decorators #########################################
import functools

def list_input_kwargs(f):
    '''
    Wrapper that allows functions that usually can not handle iterables passed
    through **kwargs to return a list of function calls of the given function.
    '''
    # wrapper function
    @functools.wraps(f)
    def func(*args, **kwargs):
        try:
            kwargs_list = dict_list(kwargs)
        except TypeError: # no lists in kwargs
            return f(*args, **kwargs)
        # calling function
        rv_ls = []
        for kwargs in kwargs_list:
            rv_ls.append( f(*args, **kwargs) )
        return rv_ls

    return func


def dict_list(list_dict):
    '''
    Function that transforms a dictionary of lists into a list of dictionaries
    using no Comprehensions.
    If all dict values do not contain iterables a TypeError is raised.
    If there is no dict given as input an NotImplementedError is raised.
    '''
    if not isinstance(list_dict, dict):
        raise NotImplementedError
    rv_ls = []
    lengths = list( list_lengths( list_dict ) )
    max_length = max( lengths )
    if max_length <= 1:
        raise TypeError('Not iterable.')
    for i in range(max_length):
        dictio = {}
        for index, key in enumerate(list_dict):
            try:
                dictio[key] = list_dict[key][i]
            except IndexError: # index out of bounds - using last valid index
                dictio[key] = list_dict[key][ lengths[ index ]-1 ]
            except TypeError: # list_dict[key] is not subscribtable - using no indexing
                dictio[key] = list_dict[key]
        rv_ls.append(dictio)
    return rv_ls
    '''
    Shorter but less robust similar solution only valid if all lists are of
    same length using comprehensions.
    If all dict values do not contain iterables a TypeError is raised.
    If there is no dict given as input an NotImplementedError is raised.
    -----------
    Not in use.
    '''
    if not isinstance(list_dict, dict):
        raise NotImplementedError
    max_length = max( list_lengths(list_dict) )
    if max_length <= 1:
        raise TypeError('Not iterable.')

    rv = [ { key: item[i] for key, item in list_dict.items() } for i in range(max_length) ]
    return rv


def list_lengths(list_dict):
    '''
    Function that evaluates a dictionary of iterables and returns a generator of
    the length for each dict value.
    '''
    for item in list_dict.values():
        try:
            yield len(item)
        except TypeError: # no attribute __len__ - return 1
            yield 1


def lengths(list):
    for item in list:
        try:
            yield len(item)
        except TypeError: # no attribute __len__ - return 1
            yield 1

def before_meth(meth, other):
    '''
    Wrapper that allows a method to call another method 'other' dircetly before
    execution.
    '''
    # wrapper
    @functools.wraps(meth)
    def func(self, *args, **kwargs):
        other(self) # maybe self.other(self)?
        return meth(self, *args, **kwargs)
        return func


def after_meth(meth, other):
    '''
    Wrapper that allows a method to call another method 'other' dircetly after
    execution.
    '''
    # wrapper
    @functools.wraps(meth)
    def func(self, *args, **kwargs):
        rv = meth(self, *args, **kwargs)
        other(self) # maybe self.other(self)?
        return rv
    return func


def constant_input(f):
    '''
    Wrapper used to allow easy conversion from numbers to objects of the class
    'AlgebraicFunction'. Functions with this decorator automaticly convert
    numbers passed as positional arguments to 'Constant'-objects.
    '''
    from numbers import Number
    @functools.wraps(f)
    def func(*args, **kwargs):
        new_args_ls = []
        for arg in args:
            if isinstance(arg, Number):
                arg = Constant(arg)
            new_args_ls.append(arg)
        args = tuple(new_args_ls)
        return f(*args, **kwargs)
    return func


##### Declaration of a Meta-Class to ensure that all functions are defined #####
from abc import ABCMeta

class AlgebraicFunctionMeta(ABCMeta):
    '''
    Metaclass derived from ABCMeta of the 'abc'-package. Used to enforce
    decorator operations so that users do not have to worry about adding
    decorators when defining custom classes derived from AlgebraicFunction.
    '''
    def __new__(metacls, name, bases, namespace, **kwargs):
        result = super().__new__(metacls, name, bases, namespace)
        # to @list_input equivalent expression; all instanciated classes include such a decorator for value now
        result.value = list_input_kwargs(result.value)
        if name == 'AlgebraicFunction':
            result.__abstractmethods__ = {} # very 'bad' workaround to ensure that the constructor of AlgebraicFunction is still callable
        return result

##### Declaration of the abstract class AlgebraicFunction #####################
from abc import abstractmethod

class AlgebraicFunction(metaclass=AlgebraicFunctionMeta):
    '''
    Abstract base class that defines all client level behaviour for all objects
    from classes derived from this class.
    AlgebraicFunctionMeta is used as a metaclass to ensure behaviour of an
    abstract base class using the 'abstractmethod'-decorator from the abc
    package.
    '''
    def __init__(self, strg):
        '''
        Constructor of the class AlgebraicFunction. Currently unusable as
        AlgebraicFunction is abstract.
        Constructs an object of a class derived from AlgebraicFunction by
        parsing the given String using the specified grammar. Note that this
        constructor never creates an object from the class AlgebraicFunction
        itself.
        '''
        af = parse(strg)
        self.__class__ = af.__class__
        self.__dict__ = af.__dict__

    @abstractmethod
    def value(self, **kwargs):
        '''
        Abstract Method that returns a numeric value and is excecuted if the
        class is called.
        '''
        pass

    @abstractmethod
    def derivative(self, char):
        '''
        Abstract Method that always returns the derivate of an object from a
        class derived from AlgebraicFunction.
        '''
        pass

    def simplify(self):
        '''
        Instancemethod that tries to simplify the given object by checking if it
        contains a parameter. Usually invoked by a derived class through
        'super().simplify()' at the start of the overriding method when
        implementing a more specific 'simplify'-Method.

        The 'simplify'-Method changes the class of it's object to an object of
        class Constant if it deems necessary.
        '''
        try:
            c = Constant(self.value())
            self.__class__ = c.__class__
            self.__dict__ = c.__dict__
        except KeyError:
            pass

    @abstractmethod
    def __str__(self):
        '''
        Abstract method that overrides the built-in method '__str__' such that
        a string returned by the method can be reparsed into the same function.
        '''
        pass

    def __call__(self, values):
        '''
        Implementation of the built-in method '__call__' such that calling this
        object is equivalent to invoking the 'value'-method.
        '''
        return self.value(**values)

    @constant_input
    def __add__(self, other):
        '''
        Implementation of the built-in method '__add__' such that the adding
        operation using '+' for two objects of a from AlgebraicFunction derived
        class returns a new Addition object with the two objects passed to the
        constructor.
        '''
        return Addition(self, other)

    @constant_input
    def __sub__(self, other):
        return Subtraction(self, other)

    @constant_input
    def __mul__(self, other):
        return Multiplication(self, other)

    @constant_input
    def __truediv__(self, other):
        return Division(self, other)

    @constant_input
    def __pow__(self, other):
        return PowerFunction(self, other)


##### Declaration of the abstract Branch Classes ###############################

# Class that represents binary Operators
class LinkingFunction(AlgebraicFunction):

    def __init__(self, link1, link2, char):
        self.link1 = link1
        self.link2 = link2
        self.linking_operator = char

    @abstractmethod
    def value(self, **kwargs):
        pass

    @abstractmethod
    def derivative(self, char):
        pass

    def simplify(self):
        print(f'simplifying {type(self)}')
        print('l1 ', self.link1)
        self.link1.simplify()
        print('l2 ', self.link2)
        self.link2.simplify()
        print(super().simplify)
        super().simplify()
    # def simplify(self):
    #     v = self.val

    def __str__(self):
        return "(" + str(self.link1) + self.linking_operator + str(self.link2) + ")"


# Class that represents unitary Operators
class CalculationFunction(AlgebraicFunction):

    def __init__(self, func, str):
        self.func = func
        self.calculation_operator = str

    @abstractmethod
    def value(self, **kwargs):
        pass

    @abstractmethod
    def derivative(self, char):
        pass

    def simplify(self):
        self.func.simplify()
        super().simplify()

    def __str__(self):
        return self.calculation_operator + "(" + str(self.func) + ")"


##### Begin Leaf Class Declarations ############################################

class Parameter(AlgebraicFunction):

    def __init__(self, char):
        self.char = char

    def value(self, **kwargs):
        try:
            return kwargs[self.char]
        except KeyError:
            raise KeyError(f'Couldn\'t assign a value to {self.char}')

    def derivative(self, char):
        if(self.char == char):
            return Constant(1)
        else:
            return Constant(0)

    def simplify(self):
        pass

    def __str__(self):
        return str(self.char)


class Constant(AlgebraicFunction):

    def __init__(self, c):
        self.c = c

    def value(self, **kwargs):
        return self.c

    def derivative(self, char):
        return Constant(0)

    def simplify(self):
        pass

    def __str__(self):
        return str(self.c)


##### Begin BinaryOperator Class Declations ####################################

class Addition(LinkingFunction):

    def __init__(self, link1, link2):
        super().__init__(link1, link2, "+")

    def value(self, **kwargs):
        return self.link1.value(**kwargs) + self.link2.value(**kwargs)

    def derivative(self, char):
        return self.link1.derivative(char) + self.link2.derivative(char)


class Multiplication(LinkingFunction):

    def __init__(self, link1, link2):
        super().__init__(link1, link2, "*")

    def value(self, **kwargs):
        return self.link1.value(**kwargs) * self.link2.value(**kwargs)

    def derivative(self, char):
        return self.link1.derivative(char) * self.link2 + self.link1 * self.link2.derivative(char)


class PowerFunction(LinkingFunction):

    def __init__(self, link1, link2):
        super().__init__(link1, link2, "**")

    def value(self, **kwargs):
        return math.pow(self.link1.value(**kwargs), self.link2.value(**kwargs))

    def derivative(self, char):
        return self.link1**self.link2 * (Logarithm(self.link1) * self.link2.derivative(char) + self.link2 * self.link1.derivative(char) / self.link1)


class Subtraction(Addition):

    def __init__(self, link1, link2):
        super().__init__(link1, Constant(-1) * link2)

    def __str__(self):
        return "(" + str(self.link1) + "-" + str(self.link2) + ")"


class Division(Multiplication):

    def __init__(self, link1, link2):
        super().__init__(link1, ExponentialFunction(Constant(-1) * Logarithm(link2)))

    def __str__(self):
        return "(" + str(self.link1) + "/" + str(self.link2) + ")"


##### Begin UnitaryOperator Class Declations ###################################

class IdentityFunction(CalculationFunction):

    def __init__(self, func):
        super().__init__(func, "id")

    def value(self, **kwargs):
        return self.func.value(**kwargs)

    def derivative(self, char):
        return self.func.derivative(char)


class ExponentialFunction(CalculationFunction):

    def __init__(self, func):
        super().__init__(func, "exp")

    def value(self, **kwargs):
        return math.exp(self.func.value(**kwargs))

    def derivative(self, char):
        print(f'inner: {self.func.derivative(char)}')
        return self * self.func.derivative(char)


class Logarithm(CalculationFunction):

    def __init__(self, func):
        super().__init__(func, "log")

    def value(self, **kwargs):
        v = self.func.value(**kwargs)
        if v == 0: # 0 undefined
            return float('NaN')
        else:
            return math.log(v)

    def derivative(self, char):
        return self.func.derivative(char) / self.func


class TrigonometricFunction(CalculationFunction):

    def value(self, **kwargs):
        return self.func.value(**kwargs)

    def derivative(self, char):
        return self.func.derivative(char)


class SinFunction(TrigonometricFunction):

    def __init__(self, func):
        super().__init__(func, "sin")

    def value(self, **kwargs):
        return math.sin(self.func.value(**kwargs))

    def derivative(self, char):
        return CosFunction(self.func) * self.func.derivative(char)


class CosFunction(TrigonometricFunction):

    def __init__(self, func):
        super().__init__(func, "cos")

    def value(self, **kwargs):
        return math.cos(self.func.value(**kwargs))

    def derivative(self, char):
        return constant(-1) * SinFunction(self.func) * self.func.derivative(char)


class TanFunction(TrigonometricFunction):

    def __init__(self, func):
        super().__init__(func, "tan")

    def value(self, **kwargs):
        v = self.func.value(**kwargs)
        if math.abs(v) % math.pi/2 <= _min_accuracy:
            return float('NaN')
        return math.tan(v)

    def derivative(self, char):
        return (SinFunction(self.func) / CosFunction(self.func)).derivative(char)


class SquareRoot(CalculationFunction):

    def __init__(self, func):
        super().__init__(func, 'sqrt')

    def value(self, **kwargs):
        v = self.func.value(**kwargs)
        return math.sqrt(v)

    def derivative(self, char):
        return PowerFunction(func, 0.5).derivative(char)



def parse(s):
    return Parser(s).parse()


##### Parser-Class that uses a Lexer to interpret a String into a function object #####

class Parser:

    # expr -> statement
    # expr -> expr (op expr)*
    # statement -> num
    # statement -> parameter
    # statement -> func statement
    # statement -> LPAREN expr RPAREN

    def __init__(self, strg=None, lexer=None):
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
            raise TypeError(f'Bad Input: expected {class_type} and got {self.curr_token[0]}')

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


##### Lexer-Class to interpret a String to tokens of a given grammar ###########

class Lexer:

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

    def __next__(self):
        # print('next')
        self.pos += 1

        if self.pos <= len(self.tokens):
            return self.tokens[self.pos - 1]
        else:
            raise StopIteration

    def __iter__(self):
        return self

    def __str__(self):
        strg = 'Lexer:\n'
        for index, token in enumerate(self.tokens):
            if index == self.pos:
                strg += '>'
            strg += f'\t{token}\n'
        return strg[:-1]


# method that creates a list of tokens according to the induced grammar of the initialized parameters
def tokenize_string(strg):
    # strg = strg.replace(' ', '')
    tokens = []
    regex = '('
    for op in sorted(all_escaped_operators(), key=len)[::-1]:
        regex += op + '|'
    regex += '[a-z]|[A-Z]|[0-9]+\.[0-9]+|\.[0-9]+|[0-9]+\.|[0-9]+)'
    regex.replace(' ', '')
    pattern = re.compile(r'' + regex)
    for match in pattern.finditer(strg):
        span = match.span()
        token = token_class_type(strg[span[0]:span[1]])
        tokens.append(token)
    return tokens


# method that maps all identifiers to an according token of the form (class_type, identifier) according to the initialized parameters
def token_class_type(identifier):
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


# returns a list of all the declared Operators with by ReGEx-Convention escaped Operators
def all_escaped_operators():
    ls = []
    for brackets in bracket_operators:
        for op in brackets:
            ls.append(escape_string_regex(op))
    for key in linking_operator_dict:
        ls.append(escape_string_regex(key))
    for key in calculation_operator_dict:
        ls.append(escape_string_regex(key))
    return ls


# escapes all characters of a string that has to be escaped by ReGEx-Convention
def escape_string_regex(strg):
    rv_strg = ''
    for char in strg:
        c = escape_char_regex(char)
        rv_strg += escape_char_regex(char)
    return rv_strg


# escapes a single character if necessary using the ReGEx-Convention
def escape_char_regex(char):
    if char in _regex_must_be_escaped:
        return '\\' + char
    else:
        return char


###### Vital constants for runtime computation - not to be changed #############

_regex_must_be_escaped = ['.', '^', '$', '*', '+',
                          '-', '?', '(', ')', '{',
                          '}', '\\', '[', ']']
_min_accuracy = 1e-5

##### Changeable Parameters for advanced Portability ###########################

# operators in the first set define an open parenthesis and the ones in the second set define closing parenthesis
bracket_operators = ({"(", "["},  {")", "]"})

calculation_operator_dict = {
    "exp": ExponentialFunction,
    "log": Logarithm,
    "sin": SinFunction,
    "cos": CosFunction,
    "tan": TanFunction
}

linking_operator_dict = {
    "+": Addition,
    "-": Subtraction,
    "*": Multiplication,
    "/": Division,
    "**": PowerFunction
}

# every operator in the same set has equal importance and left sets have lesser importance than right ones
linking_operator_order = [{"+", "-"}, {"*", "/"}, {"**"}]


##### Sanity checks for changeable Parameters ##################################

# checking if all binary operators have a defined order of operation
for key in linking_operator_dict:
    for set in linking_operator_order:
        if key in set:
            break
    else:
        raise TypeError(f'Order of operation for \"{key}\" not defined.')

# checking if only binary operators have a defined order or operation
len_loo = 0
for order_set in linking_operator_order:
    len_loo += len(order_set)
if len(linking_operator_dict) != len_loo:
    raise TypeError(
        "Every linking-operator needs a defined order of operation (left to right).")

# checking if all structural operators have a defined counterpart (e.g. '(' and ')' )
if len(bracket_operators[0]) != len(bracket_operators[1]):
    raise TypeError(
        "Every bracket-operator needs corresponding Start- and End-Operand")

# checking if no single operator references two functionalities
...
# checking if all referenced classes are defined
...


##### Test-Module ##############################################################

def test():
    f = AlgebraicFunction('3+x')
    print(type(f))
    # afs = [  parse('x+y'),
    #         parse('x-y'),
    #         parse('x*y'),
    #         parse('x/y'),
    #         parse('x**y')  ]
    # x = y = [0,1.001]
    # for af in afs:
    #     af.value(x=x, y=y)

    ## test dict_list ##
    # d = {'x':[1,3], 'y':[2,4,6], 'z':3}
    # print(dict_list(d))




    # print(af)
    # af = parse('exp(x**2)')
    # ls = [af]
    # print(ls[-1].value(x=1))
    # for i in range(5):
    #     ls.append(ls[-1].derivative('x'))
    #     print(ls[-1].value(x=2.5))
    pass

if __name__ == '__main__':
    test()


##### End algebraicFunction.py ################################################
