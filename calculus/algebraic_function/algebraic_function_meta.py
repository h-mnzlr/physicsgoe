##### begin algebraic_function_meta.py #########################################
from abc import ABCMeta


from .decorators import list_input_kwargs

##### Declaration of a Meta-Class to ensure that all functions are defined #####


class AlgebraicFunctionMeta(ABCMeta):
    '''
    Metaclass derived from ABCMeta of the 'abc'-package. Used to enforce
    decorator operations so that users do not have to worry about adding
    decorators when defining custom classes derived from AlgebraicFunction.
    '''
    def __new__(metacls, name, bases, namespace, **kwargs):
        result = super().__new__(metacls, name, bases, namespace)
        # to @list_input equivalent expression; all instanciated classes include such a decorator for value now
        # result.value = list_input_kwargs(result.value)
        if name == 'AlgebraicFunction':
            result.__abstractmethods__ = {} # very 'bad' workaround to ensure that the constructor of AlgebraicFunction is still callable
        return result


##### end algebraic_function_meta.py #########################################
