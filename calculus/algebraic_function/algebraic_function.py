##### begin algebraic_function.py ################################################
from abc import abstractmethod

from .algebraic_function_meta import AlgebraicFunctionMeta
from .decorators import constant_input

##### Declaration of the abstract class AlgebraicFunction ######################

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

# To ensure that every package has AlgebraicFunction available the class is
#   declared while executing module code before importing further modules that
#   are necessary while running the code.
from .parser import parse
from .algebraic_function_classes import Addition, Subtraction, Multiplication, Division, PowerFunction
##### end algebraic_function.py ################################################
