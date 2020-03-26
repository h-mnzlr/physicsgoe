##### begin algebraic_function_classes.py ######################################
from abc import abstractmethod


from .algebraic_function import AlgebraicFunction

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


###### Vital constants for runtime computation #################################
_min_accuracy = 1e-5


##### end algebraic_function_classes.py ########################################
