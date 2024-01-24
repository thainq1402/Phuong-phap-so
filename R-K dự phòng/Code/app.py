from itertools      import cycle
from typing         import Callable, Tuple
from sympy          import symbols, lambdify, parse_expr
import tkinter as tk, adaptive as fb, runge_kutta as rk, systemofODEs as sode, numpy as np

prompt: dict[int,tk.Label] = {}
entry:  dict[int,tk.Entry] = {}

prompt_style = {
    'font': ('Courier',14), 
    'wraplength': 500, 
    'justify': tk.CENTER,
}

entry_style = { 
    'font': ('Courier',14),
    'width' : 45, 
    'justify': tk.CENTER,
}

METHODS   = rk.BUTCHER_TABLEAU.keys()
modes     = cycle(("System ODEs","Ode y'=f(x,y)")) 
transform = rk.transform

def create_sys(f_func:str, g_func:str, h_func:str, order:int) -> Callable[[float,Tuple],np.array]:
    """ Create a system of ODEs up to order 3 from string of functions """
    t, x, y, z = symbols("t x y z")
    if   order == 1: var = (t,x)
    elif order == 2: var = (t,x,y)
    elif order == 3: var = (t,x,y,z)
    else: return
    if order >= 1:
        f   = parse_expr(f_func,transformations=transform)
        ff  = lambdify(var,f,"numpy")
        ret = lambda t,x: np.array([ff(t,x[0])])
    if order >= 2:
        g   = parse_expr(g_func,transformations=transform)
        gg  = lambdify(var,g,"numpy")
        ret = lambda t,x: np.array([ff(t,x[0],x[1]),gg(t,x[0],x[1])])
    if order == 3:
        h   = parse_expr(h_func,transformations=transform)
        hh  = lambdify(var,h,"numpy")
        ret = lambda t,x: np.array([ff(t,x[0],x[1],x[2]),gg(t,x[0],x[1],x[2]),hh(t,x[0],x[1],x[2])])

    return ret

def switch_mode() -> None:
    def sol_one() -> None:
        """ Get input and solve y'=f(x,y) """
        fehlberg = box_val.get()
        f_xy     = entry[0].get().strip()
        init_val = entry[1].get().strip()
        choices  = entry[2].get().strip()
        exact    = entry[3].get().strip()
        message.config(text="(*) Required")
        try:
            init_val  = init_val.replace('(',' ').replace(')','').replace(',',' ')
            choices   = choices.replace('(',' ').replace(')','').replace(',',' ')
            a,b,y0,*h = [float(i) for i in init_val.split()]
            f         =  rk.ode(f_xy, a, b, y0)

            if fehlberg: fb.solve_and_plot(f, h, exact)
            else:
                methods = [tuple(METHODS)[int(i)] for i in choices.split()] or METHODS
                rk.solve_and_plot(f, h, methods, exact)
        except:
            message.config(text='An error occurred, please try again.')

    def sol_sys() -> None:
        """ Get input from system of ODEs and solve """
        f_func   = entry[0].get().strip()
        g_func   = entry[1].get().strip()
        h_func   = entry[2].get().strip()
        interval = entry[3].get().strip()
        init_val = entry[4].get().strip()
        message.config(text="(*) Required")
        if f_func: order = 1
        if g_func: order = 2
        if g_func and h_func: order = 3
        try:
            init_val  = init_val.replace('(',' ').replace(')','').replace(',',' ')
            interval  = interval.replace(',',' ')
            t0, tf, dt = (float(i) for i in interval.split())
            x0 = np.array(init_val.split(),dtype=float)
            f  = create_sys(f_func, g_func, h_func, order)

            sode.solve_and_plot(f, x0, t0, tf, dt)
        except:
            message.config(text='An error occurred, please try again.')

    mode = next(modes)
    btn_switch.config(text='Mode: ' + mode)
    message.config(text="(*) Required")
    message.pack_forget()
    btn_solve.pack_forget()
    btn_exit.pack_forget()

    if mode == "Ode y'=f(x,y)":  
        btn_solve.config(command=sol_one)
        prompt[0].config(text="(*) Equation: y' = f(x,y) = ")
        prompt[1].config(text="(*) Enter a b y0 h (eps hmin hmax): ")
        prompt[2].config(text=f"Select RK by number (no input = all)\n {dict(enumerate(METHODS))}")
        prompt[3].config(text="Exact solution y(x) = ")
        box.pack()
        prompt[4].pack_forget()
        entry[4].pack_forget()
    else:
        btn_solve.config(command=sol_sys)
        prompt[0].config(text="(*) x'(t) = f(t,x,y,z) = ")
        prompt[1].config(text="    y'(t) = g(t,x,y,z) = ")
        prompt[2].config(text="    z'(t) = h(t,x,y,z) = ")
        prompt[3].config(text="(*) t0 <= t <= tf, step dt. Enter t0 tf dt: ")
        prompt[4].config(text="(*) Init value x0 (y0 (z0)): ")
        prompt[4].pack()
        entry[4].pack()
        box.pack_forget()

    btn_solve.pack()
    btn_exit.pack()
    message.pack()

app = tk.Tk()
app.title('Runge-Kutta')
app.geometry('500x440')
app.resizable(0,0)

mode = next(modes)
btn_switch = tk.Button(app, text='Mode: '+mode, width=20, foreground='green', command=switch_mode)
btn_solve  = tk.Button(app, text='Solve and plot', width=40, foreground='green')
btn_exit   = tk.Button(app, text='Exit', width=40, foreground='red', command=exit)

box_val = tk.IntVar()
box     = tk.Checkbutton(app, text='Fehlberg (Default: eps=1e-6,hmin=1e-4,hmax=0.2)',
                     variable=box_val, onvalue=1, offvalue=0)
message = tk.Label(app, text='(*): Required', cnf=prompt_style)

for i in range(5):
    prompt[i] = tk.Label(app, text='', cnf=prompt_style)
    entry[i]  = tk.Entry(app, cnf=entry_style)

btn_switch.pack()
for k in prompt.keys():
    prompt[k].pack()
    entry[k].pack()
box.pack()
btn_solve.pack()
btn_exit.pack()

switch_mode()
app.mainloop()