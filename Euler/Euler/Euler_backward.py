from sympy import symbols, Function, lambdify
from sympy.parsing.sympy_parser import parse_expr
import NewtonRaphson as NR

def backward(f, x0:float, y0:float, xn:float, h:float):
    """
    Backward Euler formula (Implicit Euler formula): 
        `y(x + h) = y(x) + h*f(x + h, y(x + h))`
    
    """
    x_list = [x0]
    y_list = [y0]
    xi = x0
    yi = y0
    n  = int((xn - x0)/h)

    for i in range(n):
        yfw = yi + h*f(xi, yi)
        xi  = x0 + h*(i+1)
        y   = symbols('y')
        yi  = NR.NRmethod(lambdify(y, y-h*f(xi, y)-yi, modules="sympy"), y, yfw)
        #yi = yi + h*f(xi, yfw)
        x_list.append(xi)
        y_list.append(yi)

    return x_list, y_list

def main() -> None:
    pass

if __name__ == '__main__':
    main()
