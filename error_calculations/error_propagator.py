##### Begin fehlerrechnung.py - importing necessary modules ####################

import algebraic_function as af


##### Struktur-Methoden ########################################################
import functools

def dict_input_args(f):
    '''
    Wrapper that allows functions that only accepts dictionaries of singular
    values as positional arguments through '*args' to return a list of
    functioncalls of the given function.
    '''
    @functools.wraps(f)
    def func(*args, **kwargs):
        # reorder all dictionaries of lists to lists of dictionaries
        arg_lists = []
        for arg in args:
            try:
                arg_lists.append( af.dict_list(arg) )
            except NotImplementedError: # arg is not a dict
                arg_lists.append( arg )

        # iterate over the arguments in the list and select arguments for a function call
        rv_ls = []
        lengths = af.lengths(arg_lists)
        for i in range(max(lengths)):
            args = []
            for index, arg in enumerate(arg_lists):
                try:
                    args.append(arg[i])
                except IndexError: # Index out of bounds - using last element
                    args.append( arg[ lengths[index]-1 ])
                except TypeError:  # arg not subscribtable - using the element without indexing
                    args.append(arg)

            # cast arg_list to tuple and call function
            args = tuple(args)
            rv_ls.append( f(*args, **kwargs) )

        return rv_ls
    return func


def dict_test(f):
    '''
    test_wrapper
    '''
    @functools.wraps(f)
    def func(*args, **kwargs):
        print(args, kwargs)
        print(type(args), type(kwargs))
        return f(*args, **kwargs)
    return func


##### Schnittstellen Klasse ####################################################

class Fehlerrechner:
    '''
    Class that provides a dynamic API-object to calculate and display different
    ways to propagate errors. No instances of this class should be created.
    API interface:
    'set_func(strg)': taking a string as an argument the method parses that
    string to an 'algebraic_function'-object that defines the mathematical
    operation.
    'set_values(values/**kwargs)': This method is used to input the values of
    a physical quantity. Values should usually be passed as keyword arguments
    (eg. : set_values(x=x_list, y=y_list) ); but can also be passed as a regular
    dictionary or as just lists. Whenever a list is passed as a positional
    argument it is matched to the parameter-string that first appears in the
    string passed to 'set_func'. If 'set_func' has not been invoked yet a
    NotImplementedError is invoked.
    'set_errors(values/**kwargs)': Similar to 'set_values' in usage and
    implementation being passed the error margins of a physical quantity. Errors
     are always passed witch the same key as their
    counterpart values.
    '''
    # public classmethods
    @classmethod
    def set_func(self, strg):
        '''
        Classmethod to parse a given string into an 'algebraic function'-object.
        The parsing process is called explicitly as that the order of the
        parameters can be extracted when the string is tokenized using the
        lexer.
        Should parsing fail at any point a TypeError is raised.
        '''
        try:
            lexer = af.Lexer(strg=strg)
            self.parameters = lexer.parameter_list()
            parser = af.Parser(lexer=lexer)
            self.func = parser.parse()
        except:
            self._error(TypeError, 'Parsing failed')

    @classmethod
    def set_values(self, values=None, **kwargs):
        if values:
            if isinstance(values, dict):
                self._set_dict(values, 'values')
            elif isinstance(values, list):
                self._set_lists(values, 'values')
        else:
            self._set_dict(kwargs, 'values')

    @classmethod
    def set_errors(self, errors=None, **kwargs):
        if errors:
            if isinstance(errors, dict):
                self._set_dict(errors, 'errors')
            elif isinstance(errors, list):
                self._set_lists(errors, 'errors')
        else:
            self._set_dict(kwargs, 'errors')

    # private classmethods
    @classmethod
    def _set_dict(self, dict, name):
        '''
        Classmethod to update the value of a dictionary called $name of the
        class-object using the passed dict variable.
        '''
        try:
            dict_old = getattr(self, name)
        except AttributeError: # attribute self.$name not found
            dict_old = {}
        try:
            dict_old.update(dict)
        except TypeError: # variable dict does not hold a compatible type
            self._error(TypeError, 'Input cannot be converted to a dictionary.')
        setattr(self, name, dict_old)

    @classmethod
    def _set_lists(self, lists, name):
        '''
        Classmethod to convert values passed as lists to a dict which values can
        be stored using the private '_set_dict' method. Values are interpreted
        in the fixed order induced by the given function (first parameter to
        first values etc.).
        If the program cannot find a way to express the order of the parameters
        a NotImplementedError is raised.
        '''
        if not self.parameters: # Error if there is no parameter list to match values to.
            self._error(NotImplementedError, 'When Values are passed via list input a function needs to be specified first.')
        dict = {}
        for parameter, list in zip(self.parameters, lists):
            dict[parameter] = list
        self._set_dict(dict, name)

    @classmethod
    def _error(self, error_class, error_strg=None):
        raise error_class(error_strg)


##### Schnittstellen Funktionen ################################################
import math

def error_prapagation_func(func, values):
    error_func = 0
    for key in values:
        der = func.derivative(key)
        error_func = (af.Parameter(f'{key}_err')*der)**2 + error_func
    return af.SquareRoot(error_func)


@dict_input_args
def error_propagation(func, values, errors):
    '''
    Function that is used to calculate error margins for an error propagation
    when calculating the value of the passed function 'func' using the Gauß law
    for error propagation.
    Values and errors are accepted as dictionaries, where the string name of the
    parameter encodes the corresponding numerical value.
    With the given decorator the function also is able to accept dictionaries
    that encode lists as input. The return value is then a list of solutions.
    '''
    sum = 0
    for key in values:
        der = func.derivative(key)
        sub = der( values )*errors[key]
        sum += sub*sub
    return func(values), math.sqrt(sum)


@dict_input_args
def error_propagation_cov(func, values, cov_dict):
    '''
    Function that is used to calculate error margins for an error propagation
    when calculating the values of the passed function using the covariances
    for correlated parameters.
    '''
    outer = 0
    for key1 in values:
        inner = 0
        der1 = func.derivate(key1)
        for key2 in values:
            der2 = func.derivate(key2)
            inner += cov_dict[key1][key2]*math.abs( der1(values)*der2(values) )
        outer += inner
    return func(values), math.sqrt(outer)


##### ifmain and Test-Module ###################################################

def main():
    f = af.parse('x+y')
    # print(f(x=[0,1], y=[2,4]))
    # fr = Fehlerrechner(strg='x+y', values=[[0,1],[2,3]], errors=[[0.1, 0.1], [0.2, 0.3]])
    # print(fr.__dict__)


    # test error_propagation() ##
    # values = {'x':[1,3], 'y':[3,5]}
    # errors = {'x':[0.1,0.2], 'y':[0.2,0.4]}
    # print(error_propagation(f, values, errors))

    import numpy as np
    x_data = np.array([1,3])
    y_data = np.array([3,5])
    x_err = np.array([.1,.2])
    y_err = np.array([.2,.4])
    values = {'x':x_data, 'y':y_data}
    errors = {'x':x_err, 'y':y_err}
    for val in error_propagation(f, values, errors):
        print(val)
        print(type(val[1]))

    err_f = error_prapagation_func(f, values)
    print(err_f)

    # values = {'x':[1, 2], 'y':[4, 3]}
    # errors = {'x':[0.1, 0.1], 'y':[0.2, 0.4]}
    # print(error_propagation(f, values, errors))

    ## test Fehlerrechner-Class ##
    # Fehlerrechner.set_func('x+y')
    # Fehlerrechner.set_values([[1,2],[2,3]])
    # Fehlerrechner.set_errors([[.1,.2],[.2,.3]])
    #
    # Fehlerrechner.set_values({'x':[1,2], 'y':[2,3]})
    # Fehlerrechner.set_errors({'x':[.1,.2], 'y':[.2,.3]})
    #
    # Fehlerrechner.set_values(z=[1,2], y=[2,3])
    # Fehlerrechner.set_errors(x=[.1,.2], y=[.2,.3])
    # print(Fehlerrechner.__dict__)

    # import numpy as np
    # x_data = np.array([1,3])
    # y_data = np.array([3,5])
    # x_err = np.array([.1,.2])
    # y_err = np.array([.2,.4])
    # f = Fehlerrechner
    # f.set_values(x=x_data, y=y_data)
    # f.set_errors(x=x_err, y=y_err)




if __name__ == '__main__':
    main()


##### End fehlerrechnung.py ####################################################
