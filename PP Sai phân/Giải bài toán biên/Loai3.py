import numpy as np
import matplotlib.pyplot as plt
from sympy import *


x, n, h = symbols("x"), None, None
init_printing()


print(
    f"""
# .Bài toán:
    Tìm u(x) là nghiệm của phương trình vi phân :
    [p(x) * u'(x)]' - q(x) * u(x) = -f(x) với a =< x =< b
    Trong đó : (#.Điều kiện)
    p(x), q(x), f(x) là những hàm số liên tục và có đạo hàm cấp cần thiết trên đoạn [a, b]
    p(x) >= c1 > 0
    q(x) >= 0
# .INPUT:
    p(x), q(x), f(x), a, b
    Biên loại 3 => 
        p(a) * u'(a) - sigma1 * u(a) = -mu1
        p(b) * u'(b) - sigma2 * u(b) = -mu2
    sigma1, sigma2, mu1, mu2 

    Và thêm n là số mốc => h = (b - a) / (n - 1)
    Hoặc thêm h là khoảng cách lưới => n = int(1 + (b - a) / h)
"""
)


def p(x):
    # .Không có dấu -
    return 1


def q(x):
    # .Có dấu - trong đề bài
    return x**2


def f(x):
    # .Có dấu - trong đề bài
    return 2


a = -1
b = 1
# .Có dấu - trong đề bài
sigma1 = 1
# .Có dấu - trong đề bài
sigma2 = 1
# .Có dấu - trong đề bài
mu1 = 1
# .Có dấu - trong đề bài
mu2 = 1
# Thêm n hoặc h
h = 1 / 2
# n=5
# .Tính n, h theo đề bài cho:
# n là số mốc => h = (b - a) / (n - 1)
# Hoặc
# h là khoảng cách lưới => n = int(1 + (b - a) / h)
if (n is None) and (h is None):
    raise ValueError("Phải có giá trị n hoặc h")
if (n is not None) and (h is not None):
    raise ValueError("Chỉ có giá trị n hoặc h")
if n is not None:
    h = (b - a) / (n - 1)
    str_n_h = f"Vì n = {n} => h = {h}"
else:
    n = (b - a) / h + 1
    str_n_h = f"Vì h = {h} => n = {n}"
    n = int(n)
    str_n_h += f" => n = {n}"

print(
    f""" 
# .INPUT:
    p(x) = {p(x)}
    q(x) = {q(x)}
    f(x) = {f(x)}
    a = {a}
    b = {b}

    sigma1 = {sigma1}
    sigma2 = {sigma2}
    mu1 = {mu1}
    mu2 = {mu2} 
    {str_n_h}   
"""
)
# => Xong INPUT
print(
    f"""
# .Xét điều kiện:
    p(x), q(x), f(x) là những hàm số liên tục và có đạo hàm cấp cần thiết trên đoạn [a, b]
    p(x) >= c1 > 0
    q(x) >= 0
"""
)


def ox(x):
    return 0


x = np.linspace(a, b, 1000)
y_p = np.array([p(i) for i in x])
y_q = np.array([q(i) for i in x])
y_ox = np.array([ox(i) for i in x])
min_y_p = min(y_p)
min_y_q = min(y_q)
plt.plot(x, y_p, label=f"p(x); min={min_y_p}>0; ({min_y_p>0})")
plt.plot(x, y_q, label=f"q(x); min={min_y_q}>=0; ({min_y_q>=0})")
plt.plot(x, y_ox, label="ox: y = 0")
plt.legend()
print(f"p(x) >= {min_y_p} > 0 ({min_y_p>0})")
print(f"q(x) >= {min_y_q} >= 0 ({min_y_q>=0})")
if (min_y_p > 0) and (min_y_q >= 0):
    print(f"=> Có thỏa mãn điều kiện")
else:
    raise ValueError(f"=> Ko thỏa mãn điều kiện")
plt.show()
print(
    f"""
# .Xây dựng hệ có dạng 3 đường chéo theo công thức
    Cần tìm U là nghiệm của A*U=B 
    Vì là biên loại 3
    => mấy giá trị đầu,cuối thì tính theo công thức
    Tìm các hệ số còn lại: ai*u[i-1] + bi*u[i] + ci*u[i+1] = di")
"""
)
A = np.zeros((n, n))
B = np.zeros((n, 1))

A[0, 0] = -(sigma1 + p(a + h / 2) / h - q(a) * h / 2)
A[0, 1] = p(a + h / 2) / h
B[0] = -mu1 - f(a) * h / 2

A[n - 1, n - 2] = -p(b - h / 2) / h
A[n - 1, n - 1] = -sigma2 + p(b - h / 2) / h - q(b) * h / 2
B[n - 1] = -mu2 - f(b) * h / 2
# Biên loại nào cũng lặp ntn
for i in range(1, n - 1):
    xi = a + i * h
    A[i, i - 1] = p(xi - h / 2) / (h * h)
    A[i, i] = -(p(xi + h / 2) + p(xi - h / 2)) / (h * h) - q(xi)
    A[i, i + 1] = p(xi + h / 2) / (h * h)
    B[i] = -f(xi)


print(f"A = \n{A}")
print(f"B = \n{B}")


print(
    f"""
# .Giải hệ có dạng 3 đường chéo:
    Cần tìm U là nghiệm của A*U=B
"""
)


def GoiCoSanPython(A, B):
    print(f"- Nếu dùng gói có sẵn giải HPT:")
    u_goi_co_san = np.linalg.solve(A, B)
    print(f"u = \n{u_goi_co_san}")
    return u_goi_co_san


u_goi_co_san = GoiCoSanPython(A, B)
x = np.linspace(a, b, n).reshape((n, 1))



VeDoThiInput = input(f"# .Vẽ đồ thị: Enter để tiếp tục ")
plt.scatter(x, u_goi_co_san)
plt.title(f"n = {n}")
plt.show() 
print(f"# .Kết thúc chương trình")
