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
    from string import ascii_letters
    nums = [1, .1] # TODO: implement complex numbers, 1+.1j

    def test_creation(self):
        '''Testing creation of AlgebraicFunction instances'''
        from physicsgoe.calculus.algebraic_function.algebraic_function_grammar import linking_operator_dict, calculation_operator_dict, bracket_operators
        for num in self.nums:
            self.assertEqual(type( self.af.AlgebraicFunction(f'{num}') ), self.af.Constant)
        for letter in self.ascii_letters:
            self.assertEqual(type( self.af.AlgebraicFunction(f'{letter}') ), self.af.Parameter)
        for op, item in linking_operator_dict.items():
            self.assertEqual(type( self.af.AlgebraicFunction(f'1{op}1') ), item)
        for op, item in calculation_operator_dict.items():
            for l_par, r_par in zip(bracket_operators[0], bracket_operators[1]):
                self.assertEqual(type( self.af.AlgebraicFunction(f'{op}{l_par}x{r_par})') ), item)

    # def test_values(self):
    #     self.assertTrue(True)

class TestAlgebraicFunctionMeta(unittest.TestCase):
    import physicsgoe.calculus.algebraic_function.algebraic_function_meta as af_meta


class TestParsingAF(unittest.TestCase):
    import physicsgoe.calculus.algebraic_function.parser as parser


class TestLexerAF(unittest.TestCase):
    import physicsgoe.calculus.algebraic_function.lexer as lexer


class TestGrammarAF(unittest.TestCase):
    import physicsgoe.calculus.algebraic_function.algebraic_function_grammar as grammar

    def test_op_order(self):
        '''Testing every operator for defined order of operation'''
        for key in self.grammar.linking_operator_dict:
            for set in self.grammar.linking_operator_order:
                if key in set:
                    break
            else:
                self.fail(f'Order of operation for \"{key}\" not defined.')




##### END test_algebraic_function.py ###########################################
