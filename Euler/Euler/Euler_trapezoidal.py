from sympy import symbols, Function, lambdify
from sympy.parsing.sympy_parser import parse_expr
import NewtonRaphson as NR

def trapezoidal(f, x0:float, y0:float, xn:float, h:float):
    """
    Trapezoidal formula (Modified Euler formula): 
        `y(x + h) = y(x) + (f(x, y(x)) + f(x + h, y(x + h)))*h/2`
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
        yi  = NR.NRmethod(lambdify(y, y-(h/2)*(f(xi, y)+f(x0+h*i, yi))-yi, modules="sympy"), y, yfw)
        #yi  = yi + (h/2)*(f(xi, yfw) + f(x0+h*i, yi))
        x_list.append(xi)
        y_list.append(yi)

    return x_list, y_list

def main() -> None:
    pass

if __name__ == '__main__':
    main()