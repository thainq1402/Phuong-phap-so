from matplotlib     import pyplot as plt
from main_system import plotting, saving

INPUT = {
    "k" : 2,    # level of equation
    "t0": 0,    
    "tn": 5,
    "h" : 0.1,

    "iv": (0, 1, 0)    # initial values
}

"""
Let take an n_th order different equation:
    y_(n) = F(x, y, y', ..., y_(n-1))

Define new variables u1, u2, ..., un and rewrite the system:
    u1' = u2
    u2' = u3
    ...
    un-1' = un
    un' = F(x, u1, u2, ..., un)

Then we can solve it as a system of first order ODEs
"""

def stepSolve(x, y):
    """
    `y` is a list to store the answer after each step

    For example, with k = 2, we have y = [y'0, y''0], so 
    y[0] and y[1] are used as y'0 and y''0.

    Given ODE:
            v''(t) = 8v'(t) + 2v(t)                   \n
    
    we will use some variable substitution.
    Define y[0] = v(t), y[1] = v'(t) and we have the system:
            y[0]' = y[1]
            y[1]' = 8y[1] + 2y[0]

    >>> return [
            y[1],
            8*y[1] + 2y[0]
    ]
    """
    y_n = 2*y[2] + 8*y[1] + y[0] + x
    
    return [y[i+1] for i in range(len(y)-1)] + [y_n]

def solve(k, t0, tn, h, iv):
    """
    `iv` is the short form of initial values
    `y_list` is a list with `k` sublists to save the answer for each equation
    """
    t_list, y_list = [t0], [[iv[i]] for i in range(k)]
    fi = iv
    yi = []
    n  = int((tn - t0)/h)
    for j in range(n):
        t_list.append(t0 + h*(j+1))

        yi = [y_list[i][-1] for i in range(k)]    
        fi = stepSolve(t0 + h*j, yi)
        for i in range(k):
            y_list[i].append(yi[i] + h*fi[i])

    return t_list, y_list

def main() -> None:
    k       = INPUT.get("k")
    t0      = INPUT.get("t0")
    tn      = INPUT.get("tn")
    h       = INPUT.get("h")
    iv      = INPUT.get("iv")

    answer  = solve(k, t0, tn, h, iv)

    saving(answer[0], [answer[1][0]], "y", 'output_high.txt')
    plotting(answer[0], [answer[1][0]], "y", 'output_high.png')


if __name__ == '__main__':
    main()