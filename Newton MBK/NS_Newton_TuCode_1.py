import math as math
from math import *
import numpy as np
import matplotlib.pyplot as plt
import sys
import pandas as pd
from pandas import *


import cProfile
from ctypes import sizeof

def Input():
    x_t: list[float] = []
    y_t: list[float] = []
    with open('C:\\Users\\Trung Nguyen\\OneDrive\\Desktop\\PhuongPhapSo\\IdolNguyenQuocThai\\Module_MBK\\input.txt', 'r+') as f:
        for line in f.readlines():
            x_temp = float(line.split(' ')[0])          
            y_temp = float(line.split(' ')[1])           
            if x_temp in x_t:
                continue
            x_t.append(x_temp)
            y_t.append(y_temp)
    f.close()
    bubbleSort(x_t,y_t)
    return x_t, y_t # cac moc noi suy duoc lay vao 2 mang 
# Python program for implementation of Bubble Sort

def bubbleSort(arr_1,arr_2):
    n = len(arr_1)
    swapped = False
    for i in range(n-1):   
        for j in range(0, n-i-1):
            if arr_1[j] > arr_1[j + 1]:
                swapped = True
                arr_1[j], arr_1[j + 1] = arr_1[j + 1], arr_1[j]
                arr_2[j], arr_2[j + 1] = arr_2[j + 1], arr_2[j]      
        if not swapped:
            return

def Chon_diem(x0, num, x, y):
    if num > len(x):
        print("Error!!!")
        sys.exit()
    h= x[1]-x[0] # khoảng cách các mốc nội suy
    i = int((x0 - x[0])/h)  #x0 thuộc (x[i], x[i+1]) phép đổi biến theo 
    left = min(len(x) - num, max(0, i + 1 - int(num/2)))
        #max để xứ lí TH x0 < x[0], min xử lí TH x0 > x[n]
    right = left + num - 1
        #num điểm gần x0 nhất nằm trong đoạn x[left] đến x[right]
    x1, y1 = [], []
    x1[:] = x[left: right+1]
    y1[:] = y[left: right+1]
    return x1, y1

def Nhan_Da_Thuc(prev, x):
    n = len(prev) + 1
    x_poly = np.zeros(n)
    x_poly[0] = 1
    x_poly[n-1] = -prev[n-2]*x
    for i in range(1, n-1):
        x_poly[i] = -x*prev[i-1] + prev[i]
    return x_poly

#Bo n vi truyen vao x nen co the tao 1 bien local n=len(x)
def NS_Newton(x, y, Coef, n):    #n là bậc của đa thức nội suy 
    he_so = np.zeros(n+1)       # Tạo 1 array n+1 phần tử 
    he_so[n] = y[0]             # phần tử index[n] = y0 <=> ao
    poly = [1] 
    for i in range(1, n+1): 
        poly = Nhan_Da_Thuc(poly, x[i-1])
        for j in range(i+1):
            he_so[n-i+j] = he_so[n-i+j] + Coef[0, i]*poly[j]
    return he_so, poly

#Bảng tỷ sai phân
def Bang_Ty_Sai_Phan(x,y,n): # n la deg -1 
    Coef = np.zeros([n+1,n+1]) # Ma trận tỷ sai phân
    #Copy vecto y vao cot dau tien cua bang tsp
    for i in range(n+1):
        Coef[i,0] = y[i]
    for j in range(1,n+1):
        for i in range(0,n+1-j):
            Coef [i,j]= (Coef[i+1,j-1]-Coef[i,j-1])/(x[j+i]-x[i])
    return Coef # Ma trận tỷ sai phân

def He_So_Da_Thuc(x,Coefficient,y_0) : # Input Vecto x, Bang ty sai phan 
    len_x=len(x)
    Matran_heso=np.zeros([len_x-1,len_x]) # ma trận chứa các hệ số của đa thức t(t-1)(t-2)....

    for j in range(0,len_x-1):      
        # tạo mảng 1 chiều lưu các giá trị từ vecto X
        x_poly=np.zeros(j+1)   
        #copy tu X_vecto sang 
        for i in range(0,j+1):
            x_poly[i]=x[i]
        # Sử dụng thư viện để tính các hệ số 
        x_poly=np.poly(x_poly)

        # Gán vào ma trận hệ số 
        k = len_x-len(x_poly) # vị trí bắt đầu gán
        len_x_poly = len(x_poly) # vị trí dừng lặp
        for m in range(0, len_x_poly):       
            Matran_heso[j][k+m] = x_poly[m]

    #Nhan ty sai phan với bảng ma trận hệ số 
    for i in range(len_x-1):
        for j in range(len_x):
            Matran_heso[i,j]=Matran_heso[i,j]*Coef[0,i+1]
    

    #Cộng các hàng của ma trận hệ số
    for i in range (len_x):
        sum=0
        for j in range(len_x-1):
            sum=sum+Matran_heso[j,i]
            Matran_heso[0,i]=sum

    #Gan gia tri y_0 vao bang 
    Matran_heso[0,len_x-1]=Matran_heso[0,len_x-1]+y_0

    return Matran_heso

#xap si ham x*sin(2*x+pi/4)
def Toi_Uu_Loai_1(x,y):
    n=len(x)
    #Moc noi suy toi uu 
    x_new = x  
    y_new = y

    for i in range(n):
        x_new[i]=math.cos((2*i+1)*math.pi/(2*n))
    #Gia tri noi suy toi uu 
        y_new[i]=x[i]*math.sin(2*x[i]+math.pi/4)+1
        #y_new[i]=1/(25*pow(x[i],2)+1)

    return x_new,y_new
   
def Toi_Uu_Loai_2(x,y):
    n=len(x)

    #Moc noi suy toi uu loai 2
    x_new=x
    x_new.sort()
    y_new=y

    for i in range(n):
        x_new[i] = 0.5*((x[n-1]-x[0])*math.cos((2*i+1)*math.pi/(2*n))+(x[n-1]-x[0]))
        y_new[i]=x_new[i]*math.sin(2*x_new[i]+math.pi/4) + 1 # chinh sua ham xap xi 
    return x_new,y_new

def Hoocne(x,a): # poly là hệ số của đa thức
    b=np.zeros(len(a))
    b[0]=a[0]
    size =  len(a)
    for i in range(1,size):
        b[i]=a[i]+b[i-1]*x
    return b[size-1] #b la 1 mang


if __name__ == "__main__":
    x,y = Input()
    
    num=int(input("Nhập số mốc nội suy cần dùng : "))
    Xap_xi = float(input("Nhap gia tri xap xi : "))
    x1,y1=Chon_diem(Xap_xi,num,x,y)
    deg=len(x1)-1
    print("Các mốc nội suy : ")
    print(x1)
    print(y1)

    print("\n Da thuc P(n) bậc : "+str(deg) )

    Coef = Bang_Ty_Sai_Phan(x1,y1,deg) # Bang ty sai phan
    he_so,poly=NS_Newton(x1,y1,Coef,deg) # Tinh he so cua da thuc noi suy 

    print(DataFrame(Coef))
    print()
    print(he_so) # He so da thuc noi suy rut gon 

 
    #Gia_tri=Hoocne(Xap_xi,he_so)
    print(Hoocne(Xap_xi,he_so))

    # Matran_heso = He_So_Da_Thuc(x,Coef,y[0]) # output : ma tran ty sai phan + he so da thuc noi suy 
    # print(DataFrame(Matran_heso))









