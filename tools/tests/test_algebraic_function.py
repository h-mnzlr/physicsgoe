##### BEGIN test_algebraic_function.py #########################################
'''
Implements 'TestCase'-Classes for all modules from 'algebraic_function'.

## TODO: Documentation
This module assumes the 'test_pkg'-modules runs without problems.
'''
##### importing necessary modules ##############################################
import unittest

##### BEGIN classes
class TestAlgebraicFunction(unittest.TestCase):
    import physicsgoe.calculus.algebraic_function.algebraic_function as af

    def test_creation(self):
        from physicsgoe.calculus.algebraic_function.algebraic_function_grammar import linking_operator_dict
        for op, item in linking_operator_dict.items():
            self.assertTrue(self.af.AlgebraicFunction(f'1{op}1'), item)

    # def test_values(self):
    #     self.assertTrue(True)

class TestAlgebraicFunctionMeta(unittest.TestCase):
    import physicsgoe.calculus.algebraic_function.algebraic_function_meta as af_meta


class TestAlgebraicFunctionClasses(unittest.TestCase):
    import physicsgoe.calculus.algebraic_function.algebraic_function_classes as af_clss


class TestParsingAF(unittest.TestCase):
    import physicsgoe.calculus.algebraic_function.parser as parser


class TestLexerAF(unittest.TestCase):
    import physicsgoe.calculus.algebraic_function.lexer as lexer


class TestGrammarAF(unittest.TestCase):
    import physicsgoe.calculus.algebraic_function.algebraic_function_grammar as grammar
