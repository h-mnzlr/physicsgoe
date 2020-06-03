# -*- coding: utf-8 -*-
""".

This module uses a metaclass to enforce backend functionality to classes
derived from the 'AlgebraicFunction'-class that is used as the frontend
interface. The module implements automatic decorator-operations and
automatic function creations to minimize code in the '
algebraic_function_grammar'-module as that this module can be considered a
semi-frontend interface as well. It should provide users with the ability to
define their own classes without worrying about backend functionality.


"""

# begin algebraic_function_meta.py - importing necessary modules
from abc import ABCMeta
from .decorators import list_input_kwargs


# Declaration of a Meta-Class to ensure that all functions are defined
class AlgebraicFunctionMeta(ABCMeta):
    """
    Enforce functionality on all classes derived from AlgebraicFunction.

    Module level metaclass derived from the'ABCMeta'-class from the abc
    package. Used as the metaclass for the frontend abstract interface class
    'AlgebraicFunction'. Provides backend functionalities to every class
    derived from 'AlgebraicFunction' to make defining such classes more enduser
    friendly.
    """

    def __new__(metacls, name, bases, namespace, **kwargs):
        """."""
        result = super().__new__(metacls, name, bases, namespace)
        # to @list_input equivalent expression; all instanciated classes
        # include such a decorator for value now.
        #
        # result.value = list_input_kwargs(result.value)
        if name == 'AlgebraicFunction':
            result.__abstractmethods__ = {}  # very 'bad' workaround to ensure
            # that the constructor of AlgebraicFunction is still callable
        return result


# end algebraic_function_meta.py
