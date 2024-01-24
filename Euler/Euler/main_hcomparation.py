from sympy import symbols, Function, lambdify
from sympy.parsing.sympy_parser import (standard_transformations, implicit_multiplication_application, convert_xor,parse_expr)
from matplotlib import pyplot as plt

from Euler_forward      import forward
from Euler_backward     import backward
from Euler_trapezoidal  import trapezoidal

TRANSFORMATIONS = (standard_transformations + (implicit_multiplication_application, convert_xor))

def switch(argument, f, x0, y0, xn, h):
    switcher = {
        0: forward(f, x0, y0, xn, h),
        1: backward(f, x0, y0, xn, h),
        2: trapezoidal(f, x0, y0, xn, h)
    }

    return switcher.get(argument, "Incorrect method number!")

def plotting(x_collection, y_collection, label_collection, func, method_name):
    """
    Use pyplot to plot the result
    """
    for i in range(len(y_collection)):
        try:
            plt.plot(x_collection[i], y_collection[i], label="h = " + str(label_collection[i]))
        except Exception as e:
            print("Can't plot with step h = " + str(label_collection[i]))
            print(f"Error: \n{e}")
    
    plt.legend()
    plt.title(f"y' = {func}\nUsing {method_name} method")
    plt.grid(True)

    plt.savefig('Output/output_hcomparation.png')

    plt.show()

def main() -> None:
    x           = symbols('x')
    y           = symbols('y', cls=Function)
    f_input     = parse_expr(input("y' = f(x, y) = "), transformations=TRANSFORMATIONS)
    f           = lambdify((x, y), f_input, modules="sympy")
    x0, y0, xn  = [float(value) for value in input("Enter x0, y0, xn: ").split(",")]
    h_list      = [float(value) for value in input("Enter list of step size (h): ").split(",")]
    method_used = int(input("Method used: "))
    method_list = ["Forward Euler", "Backward Euler", "Trapezoidal"]
    print("Using " + method_list[method_used] + " method")

    answerList_x = []
    answerList_y = []
    for h in h_list:
        answer = switch(method_used, f, x0, y0, xn, h)
        answerList_x.append(answer[0])
        answerList_y.append(answer[1])

    plotting(answerList_x, answerList_y, h_list, f_input, method_list[method_used])

if __name__ == '__main__':
    main()