import math as math
from math import *
import numpy as np
import matplotlib.pyplot as plt
import sys
import pandas as pd
from pandas import *

np.set_printoptions(suppress=True, linewidth=np.inf, precision=8     ) #chỉnh số chữ số sau dấu phẩy

def Input():  #input đc sắp xếp tăng dần và cách đều
    x, y = [], []
    with open('input1.txt','r+') as f: # đọc file input
        for line in f.readlines(): # duyệt từng hàng trong file
            if float(line.split()[0]) not in x:
                x.append(float(line.split()[0]))
                y.append(float(line.split()[1]))
    for i in range(1, len(x)): # kiếm tra điều kiện cách đều
        if abs(x[i] - x[i-1] - (x[1] - x[0])) > 1e-6:
            print("Input không hợp lệ!")
            sys.exit()
    return x, y


#chọn ra sô điểm gần x0 nhất ( số lượng nhập từ bàn phím )
def Chon_diem(x0, num, x, y):
    if num > len(x):
        print("Error!!!")
        sys.exit()
    h= x[1]-x[0] # khoảng cách các mốc nội suy
    i = int((x0 - x[0])/h)  #x0 thuộc (x[i], x[i+1]) phép đổi biến theo t
    left = min(len(x) - num, max(0, i + 1 - int(num/2)))
        #max để xứ lí TH x0 < x[0], min xử lí TH x0 > x[n]
    right = left + num - 1
        #num điểm gần x0 nhất nằm trong đoạn x[left] đến x[right]
    x1, y1 = [], []
    x1[:] = x[left: right+1]
    y1[:] = y[left: right+1]
    return x1, y1

def  He_So(BSP,y1):
    size=len(y1)
    _he_so = np.zeros(size)
    x=np.zeros(size)
    _Matran_heso=np.zeros([size-1,size])

    #tạo 1 mảng lưu các hệ số của đa thức nhân 
    for i in range(size):
       x[i]=i
    #tính toán và gán các hệ số vào ma trận 
    for i in range(size-1):
        x_poly=np.zeros(i+1)
        for j in range(i+1):
            x_poly[j]=x[j]
        x_poly=np.poly(x_poly)
    #Gán vào ma trận hệ số 
        k = size-len(x_poly) #vị trí bắt đầu gán 
        len_x_poly = len(x_poly)  #vị trí dừng lặp 
        for m in range(len_x_poly):
            _Matran_heso[j,k+m] = x_poly[m]

    #copy hàng đầu bảng sai phân sang mảng
    _he_so[0]=y1[0]
    for i in range(1,size):
        _he_so[i]=BSP[0,i]/math.factorial(i)

    
    #Nhân BSP vào ma trận trên 
    for i in range(1,size): # chuyển từ sai phân cấp n sang sp n+1 ở _he_so và xuống dòng
        for j in range(size): # chuyển các phần từ cột 
            _Matran_heso[i-1,j]=_he_so[i]*_Matran_heso[i-1,j]

    # Cộng các hàng lại, chưa gán hệ số đa thức bằng y1 hay y_n tùy vào tiến or lùi 
    _he_so_da_thuc = np.zeros(size)
    sum = 0.0

    for i in range(size): # duyệt theo cột 
        for j in range(size-1):
            sum = sum + _Matran_heso[j,i]
        _he_so_da_thuc[i] = sum 
        sum=0

    _he_so_da_thuc[size-1]=y1[0]

    return _he_so_da_thuc

    
def Bang_sai_phan(y1):
    size=len(y1)
    _Coef = np.zeros([size,size])
    #copy vecto cot y vao hang dau bang sai phan 
    for i in range(size):
        _Coef[i,0]=y1[i]
    for i in range(size-1):
        for j in range(size-i-1):
            _Coef[j,i+1]=_Coef[j+1,i]-_Coef[j,i]
    return _Coef

def Xap_xi(Heso,x0,x1):
    size = len(Heso)
    _t = (x0-x1[0])/(x1[1]-x1[0])
    #hoocne
    b=np.zeros(size)
    b[0]=Heso[0]
    for i in range(1,size):
        b[i]=Heso[i]+b[i-1]*_t
    return b[size-1]

def main():
    x,y =  Input()
    x0 = float(input("Nhập giá trị cần xấp xỉ : ")) # giá trị cần xấp xi tại x0

    num = int(input(f"\nChọn số lượng mốc nội suy muốn tính (<= {len(x)}): ")) 

    x1,y1=Chon_diem(x0,num,x,y)
     
    print("Các mốc nội suy : ")
    print(f"{x1} \n ")
    print(f"{y1} \n")

    BSP = Bang_sai_phan(y1)
    print("Bảng sai phân : ")
    print(f" {BSP} \n")


    He_so_da_thuc = He_So(BSP,y1)
    print(f"Hệ số của đa thức nội suy ( từ bậc cao nhất ) : \n {He_so_da_thuc} \n")

    print(f"Đổi biến :  t = (x - {x1[0]})/{round(x1[1]-x1[0], 6)} \n")

    value = Xap_xi(He_so_da_thuc,x0,x1)

    print(f"Giá trị xấp xỉ là : {value}")

   
if __name__=='__main__':
    main()

