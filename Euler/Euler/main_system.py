from matplotlib import pyplot as plt

INPUT = {
    "k" : 2,    # number of equation
    "t0": 3,    
    "tn": 6,
    "h" : 0.1,

    "iv": (3, 1, -0.5)   # initial values
}

"""
System of ODEs:
    dx1/dt = f1(t, x1, x2, ..., xn)
    dx2/dt = f2(t, x1, x2, ..., xn)
    dx3/dt = f3(t, x1, x2, ..., xn)
    ...
    dxn/dt = fn(t, x1, x2, ..., xn)

with the initial values:
    x1(t0) = x1_0, x2(t0) = x2_0, ..., xn(t0) = xn_0

We can apply Euler method to approximate the x1, x2, ..., xn
at t1 and repeat that process until we reach the final t point
"""

def stepSolve(t, y):
    """
    `y` is a list to store the answer after each step

    For example, with k = 2, we have y = [x0, y0], so 
    y[0] and y[1] are used as x0 and y0.

    Given system of ODEs:
            x' = 8y + 2x                    \n
            y' = 22x + 11y
    can be rewrited as:
            y[0]' = 8y[1] + 2y[0]           \n
            y[1]' = 22y[0] - 11y[1]

    >>> return [
            8*y[1] + 2*y[0],
            22*y[0] - 11*y[1]
    ]
    """
    return [
        # -5*y[0] + 5*y[1],
        # 14*y[0] - 2*y[1] - y[2]*y[0],
        # -3*y[2] + y[0]*y[1] 
       -2*y[0]+y[1],
       y[0]-2*y[1]
    ]

def solve(k, t0, tn, h, iv):
    """
    `iv` is the short form of initial values (giá trị ban đầu)
    `y_list` is a list with `k` sublists to save the answer for each equation
    """
    t_list, y_list = [t0], [[iv[i]] for i in range(k)]
    fi = iv
    yi = []
    n  = int((tn - t0)/h)
    for j in range(n):
        t_list.append(t0 + h*(j+1))

        yi = [y_list[i][-1] for i in range(k)]    
        fi = stepSolve(t0+h*j, yi)
        for i in range(k):
            y_list[i].append(yi[i] + h*fi[i])

    return t_list, y_list

def saving(xi, answerLists_y, labelList, filename):
    with open('Output/' + filename, 'w') as output_:
        output_.truncate(0)
        
    n = len(str(len(xi)))
    output_text = "\nUsing Forward Euler method:\n\n    " + (n-1)*" " + "i    xi          "
    for label in labelList:
        output_text += label + (24-len(label))*" "
    with open('Output/' + filename, 'a') as output_:
        output_.write(output_text + "\n")
        
        for i in range(len(xi)):
            output_ans = ""
            for method_y in answerLists_y:
                output_ans += str(method_y[i]) + (24-len(str(method_y[i])))*" "
            output_num = f"""\n    {(n - len(str(i)))*" " + str(i)}    {format(xi[i], '.6f')}    {output_ans}"""

            output_.writelines(output_num)

def plotting(x_collection, y_collection, label_collection, filename):
    """
    Use `pyplot` to plot the result
    """
    for i in range(len(y_collection)):
        try:
            plt.plot(x_collection, y_collection[i], label=label_collection[i])
        except Exception as e:
            print("Can't plot " + label_collection[i])
            print(f"Error: \n{e}")
    
    plt.legend()
    plt.title("No title")
    plt.grid(True)

    plt.savefig('Output/' + filename)

    plt.show()

def main() -> None:
    k, t0, tn, h, iv = list(INPUT.values())
    
    answer  = solve(k, t0, tn, h, iv)

    labels  = ["x", "y", "z", "t", "w"]
    saving(answer[0], answer[1], labels[:k], 'output_system.txt')
    plotting(answer[0], answer[1], labels[:k], 'output_system.png')

if __name__ == '__main__':
    main()