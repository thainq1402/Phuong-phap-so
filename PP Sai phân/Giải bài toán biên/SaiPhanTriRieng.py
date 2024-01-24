import numpy as np
import matplotlib.pyplot as plt
from sympy import *


x, n, h = symbols("x"), None, None
init_printing()


print(
    f"""
# .Bài toán:
    Tìm 𝜆 và u(x) là nghiệm của phương trình vi phân :
    [p(x) * u'(x)]' - q(x) * u(x) = 𝜆*r(x)*u(x) với a < x < b
    Trong đó : (#.Điều kiện)
    # #.  p(x), q(x), r(x) là những hàm số liên tục và có đạo hàm cấp cần thiết trên đoạn [a, b]
    # # .p(x) >= c1 > 0
    # # .q(x) >= 0
    # # .r(x) > 0
# .INPUT:
    p(x), q(x), r(x)
    a, b
    u(a) := U_a, u(b) := U_b

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


def r(x):
    # .Không có dấu -
    return 2


a = -1
b = 1
U_a = 0
U_b = 0
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
    r(x) = {r(x)}
    a = {a}
    b = {b}
    u(a) = {U_a}
    u(b) = {U_b} 
    {str_n_h}      
"""
)
# => Xong INPUT
print(
    f"""
# .Xét điều kiện:
   Trong đó : (#.Điều kiện)
    # #.  p(x), q(x), r(x) là những hàm số liên tục và có đạo hàm cấp cần thiết trên đoạn [a, b]
    # # .p(x) >= c1 > 0
    # # .q(x) >= 0
    # # .r(x) > 0
"""
)


def ox(x):
    return 0


x = np.linspace(a, b, 1000)
y_p = np.array([p(i) for i in x])
y_q = np.array([q(i) for i in x])
y_r = np.array([r(i) for i in x])
y_ox = np.array([ox(i) for i in x])
min_y_p = min(y_p)
min_y_q = min(y_q)
min_y_r = min(y_r)
plt.plot(x, y_p, label=f"p(x); min={min_y_p}>0; ({min_y_p>0})")
plt.plot(x, y_q, label=f"q(x); min={min_y_q}>=0; ({min_y_q>=0})")
plt.plot(x, y_r, label=f"r(x); min={min_y_r}>0; ({min_y_r>0})")
plt.plot(x, y_ox, label="ox: y = 0")
plt.legend()
print(f"p(x) >= {min_y_p} > 0 ({min_y_p>0})")
print(f"q(x) >= {min_y_q} >= 0 ({min_y_q>=0})")
print(f"r(x) >= {min_y_r} >= 0 ({min_y_r>0})")
if (min_y_p > 0) and (min_y_q >= 0) and (min_y_r > 0):
    print(f"=> Có thỏa mãn điều kiện")
else:
    raise ValueError(f"=> Ko thỏa mãn điều kiện")
plt.show()


print(
    f"""
# .Xây dựng hệ có dạng 3 đường chéo theo công thức 
"""
)

matrix = np.zeros((n, n))
for i in range(n):
    x_i = a + h * (i + 1)
    if i != 0:
        matrix[i, i - 1] = -p(x_i - h / 2) / (h * h * r(x_i))
    matrix[i, i] = (p(x_i + h / 2) + p(x_i - h / 2)) / (h * h * r(x_i)) - q(x_i) / r(
        x_i
    )
    if i != n - 1:
        matrix[i, i + 1] = -p(x_i + h / 2) / (h * h * r(x_i))


tri_rieng, vecto_rieng = np.linalg.eig(matrix)

for id in range(n):
    λ = tri_rieng[id]
    print(f"Với trị riêng λ = {λ}")
    points = np.zeros((n, 2))
    for i in range(n):
        x_i = a + h * (i + 1)
        points[i, 0] = x_i
        points[i, 1] = vecto_rieng[i, id] / vecto_rieng[0, id]
        print("(", points[i, 0], ", ", points[i, 1], ")") 
 