##### begin algebraic_function_grammar.py ######################################


from . import algebraic_function_classes as clss

##### Changeable Parameters for advanced Portability ###########################

# operators in the first set define an open parenthesis and the ones in the second set define closing parenthesis
bracket_operators = ({"(", "["},  {")", "]"})

calculation_operator_dict = {
    "exp": clss.ExponentialFunction,
    "log": clss.Logarithm,
    "sin": clss.SinFunction,
    "cos": clss.CosFunction,
    "tan": clss.TanFunction
}

linking_operator_dict = {
    "+": clss.Addition,
    "-": clss.Subtraction,
    "*": clss.Multiplication,
    "/": clss.Division,
    "**": clss.PowerFunction
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


##### end algebraic_function_grammar.py ########################################
