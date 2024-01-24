import numpy as np
import matplotlib.pyplot as plt

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

def Binary_search(Gtri_xapxi,array,low,high):
    mid=(low+high)//2 # never over flow
    #print(mid)
    #base case
    if low == high :
        return low
    else:
        if array[mid] < Gtri_xapxi :
            return Binary_search(Gtri_xapxi,array,mid+1,high)
        elif array[mid] == Gtri_xapxi:
            return mid
        else:
            return Binary_search(Gtri_xapxi,array,low,mid)
#input : num- số mốc nội suy cần dùng
         #x,y : các mốc nội suy 
#output :  các mốc nội suy xung quanh tri xấpxi
def Chon_diem(Gtri_xapxi,num,x,y):
    size=len(x)
    index = Binary_search(Gtri_xapxi,x,0,size-1)
    left=max(0,index-int((num/2))) 
    right = min(size-1,num+left-1)
    x1, y1 = [], []
    x1[:] = x[left: right+1] 
    y1[:] = y[left: right+1]
    return x1,y1

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

def P_n(x, n, index):
    p = 0
    for i in range(n+1):
        p += index[i]*x**(n-i)
    return p

def choose():
    print("")
    print("1. Thêm mốc nội suy?")
    print("2. Kết thúc.")
    choose = int(input("Lựa chọn: "))
    return choose

def Bang_Sai_Phan(x, y, n):
    BSB = np.zeros([n + 1, n + 1])
    for i in range(n + 1):
        BSB[i, 0] = y[i]
    for j in range(1, n + 1):
        for i in range(n + 1 - j):
            BSB[i, j] = (BSB[i + 1, j - 1] - BSB[i, j - 1]) / (x[i + j] - x[i])
    return BSB

def nhandathuc(prev, x):
    n = len(prev) + 1
    xpoly = np.zeros(n)
    xpoly[0] = 1
    xpoly[n-1] = -prev[n-2]*x
    for i in range(1, n-1):
        xpoly[i] = -x*prev[i-1] + prev[i]
    return xpoly

def NS_Newton(x, y, BSB, n):
    he_so = np.zeros(n+1)
    he_so[n] = y[0]
    poly = [1]
    for i in range(1, n+1):
        poly = nhandathuc(poly, x[i-1])
        for j in range(i+1):
            he_so[n-i+j] = he_so[n-i+j] + BSB[0, i]*poly[j]
    return he_so, poly

def Hoocne(x,a): # poly là hệ số của đa thức
    b=np.zeros(len(a))
    b[0]=a[0]
    size =  len(a)
    for i in range(1,size):
        b[i]=a[i]+b[i-1]*x
    return b[size-1] #b la 1 mang
 
def addData(x, y, BSB, n):
    with open('C:\\Users\\Trung Nguyen\\OneDrive\\Desktop\\20221\\PPS\\Module_MBK\\addData.txt', 'r+') as f:
        for line in f.readlines():
            x_temp = float(line.split(' ')[0])
            y_temp = float(line.split(' ')[1])
            if x_temp in x:
                continue
            x.append(x_temp)
            y.append(y_temp)
    f.close()
    m = len(x) - n - 1
    BSB_new = np.zeros([n+m+1, n+m+1])
    for i in range(n+1):
        BSB_new[i, :] = np.hstack([BSB[i, :], np.zeros(m)])
    BSB_new[:, 0] = np.transpose(y)
    for j in range(1, n+m+1):
        if j >= n+1:
            k = 0
        else:
            k = n+1-j
        for i in range(k, n+m+1-j):
            BSB_new[i, j] = (BSB_new[i+1, j-1] - BSB_new[i, j-1]) / (x[i+j] - x[i])
    return BSB_new, x, y, m

def addnsNewton(x, BSB, m, n, he_so, poly):
    for i in range(m):
        poly = nhandathuc(poly, x[n+i])
        he_so = np.hstack([[0], he_so]) + BSB[0, n+i+1]*poly
    return he_so

# def drawgraph(x, y, n, he_so, choose):
    xx = np.linspace(min(x)-0.5, max(x)+0.5, 100)
    plt.figure()
    plt.scatter(x, y, marker='*')
    plt.plot(xx, f(xx))
    plt.plot(xx, P_n(xx, n, he_so))
    plt.grid()
    plt.xlabel('Points')
    plt.ylabel('Values')
    if not choose:
        plt.savefig("mygraph.png")
    else:
        plt.savefig("mygraph1.png")
if __name__ == "__main__":
    x, y = Input()

    num=(int(input("Số mốc nội suy muốn sư dụng : ")))
    xap_xi=(float(input("Nhập điểm cần xấp xỉ : ")))

    x1,y1=Chon_diem(xap_xi,num,x,y)

    print(f"Mốc nội suy sử dụng : \n{x1}\n{y1}")

    deg = len(x1) - 1
    print("Bậc đa thức P_n: ", deg)

    he_so = np.zeros(deg+1)
    BSB = Bang_Sai_Phan(x1, y1, deg)
    print(f"Bảng tỷ sai phân : \n{BSB} ")
    he_so, poly = NS_Newton(x1, y1, BSB, deg)
    print(he_so) # hệ số của đa thức nội suy từ cao -> thấp
    
    result = Hoocne(xap_xi,he_so)
    print(f"Giá trị xấp xỉ : {result} ")
    # drawgraph(x, y, deg, he_so, 0)

    choose = choose()

    if choose == 1:
        BSB, x1, y1, num_add = addData(x, y, BSB, deg)
        he_so = addNS_Newton(x1, BSB, num_add, deg, he_so, poly)
        print("Đa thức sau khi thêm mốc nội suy (bậc {0}): {1}".format(deg+num_add, he_so))
        #drawgraph(x, y, deg+num_add, he_so, 1)