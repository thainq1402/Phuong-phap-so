# Central interpolation - Developed by Le Nguyen Bach - CTTN MI K64 

from termcolor       import colored        
from math            import *
from sympy           import *

import matplotlib.pyplot as plt
import numpy             as np
import sys 

EPSILON_SYS = 1e-15 
MAX_n       = 2

def setattribute(func): 
    attribute_name = '_attr_' + func.__name__

    @property
    def _wrapper(self):
        if not hasattr(self, attribute_name):
            setattr(self, attribute_name, func(self))  # Create instance attribute.

        return getattr(self, attribute_name)

    return _wrapper

def timer(func):
    from termcolor import colored
    import time 

    def __wrapper(*args, **kwargs):
        start_time = time.time() 

        result = func(*args, **kwargs)

        end_time = time.time() 
        run_time = (end_time - start_time) * 1000

        print(f"\nTotal runtime of {func.__name__}() is {run_time} ms")
        
        return result

    return __wrapper



class Central_interpolation:
    def __init__(self, table_x, table_y, value_x, formula):
        self.table_x = table_x
        self.table_y = table_y
        self.value_x = value_x
        self.formula = formula

        self.h = table_x[1] - table_x[0] # Jump step

        self.switch = {
            "Stirling" : 0,
            "Bessel"   : 1
        }.get(formula)  # Mystery constant Ψ(￣∀￣)Ψ VERY IMPORTANT!!

        self.init_index = round((value_x - table_x[0]) / self.h - 0.5 * self.switch)                    # round() if 0 else int()  
        self.n          = min(len(table_x) - self.init_index - self.switch - 1, self.init_index, MAX_n) # Maximum number of data point in Stirling is 5, Bessel is 6
        self.value_t    = (value_x - table_x[self.init_index]) / self.h - self.switch / 2

    @classmethod 
    def fromFileInput(cls):
        fileI = open("D:\Download\Input.txt", "r")

        table_x = list(map(float, fileI.readline().split()))
        table_y = list(map(float, fileI.readline().split()))
        value_x = float(fileI.readline()) 
        formula = str(fileI.readline()).strip()
        
        if len(table_x) == 0 or len(table_x) == 1:
            colored("xTableSizeError: xTable doesn't have enough element", 'red')
            sys.exit() 
        
        condition_xJumpStep   = True 
        condition_xIncreasing = True 
        
        h = table_x[1] - table_x[0]
        
        for i in range(len(table_x) - 1):
            d = table_x[i + 1] - table_x[i]
        
            if d <= 0:
                condition_xJumpStep = False
                break 
        
            elif abs(d  - h) > EPSILON_SYS:
                condition_xIncreasing = False 
                break  
        
        condition_yTableSize = len(table_y) == len(table_x) 
        condition_xValue     = value_x >= table_x[0] and value_x <= table_x[-1]
        condition_Name       = formula == "Stirling" or formula == "Bessel" 
        
        condition_error = {
            condition_Name        : colored("NameError: Please type Stirling or Bessel correctly"                                              , 'red'),
            condition_xValue      : colored("RangeError: xValue out of range"                                                                  , 'red'),
            condition_yTableSize  : colored(f"TableSizeError: xTable has {len(table_x)} element(s), while yTable has {len(table_y)} element(s)", 'red'),
            condition_xIncreasing : colored("xIncreasingError: xTable must have increasing value from left to right"                           , 'red'),
            condition_xJumpStep   : colored("xJumpStepError: Distance between two consecutive value are not the same"                          , 'red'),       
        }.get(False) 
        
        if condition_error == None:
            return cls(table_x, table_y, value_x, formula) 
        else:
            print(condition_error)
            sys.exit() 

    @staticmethod
    def __add(arr_2D, new_value):
        if len(arr_2D[0]) == 0:
            return [[new_value]]
        
        arr_2D.insert(0, [new_value]) # Add new_value to the top 
        
        for i in range(1, len(arr_2D)):
            new_element = arr_2D[i - 1][i - 1] - arr_2D[i][i - 1] 
            arr_2D[i].append(new_element)

        return arr_2D 

    @setattribute
    def __differenceTable(self):
        table_y  = self.table_y
        n        = self.n
        switch   = self.switch 
        init_index = self.init_index
       
        dt          = [[]] # dt is short for "difference table"
        index_range = range(init_index - n, init_index + n + 1 + switch) 
        
        for index in index_range:
            dt = self.__add(dt, table_y[index])

        return dt

    @setattribute
    def __coeff(self):
        n      = self.n
        switch = self.switch  
        coeff  = np.identity(n + switch) # Create an idenity matrix, size m x m

        # Put the correct number at the below triangle
        for i in range(1, n + switch):
            coeff[i] = np.add(
                [-x * (i - switch / 2) ** 2 for x in coeff[i - 1]],
                np.roll(coeff[i - 1], 1)
            )
        
        return coeff

    @setattribute
    def __tHat(self):
        switch = self.switch
        n      = self.n
        t      = symbols("t")

        tHat_odd = np.full((n + switch, 1), t ** (1 - switch))
        for i in range(n - 1 + switch):
            tHat_odd[i + 1][0] = tHat_odd[i][0] * t * t

        tHat_even = [[i[0] * t] for i in tHat_odd]

        return [tHat_even, tHat_odd]   

    @setattribute
    def __yHatT(self):
        switch = self.switch 
        n      = self.n 
        dt     = self.__differenceTable
        
        yHatT_even = [[]]
        yHatT_odd  = [[]]

        for i in range(n + switch):
            even_element = dt[-1 - i][-1 - i] / factorial(2 * (n - i) + switch)
            odd_element  = 0.5 * (dt[-1 - i][-2 - i] + dt[-2 - i][-1 - i]) / factorial(2 * (n - i) - 1 + switch) 
        
            yHatT_even[0].insert(0, even_element) 
            yHatT_odd[0].insert(0, odd_element)

        return [yHatT_even, yHatT_odd]

    @setattribute
    def __error(self): 
        value_t = self.value_t
        switch  = self.switch  
        t_sq    = value_t * value_t # Just t^2, nothing special :) 
        n       = self.n 
        
        dt = self.__differenceTable
        n  = self.n  
        error = dt[-1][-1] / factorial(2 * n + switch) / (1 +  value_t * (1 - switch)) 

        for i in range(n + 1):
            error *= (t_sq - (i + switch / 2) ** 2)
        
        return abs(error) 

    @setattribute
    def interpolatingPolynomial(self):
        switch     = self.switch 
        table_y    = self.table_y 
        init_index = self.init_index
        coeff      = self.__coeff
        yHatT_even = self.__yHatT[0]
        yHatT_odd  = self.__yHatT[1]
        tHat_even  = self.__tHat[0]
        tHat_odd   = self.__tHat[1]

        y0 = table_y[init_index]
 
        polynomial_t_expr = y0 * (1 - switch) +  np.add(yHatT_odd @ coeff @ tHat_odd,yHatT_even @ coeff @ tHat_even)[0][0]      
        
        return polynomial_t_expr 

    
    def getResult(self):
        h               = self.h
        switch          = self.switch
        table_x         = self.table_x  
        value_x         = self.value_x 
        value_t         = self.value_t
        error           = self.__error
        init_index      = self.init_index
        polynomial_expr = self.interpolatingPolynomial

        x0 = table_x[init_index]
        t  = symbols("t")
        
        polynomial_eval = lambdify(t, polynomial_expr, "math") 

        fileO = open("D:\Download\Output.txt", "w")

        fileO.write("Interpolating polynomial\n")
        fileO.write(f"P(t) = {polynomial_expr}\n")
        fileO.write(f"where t = {1 / h}x - {x0 / h + 0.5 * switch}\n\n")
        fileO.write("Result:\n")
        fileO.write(f"y({value_x}) = {polynomial_eval(value_t)} ± {error}")

        

    def computeOnly(self):
        polynomial_t_expr = self.interpolatingPolynomial
        value_t           = self.value_t 

        polynomial_t_eval = lambdify(symbols("t"), polynomial_t_expr, "math")

        return polynomial_t_eval(value_t) 


def main():
    user = Central_interpolation.fromFileInput()
    user.getResult()
    # print(user.computeOnly()) 

if __name__ == '__main__':
    main() 

