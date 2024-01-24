from sympy import symbols, Function, lambdify
from sympy.core.facts import apply_beta_to_alpha_route
from sympy.parsing.sympy_parser import (standard_transformations, implicit_multiplication_application, convert_xor,parse_expr)
from matplotlib import pyplot as plt

from Euler_forward      import forward      as fw
from Euler_backward     import backward     as bw
from Euler_trapezoidal  import trapezoidal  as tz
import wolfram

TRANSFORMATIONS     = (standard_transformations + (implicit_multiplication_application, convert_xor))
METHODS             = ["Forward", "Backward", "Trapezoidal"]
MODULES             = 'sympy'

def exactSolve(f, x:symbols, x0:float, y0:float, xn:float, h:float): #giải chính xác hàm bằng wolfram
    """
    Find exact answer of the ODE to compare with the answer of Euler method

    First we get the answer from wolfram by using the function `wolfram.solve`
    But the answer might have the substring "e^" in it such that "e^x"
    so the next 2 `replace()` functions are to replace "e^" with "exp"
    so that we can plot it
    """
    try:
        # Use Wolfram Alpha API to solve
        wa_result           = wolfram.solve(f"y' = {f}, y({x0}) = {y0}")

        # Replace "e^f" in the answer from Wolfram with "exp(f)"
        wa_result_replaced  = wa_result.replace("e^", "exp")
        wa_result_replaced  = wa_result_replaced.replace("expx", "exp(x)")

        print(f"\nAnswer from Wolfram: y = {wa_result}\n")

        solve_expr  = parse_expr(wa_result_replaced, transformations=TRANSFORMATIONS)
        f_wa        = lambdify(x, solve_expr, modules=MODULES)

        n           = int((xn - x0)/h) + 1
        xe_list     = [x0 + h*i for i in range(1, n)]
        ye_list     = [y0]
        for xi in xe_list:
            ye_list.append(f_wa(xi))
        
        return ye_list
    except:
        return None

def saving(xi, answerLists_y, labelList): #đưa kết quả vào output
    n = len(str(len(xi)))
    output_text = "\nUsing Euler methods:\n\n    " + (n-1)*" " + "i    xi          "
    for label in labelList:
        output_text += label + (24-len(label))*" "
    with open('Output/output.txt', 'a') as output_:
        output_.write(output_text + "\n")
        
        for i in range(len(xi)):
            output_ans = ""
            for method_y in answerLists_y:
                output_ans += str(method_y[i]) + (24-len(str(method_y[i])))*" "
            output_num = f"""\n    {(n - len(str(i)))*" " + str(i)}    {format(xi[i], '.6f')}    {output_ans}"""

            output_.writelines(output_num)
    
def plotting(x_collection, y_collection, label_collection, func, h): #vẽ đồ thị
    """
    Use pyplot to plot the result
    """
    for i in range(len(y_collection)):
        try:
            if label_collection[i] == "Exact Answer":
                plt.plot(x_collection, y_collection[i], "-.", label=label_collection[i])
            else:        
                plt.plot(x_collection, y_collection[i], label=label_collection[i])
        except Exception as e:
            print("Can't plot " + label_collection[i])
            print(f"Error: \n{e}")
    
    plt.legend()
    plt.title(f"y' = {func}\nh = {h}")
    plt.grid(True)

    plt.savefig('Output/output.png')

    plt.show()

def switch(argument, f, x0, y0, xn, h): #giải ở chỗ này, gọi hàm từ các gói
    switcher = {
        0: fw(f, x0, y0, xn, h),
        1: bw(f, x0, y0, xn, h),
        2: tz(f, x0, y0, xn, h)
    }

    return switcher.get(argument, "Incorrect method number!")[1]

def main() -> None:
    #khai báo output
    with open('Input/input.txt', 'r') as input_:
        input_lines = [lines.strip() for lines in input_]
    #khai báo biến
    x               = symbols('x')
    y               = symbols('y', cls=Function)
    f_input         = parse_expr(input_lines[0], transformations=TRANSFORMATIONS)
    f               = lambdify(args=(x, y), expr=f_input, modules=MODULES) 
    x0, y0, xn, h   = [float(value) for value in input_lines[1].split(",")] 
    use_methods     = [int(value) for value in input_lines[2].split(",")]
    doExactSolve    = True if input_lines[3] == 'y' else False #hỏi xem có cần tính chính xác không (dùng hàm)
    #in ra màn hình
    print(
        f"""
        y' = f(x, y) = {input_lines[0]}
        Enter x0, y0, xn, h: {input_lines[1]}"""
        )
    
    #nhập các mốc x vào mảng
    answerList_x = [x0]
    for i in range(int((xn-x0)/h)):
        answerList_x.append(x0 + h*(i+1))
    #khai báo mảng y và answerlabels
    answerLists_y, answerLabels = [], []
    #giải chính xác
    if doExactSolve: answer_ex = exactSolve(f_input, x, x0, y0, xn, h)
    else: answer_ex = None
    #tính toán
    print_text = "Methods used: "
    for method_no in use_methods:
        print_text += METHODS[method_no]
        if method_no != use_methods[-1]: print_text += ", "

        answerLists_y.append(switch(method_no, f, x0, y0, xn, h)) #mỗi switch(method) trả về một list y và append vào answerList_y (list của list)
        answerLabels.append(METHODS[method_no]) #lưu lại tên method (để display cho tiện)
        
    print(print_text + "\n")
    
    if answer_ex != None:
        answerLists_y.append(answer_ex)
        answerLabels.append("Exact Answer")

    ########################################
    # Save all xi and yi

    with open('Output/output.txt', 'w') as output_:  #lưu vào 
        output_.truncate(0)
    saving(answerList_x, answerLists_y, answerLabels)

    ########################################    

    plotting(answerList_x, answerLists_y, answerLabels, f_input, h) #vẽ
  
if __name__ == '__main__':
    main()
    