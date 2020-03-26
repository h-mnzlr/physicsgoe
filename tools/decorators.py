##### begin decorators.py ######################################################
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

##### end decorators.py ########################################################
