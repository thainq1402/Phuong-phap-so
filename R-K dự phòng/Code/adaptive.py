from typing                     import List, Iterable, Tuple
from sympy                      import symbols,lambdify
from sympy.parsing.sympy_parser import (standard_transformations,
    implicit_multiplication_application,convert_xor,parse_expr)
from matplotlib                 import pyplot as plt
from math                       import fsum
import numpy                    as np
import os

transform = (standard_transformations+(implicit_multiplication_application,convert_xor))
this_dir  = os.path.dirname(os.path.abspath(__file__))
if not os.path.isdir(this_dir+os.sep+'output'): os.mkdir(this_dir+os.sep+'output')

RK_ADAPTIVE = {k:(v.pop(),[r.pop(0) for r in v],v) for k,v in {
    'EH12': [
        [0   ,],
        [1   ,  1,],
            ((1/2,1/2),
             (1  ,  0),0.5)
    ],
    'BS34': [
        [0   ,],
        [1/2, 1/2 ,],
        [3/4, 0   , 3/4,],
        [1  , 2/9 , 1/3, 4/9,],
           (( 7/24, 1/4, 1/3, 1/8,),
            (  2/9, 1/3, 4/9, 0  ,),0.25)
    ],
    'RKF45': [
        [0    ,],
        [1/4  ,   1/4   ,],
        [3/8  ,  3/32   ,   9/32   ,],
        [12/13,1932/2197,-7200/2197,7296/2197 ,],
        [1    , 439/216 ,   -8     , 3680/513 , -845/4104 ,],
        [1/2  ,  -8/27  ,    2     ,-3544/2565, 1859/4104 ,-11/40 ,],
             ((  16/135 ,    0     ,6656/12825,28561/56430, -9/50 ,2/55,),
              (  25/216 ,    0     , 1408/2565, 2197/4104 ,  -1/5 ,   0,),0.2)
    ]
}.items()}

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

    def get_init_value(self) -> Tuple[float]:
        return self.interval + (self.y_0,)

def Runge_Kutta_Fehlberg(f:ode,h0:float,hmin:float,hmax:float,atol:float,
                        rtol=4e-3,method='RKF45') -> Iterable[Tuple]:
    """ Runge Kutta adaptive step size method """
    R, ALPHA, BETA = RK_ADAPTIVE[method]
    a, b, y0 = f.get_init_value() 
    x, y, h  = a, y0, max(min(h0, hmax),hmin)
    s, count = len(R[0]), 0
    k        = np.zeros(s)
    yield x, y
    while x < b:
        count += 1
        if x + h > b: h = b - x
        for i in range(s):
            k[i] = h*f(x + h*ALPHA[i], y + fsum(k[j]*BETA[i][j] for j in range(i)))
        delta_y0 = fsum(R[0][i]*k[i] for i in range(s))
        delta_y1 = fsum(R[1][i]*k[i] for i in range(s))
        delta    = abs(delta_y0 - delta_y1)
        err      = delta/atol + rtol
        if err <= 1:
            x, y = x + h, y + delta_y0
            yield x, y
        if h < hmin: break
        h = min(0.94*h*(1/err)**(R[2]),hmax)
    print(f"\n {count} loops\n y({x}) = {y}")

def solve_and_plot(f:ode,h:List[float],exact=None) -> None:
    """ Use Fehlberg method to solve and plot """
    
    if   len(h) == 0: h0, atol, hmin, hmax = 0.1 , 1e-6, 1e-4, 0.2
    elif len(h) == 1: h0, atol, hmin, hmax = h[0], 1e-6, 1e-4, 0.2
    elif len(h) == 2: h0, atol, hmin, hmax = h[0], h[1], 1e-4, 0.2
    elif len(h) == 3: h0, atol, hmin, hmax = h[0], h[1], h[2], 2000*h[2]
    elif len(h) == 4: h0, atol, hmin, hmax = h
    else: return
    savepath = os.sep.join((this_dir,'output','adaptive.png'))
    result   = np.array(tuple(Runge_Kutta_Fehlberg(f,h0,hmin,hmax,atol)))
    plt.plot(result[:,0],result[:,1],marker='o',label='RK-Fehlberg')
    a, b = f.interval
    print("\n Points:",result.shape[0])
    
    if exact:
        x_range = np.linspace(a, b, 4096)
        y_exact = lambdify(x,parse_expr(exact,transformations=transform),"numpy")
        plt.plot(x_range, y_exact(x_range), '--', label='Exact')
    
    plt.grid()
    plt.legend()
    plt.savefig(savepath)
    plt.show()

def main() -> None:
    f_xy       = input("\n Enter equation:" + "\n y' = ")
    init_value = input("\n Init Value: a <= x <= b, y(a) = y0\n" +
                       "\n Enter a b y0 h0 (eps hmin hmax): ").replace('(','').replace(')','')
    exact      = input("\n Exact solution (no input = skip): y(x) = ").strip()

    a,b,y0,*h  = [float(i) for i in init_value.split()]
    f          =  ode(f_xy, a, b, y0)
    solve_and_plot(f, h, exact)

if __name__ == '__main__':
    main()
