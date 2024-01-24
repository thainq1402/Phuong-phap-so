from sympy import symbols, lambdify, diff
from sympy.parsing.sympy_parser import (standard_transformations, implicit_multiplication_application,convert_xor,parse_expr)

ACC = 8

def NRmethod(f, x, x0):
    df = lambdify(x, diff(f(x), x), modules="sympy")

    x_check = round(x0, ACC)
    xi = x0 - f(x0)/df(x0)
    while round(xi, ACC) != x_check:
        x_check = round(xi, ACC)
        xi = xi - f(xi)/df(xi)
    
    return round(xi, ACC)
    
def main() -> None:
    x = symbols('x')
    f_input = parse_expr(input("f(x) = "), transformations=(standard_transformations + (implicit_multiplication_application, convert_xor)))
    f = lambdify(x, f_input, modules="sympy")
    x0 = float(input("x0 = "))
    answer = NRmethod(f, x, x0)
    print(answer)

if __name__ == '__main__':
    main()