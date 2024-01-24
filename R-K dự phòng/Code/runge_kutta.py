from sympy                      import lambdify, symbols
from sympy.parsing.sympy_parser import (standard_transformations,
    implicit_multiplication_application,convert_xor,parse_expr)
from matplotlib                 import pyplot as plt
from typing                     import Iterable, List
from itertools                  import cycle
from math                       import fsum
import numpy                    as np
import os

transform = (standard_transformations+(implicit_multiplication_application,convert_xor))
_________ = lambda ____: {k:(v.pop(),[_.pop(0) for _ in v],v) for k,v in ____.items()}
this_dir  = os.path.dirname(os.path.abspath(__file__))
if not os.path.isdir(this_dir+os.sep+'output'): os.mkdir(this_dir+os.sep+'output')

RESET, GREEN, YELLOW = "\033[0m", "\033[0;32m", "\033[0;33m"

BUTCHER_TABLEAU = _________({
    'RK1 Euler': [
        [0  ,],
            (1   ,),
    ],
    'RK2 Heun' : [
        [0  ,],
        [1  ,1  ,],
            (1/2,1/2)
    ],
    'RK2Midpoint' : [
        [0  ,],
        [1/2,1/2,],
            (0  ,  1)
    ],
    'RK3 Simpson' : [
        [0  ,],
        [1/2, 1/2,],
        [1  ,-1  , 2  ,],
            ( 1/6, 2/3, 1/6),
    ],
    'RK3 Heun' : [
        [0  ,],
        [2/3, 1/3,],
        [2/3, 0  , 2/3,],
            ( 1/4, 0  , 3/4),
    ],
    'RK4 Classic' : [
        [0   ,],
        [1/2 ,1/2 ,],
        [1/2 ,0   ,1/2 ,],
        [1   ,0   ,0   ,1   ,],
             (1/6 ,1/3 ,1/3 ,1/6),
    ],
    'RK4 3/8' : [
        [0  ,],
        [1/3, 1/3,],
        [2/3,-1/3,   1,],
        [1  ,   1,  -1,   1,],
            (1/8 , 3/8, 3/8,1/8),
    ],
    'RK 6 stages'      : [
        [0  ,],
        [1/4, 1/2 ,],
        [1/4, 3/16, 1/16,],
        [1/2, -1/4, -1/4, 1    , ],
        [3/4, 3/16, 0   , 0    , 9/16 ,],
        [1  , -2/7, 1/7 , 12/7 , -12/7, 8/7  ,],
            ( 7/90, 0   , 16/45, 2/15 , 16/45, 7/90)
    ],
})

class ode:
    """ Ordinary differential equation y' = f(x,y) """
    global x, y
    x, y = symbols("x y")

    def __init__(self, f_xy:str, a:float=0, b:float=0, y_0:float=0) -> None:
        self.function = parse_expr(f_xy, transformations=transform)
        self.interval = (a,b)
        self.y_0      = y_0
        self.feval    = lambdify((x,y),self.function,"numpy")

    def __call__(self, xi:float, yi:float) -> float:
        return self.feval(xi,yi)

    def get_init_value(self):
        return self.interval + (self.y_0,)

def Runge_Kutta(f:ode, h:float=0.1, method='RK4 Classic') -> Iterable[float]:
    """ Runge-Kutta method with uniform grid step h """
    R, ALPHA, BETA = BUTCHER_TABLEAU[method]
    a, b, y = f.get_init_value()
    s, n    = len(R), int((b-a)/h + 1)
    k       = np.zeros(s)
    yield y
    for t in range(n-1):
        for i in range(s): 
            k[i] = h*f(a+t*h+h*ALPHA[i],y+fsum(k[j]*BETA[i][j] for j in range(i)))

        y = y + fsum(R[i]*k[i] for i in range(s))
        yield y
    print(f"\n {method} - h = {h} \t\t y({b}) = {y}")

def solve_and_plot(f:ode, steps:List[float], methods:List[str],exact=None) -> None:
    """ Use RKs to solve then plot the result """

    line_pattern = "% 10.4f\t" + "% 15.6f\t" * len(methods) + "\n"
    savepath = os.sep.join((this_dir,'output','runge_kutta.png'))
    header   = "\n_____________________ h = %f _____________________\n" + "\t".join(
                ["     x     "] + [f"{name:>15s}" for name in methods]) + "\n"
    marker   = cycle((',', '+', '.', 'o', '*','x','^'))
    a, b     = f.interval    
    plt.figure(figsize=(10,6),dpi=120)
    plt.grid()
    
    with open(os.sep.join((this_dir,'output','runge_kutta.txt')),'w') as output_file:
        output_file.write(f"y' = {f.function}\n")
        for h in steps:
            output_file.write(header % h)
            point_x   = [a + t*h for t in range(int((b-a)/h + 1))]
            rk_return = []
            for method in methods:
                solution = tuple(Runge_Kutta(f, h, method))
                rk_return.append(solution)
                plt.plot(point_x, solution, label=f"{method} - h={h}",marker=next(marker))

            y_values = iter(zip(*rk_return))
            for x_i in point_x: output_file.write(line_pattern % ((x_i,) + next(y_values)))
    
    if exact:
        x_range = np.linspace(a, b, 4096)
        y_exact = lambdify(x,parse_expr(exact,transformations=transform),"numpy")
        plt.plot(x_range, y_exact(x_range), '--', label='Exact')
    
    plt.legend()
    plt.savefig(savepath)
    plt.show()
    plt.close()

def main() -> None:
    METHODS    = BUTCHER_TABLEAU.keys()
    f_xy       = input(f"\n{GREEN} Enter equation: {RESET}\n y' = ")
    init_value = input(f"\n Init value: {YELLOW} a <= x <= b, y(a) = y0 {RESET}"+
                        "\n Enter a b y0 h (allow more than one h): ")
    choices    = input(f"\n{GREEN}:--- R-K:{RESET} {dict(enumerate(METHODS))}"+
                       f"\n{GREEN}'------->{RESET} Select (Ex: 1 3, no input = all): ")
    exact      = input("\n Exact solution (no input = skip): y(x) = ").strip()
    
    a,b,y0,*h  = [float(i) for i in init_value.split()]
    methods    = [tuple(METHODS)[int(i)] for i in choices.split()] or METHODS
    f          =  ode(f_xy, a, b, y0)
    solve_and_plot(f, h, methods, exact)

if __name__ == '__main__':
    main()