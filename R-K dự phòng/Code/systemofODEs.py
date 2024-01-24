from typing                 import Tuple
from matplotlib.widgets     import Button
from adaptive               import RK_ADAPTIVE
from math                   import *
import numpy                as np
import matplotlib.pyplot    as plt
import os

this_dir = os.path.dirname(os.path.abspath(__file__))
if not os.path.isdir(this_dir+os.sep+'output'): os.mkdir(this_dir+os.sep+'output')

##################################################################

def f(t,x) -> np.array:
    """
    Hướng dẫn:
    ```txt
                    (Đổi biến, hàm x biến t)
           y' = 1.1y - 0.4yz   <=>  x_0' = 1.1*x_0 - 0.4*x_0*x_1
           z' = 0.1yz - 0.4z        x_1' = 0.1*x_0*x_1 - 0.4*x_1
    ```
    thì hàm này sẽ có return như sau:
    >>> return np.array([
                    1.1*x[0] - 0.4*x[0]*x[1],
                    0.1*x[0]*x[1] - 0.4*x[1],
                ])
    """
    return np.array([
                        # Sửa return ở dòng dưới này
                        0.6*x[0]*(1 - x[0]/100) - 0.4*x[0]*x[1],
                        0.4*x[0]*x[1] - 1.2*x[1],

                ])

##################################################################

def RungeKutta4(f,x0,t0:float,tf:float,dt:float) -> Tuple[np.array]:
    """ Use classic RK4 to solve system of ODEs """
    nt     = int((tf-t0)/dt + 1)
    t      = np.linspace(t0,tf,nt,endpoint=True)
    nx     = x0.size
    x      = np.zeros((nx,nt))
    x[:,0] = x0
    for k in range(nt-1):
        k1 = dt*f(t[k],x[:,k])
        k2 = dt*f(t[k] + dt/2,x[:,k] + k1/2)
        k3 = dt*f(t[k] + dt/2,x[:,k] + k2/2)
        k4 = dt*f(t[k] + dt,x[:,k] + k3)
        x[:,k+1] = x[:,k] + (k1 + 2*k2 + 2*k3 + k4)/6
    return x,t

def Runge_Kutta_Fehlberg(f,x0, a:float, b:float, h0:float, hmin=1e-4, hmax=0.2,
                         atol=1e-6, rtol=4e-3) -> Tuple[np.array]:
    """ Use RKF in solving system of ODEs order 1 """
    
    R, ALPHA, BETA = RK_ADAPTIVE['RKF45']
    x, y, h  = a, x0, max(min(h0,hmax),hmin)
    s, nx    = len(R[0]), x0.size
    k        = [None]*s
    xr, yr   = [x], [y]
    
    def SUM(First, Second, n:int) -> list:
        S = np.zeros(nx)
        for i in range(n): S = S + First[i]*Second[i]
        return S

    while x < b:
        if x + h > b: h = b - x
        k[0] = h*f(x,y)
        for i in range(1,s):
            k[i] = h*f(x + h*ALPHA[i], y + SUM(k,BETA[i],i))
        delta_y0 = SUM(k,R[0],s)
        delta_y1 = SUM(k,R[1],s)
        delta    = np.max(np.abs(delta_y1 - delta_y0))
        err      = delta/(atol) + rtol
        if err <= 1:
            x, y = x + h, y + delta_y0
            xr.append(x)
            yr.append(y)
        if h < hmin: break
        h = min(0.94*h*(1/err)**0.2,hmax)

    return np.stack(yr).T, np.array(xr)

def solve_and_plot(f, x0, t0:float, tf:float, dt:float) -> None:
    """ Solve system of ODEs and plot it in 2D,3D if there are 3 ODEs in the system """

    header = f"See the system in `systemofODEs.py`\n" + "\nData in each line: t" + (
             (", x_%d(t)"*x0.size) % tuple(range(x0.size-1,-1,-1)))
    savepath = os.sep.join((this_dir, 'output','systemSolution.png'))

    # adaptive = input("Press 'Enter' to plot").strip()   # :)
    adaptive = False
    x, t = Runge_Kutta_Fehlberg(f,x0,t0,tf,dt) if adaptive else RungeKutta4(f,x0,t0,tf,dt)
    np.savetxt(os.sep.join((this_dir,'output','systemSolution.txt')),
              np.rot90(np.vstack((x,t)),-1),'%15.6f',',\t',
              header=header,comments='#_____ ')
    print("",t.size,"points")
    print("x <=> x_0, y <=> x_1, z <=> x_2")
    fig = plt.figure(figsize=(8, 6),dpi=120)
    k   = x0.size
    for i in range(k): plt.plot(t,x[i,:],label=f'x_{i}')

    def special(_) -> None:
        nonlocal fig,bnext
        fig.clear()
        if k == 2:
            ax = fig.gca()
            ax.plot(x[0,:],x[1,:])
            plt.xlabel("x_0(t)")
            plt.ylabel("x_1(t)")
            fig.canvas.draw()
        else:
            ax = fig.gca(projection="3d")
            ax.plot(x[0,:], x[1,:], x[2,:])
            plt.draw()
        bnext.set_active(False)

    plt.xlabel("Time (t)")
    plt.legend()
    plt.savefig(savepath)

    if k == 2 or k == 3:
        axes  = plt.axes([0.87, 0.01, 0.08, 0.06])
        bnext = Button(axes, '2nd Plot')
        bnext.on_clicked(special)

    plt.show()
    plt.close()

class x_sample:
    @staticmethod
    def __getitem__(_) -> int: return 0

def main() -> None:
    order      = f(0,x_sample()).size
    t0, tf, dt = (float(i) for i in input("\n Enter start point (t0), end point (tf), step (dt)\n t0 tf dt: ").split())
    x0         = np.array(input(f"\n Enter {order} initial value(s): ").split(),dtype=float)
    solve_and_plot(f,x0, t0, tf, dt)

if __name__ == '__main__':
    main()
