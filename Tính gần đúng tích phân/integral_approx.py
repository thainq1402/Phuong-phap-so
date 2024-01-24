from sympy import sympify, symbols
from sympy import *
import math


#region Công thức hình thang DONE


def CthucHinhThang(A):    
    trapezoidal  = 1/2*(A[0] + A[n])
    for i in range(1, n):
        trapezoidal  = trapezoidal  + A[i]
    #print(f"Tích phân bằng công thức hình thang {trape*h}")
    return trapezoidal*h

def CthucHinhThangSaiSo(): # hàm tính sai số 
    m = max(f, 2)
    #print(f"Sai số công thức hình thang :  {m/12*(b-a)*(h**2)}")
    return m/12*(b-a)*(h**2)

def CthucHinhThang_KhoangChia(): # số khoảng chia thỏa mãn sai số cho trước
    """ Số khoảng chia để thỏa mãn sai số cho trước trong công thức hình thang"""
    m = max(f, 2)
    khoang_chia = math.floor((abs(((m*(b-a)**3)*(1/12)*(1/eps))))**(1/2))+1 
    #print("Số khoảng chia cần thiết (Hình thang)    :",math.floor((abs(((m*(b-a)**3)*(1/12)*(1/eps))))**(1/2))+1)
    return khoang_chia
#endregion
#region Công thức Simpson DONE
# Công thức Simpson

def CthucSimpson(A): # Tính gần đúng tích phân xác định bằng công thức Simpson
    simpson = h/3*(A[0]+A[n])
    simp_le = 0
    simp_chan = 0        
    for i in range(1, n, 2):
        simp_le += A[i]
    for i in range(2, n, 2):
        simp_chan += A[i]
    simpson = simpson + h/3*4*simp_le + h/3*2*simp_chan
    return simpson

def CthucSimpsonSaiSo(): # Sai số của công thức Simpson
    epxilon = max(f, 4)
    return  epxilon/180*(b-a)*(h**4)

def Simpson_KhoangChia(): # số khoảng chia thỏa mãn sai số cho trước trong công thức Simpson
    m = max(f, 4)
    n = math.floor((abs((m*(b-a)**5)*(1/180)*(1/eps)))**(1/4))+1
    if n % 2 == 1:
        n=n+1
    else:
        n=n+2
    return n
    
#endregion
#region Công thức Newton - Cotes

def Hoocne_nhan(A, i) -> list: # Hàm nhân đa thức Hocnne
    A.append(0)
    for j in range(len(A)-1,0,-1):
        A[j] = A[j] - A[j - 1] * i
    return A

def Hoocne_chia(A, i) -> list: # Hàm hoocne chia
    X = A.copy()
    X.pop()
    for j in range(1, len(X)):
        X[j] = i*X[j-1] + X[j]
    return X

def Ham_tich_phan(A, a, b) -> float: # Hàm tính tích phân
    I = 0
    for j in range(0, len(A)):
        if (A[j] == 0):
            continue
        else:
            A[j] = A[j]/(len(A)-j)     
        I = I + A[j]*(b**(len(A)-j)-a**(len(A)-j))
    return I

def cotez_coef(i) -> float: # Hàm tính hệ số Hi của Newton Cotez
   
    X = Hoocne_chia(D, i)
    h = (1/n)*((-1)**(n-i))/(math.factorial(i)*math.factorial(n-i))*Ham_tich_phan(X, 0, n) # tìm h i 
    return h


    """
    D là tích các đa thức (t-j), j từ 0 đến n, nhưng để tiết kiệm thời gian, tính 
    nó một lần duy nhất ở dưới.
    """
    
def Cthuc_NewCot() -> float: # Hàm tính tích phân Newton Cotez
    E = 0
    Hs = [1]*(n+1)
    for i in range(0, n+1):
        Hs[i]   = cotez_coef(i)
        E       = E + Hs[i]*A[i]
    print(f'Hệ số Cotes ứng với n = {n}:',Hs)
    return E*(b-a)

def Cthuc_NewCot_SaiSo() -> float: # Sai sô Newton Cotez
    g = Derivative(f,(x, n), evaluate=True)
    error = 0 
    if (n % 2 == 0):
        D1 = D.copy()
        Hoocne_nhan(D1, n+1)
        m2 = max(g, 2)
        error = abs(float(m2)*Ham_tich_phan(D1, 0, n)*(h**(n+3))/math.factorial(n+2))
    else:
        m1 = max(g, 1)
        error = abs(float(m1)*Ham_tich_phan(D, 0, n)*(h**(n+2))/math.factorial(n+1))
    return error


def max(fx, i): # Tìm max của đạo hàm cấp i 
    g   = Derivative(fx,(x, i), evaluate=True)
    m1  = abs(maximum(g, x, Interval(a, b)))
    m2  = abs(minimum(g, x, Interval(a, b)))
    if m1 > m2:
        m = m1
    else:
        m = m2
    return m

#endregion


#region Xap xi tich phan 
def main():
    global n, a, b, f, h, x, D, A, eps
    x           = symbols('x')
    func        = input('Nhập hàm f(x): ')
    f           = sympify(func)
    init_value  = input('Nhập khoảng lấy tích phân: ')


    a, b        = [float(i) for i in init_value.split()] # lưu khoảng lấy tích phân 
    ques  = int(input('Chọn phương pháp xấp xỉ : \n\t1.Hình thang \n\t2.Simpson \n\t3.Newton Cotez\n'))

    if ques == 1:
        eps = float(input('Nhập epsilon: ')) 
        n = CthucHinhThang_KhoangChia()
        h = (b-a)/n
        D = [1]
        for i in range(0, n+1):
            Hoocne_nhan(D, i)                           # Tích các (t-j), j từ 0 đến n
        
        A = [f.subs(x,a+i*h) for i in range(n+1)]     # Tạo mảng lưu giá trị hàm tại các mốc nội suy
        print(f"Xấp xỉ bằng Hình Thang: {CthucHinhThang(A)}")
        print(f"Sai số công thức hình thang: {CthucHinhThangSaiSo()}")
    elif ques == 2:
        eps = float(input('Nhập epsilon: ')) 
        n = Simpson_KhoangChia() # nếu đề bài cho khoảng chia thì comment 2 dòng này 
        n=int(input('Nhập khoảng chia'))
        h = (b-a)/n
        D = [1]
        for i in range(0, n+1):
            Hoocne_nhan(D, i)                           # Tích các (t-j), j từ 0 đến n
        
        A = [f.subs(x,a+i*h) for i in range(n+1)]     # Tạo mảng lưu giá trị hàm tại các mốc nội suy
        print(f"Xấp xỉ bằng Simpson: {CthucSimpson(A)}")
        print(f"Sai số công thức Simpson: {CthucSimpsonSaiSo()}")
    elif ques == 3 :
        n       = int(input('Nhập số khoảng chia n : ')) # nhập số khoảng chia trong Newton Cotez 
        h       = (b-a)/n
        D       = [1]
        for i in range(0, n+1):
            Hoocne_nhan(D, i)                           # Tích các (t-j), j từ 0 đến n
        
        A       = [f.subs(x,a+i*h) for i in range(n+1)]     # Tạo mảng lưu giá trị hàm tại các mốc nội suy

        print(f"Xấp xỉ bằng công thức Newton Cotez: {Cthuc_NewCot()}")
        print(f"Sai số công thức Newton Cotez: {Cthuc_NewCot_SaiSo()}")
#endregion


if __name__ == '__main__':
    main()






































#region Tính tích phân
# def main():
#     global n, a, b, f, h, x, D, A, eps
#     x           = symbols('x')
#     func        = input('Nhập hàm f(x): ')
#     f           = sympify(func)
#     # init_value  = input('Nhập khoảng lấy tích phân a, b (a < b) cách nhau bởi dấu cách: ')
#     init_value  = input('Nhập khoảng lấy tích phân: ')


#     a, b        = [float(i) for i in init_value.split()] # lưu khoảng lấy tích phân 
#     q           = int(input('Chọn bài toán bạn muốn giải quyết (Nhập số theo bài toán)''\n''(1) Tính tích phân (2) Tính số khoảng chia cần thiết: '))
    
#     if q == 1:
#         n       = int(input('Nhập số khoảng chia n: '))
#         h       = (b-a)/n
    
#         D       = [1]
#         for i in range(0, n+1):
#             Hoocne_nhan(D, i)                           # Tích các (t-j), j từ 0 đến n
        
#         A       = [f.subs(x,a+i*h) for i in range(n+1)]     # Tạo mảng lưu giá trị hàm tại các mốc nội suy

#         if n % 2 == 0:
#             print(f"Xấp xỉ bằng công thức hình thang: {CthucHinhThang(A)}")
#             print(f"Sai số công thức hình thang : {CthucHinhThangSaiSo()}")
#             print("===============")
#             print(f"Xấp xỉ bằng công thức Simpson: {CthucSimpson(A)}")
#             print(f"Sai số công thức Simpson{CthucSimpsonSaiSo()}")
#             print("==============")
#             print(f"Xấp xỉ bằng công thức Newton Cotez: {Cthuc_NewCot()}")
#             print(f"Sai số công thức Newton Cotez: {Cthuc_NewCot_SaiSo()}")
#         else:
#             print(f"Tính tích phân bằng công thức hình thang: {CthucHinhThang(A)}")
#             print(f"Sai số công thức hình thang : {CthucHinhThangSaiSo}")
#             print("===============")
#             print(f"Xấp xỉ bằng công thức Newton Cotez: {Cthuc_NewCot()}")
#             print(f"Sai số công thức Newton Cotez: {Cthuc_NewCot_SaiSo()}")

# #endregion
# #region Tính khoảng chia cần thiết để đạt epxilon
#     if q == 2:
#         eps     = float(input('Nhập epsilon: ')) 
#         print(f"Số khoảng chia công thức Hình Thang: {CthucHinhThang_KhoangChia()}")
#         print(f"Số khoảng chia công thức Simpson: {Simpson_KhoangChia()}")
#endregion

       
#     if q == 1:
#         n       = int(input('Nhập số khoảng chia n: '))
#         h       = (b-a)/n
    
#         D       = [1]
#         for i in range(0, n+1):
#             multiply_horner(D, i)                           # Tích các (t-j), j từ 0 đến n
        
#         A       = [f.subs(x,a+i*h) for i in range(n+1)]     # Tạo mảng lưu giá trị hàm tại các mốc nội suy

#         if n % 2 == 0:
#             print(f"Xấp xỉ bằng công thức hình thang: {CthucHinhThang(A)}")
#             print(f"Sai số công thức hình thang : {CthucHinhThangSaiSo()}")
#             print("===============")
#             print(f"Xấp xỉ bằng công thức Simpson: {CthucSimpson(A)}")
#             print(f"Sai số công thức Simpson{CthucSimpsonSaiSo()}")
#             print("==============")
#             print(f"Xấp xỉ bằng công thức Newton Cotez: {Cthuc_NewCot()}")
#             print(f"Sai số công thức Newton Cotez: {Cthuc_NewCot_SaiSo()}")
#         else:
#             print(f"Tính tích phân bằng công thức hình thang: {CthucHinhThang(A)}")
#             print(f"Sai số công thức hình thang : {CthucHinhThangSaiSo}")
#             print("===============")
#             print(f"Xấp xỉ bằng công thức Newton Cotez: {Cthuc_NewCot()}")
#             print(f"Sai số công thức Newton Cotez: {Cthuc_NewCot_SaiSo()}")

# #endregion
# #region Tính khoảng chia cần thiết để đạt epxilon
#     if q == 2:
#         eps     = float(input('Nhập epsilon: ')) 
#         print(f"Số khoảng chia công thức Hình Thang: {CthucHinhThang_KhoangChia()}")
#         print(f"Số khoảng chia công thức Simpson: {Simpson_KhoangChia()}")
# #endregion
