import numpy as np
import matplotlib.pyplot as plt
import math
#Thay doi dau vao
def p (x):
    return 1
def q (x):
    return 4*pow(x, 3)
def f(x):
    return -2/pow(x, 3) + 4*x
a = 1
b = 100
n = 1000
epsilon = 1e-6 #sai so 10^-6

h = (b - a)/(n - 1)

#Thay doi U cho phu hop
matU = [2 for element in range(0, n)]
matA = [[0 for element in range(0, n)] for element in range(0, n)]
matB = [0 for element in range(0, n)]
for i in range (1, n-1):
    matB[i] = - pow(h, 2) * f(a + i*h)
matX = [0 for element in range(0, n)]
for i in range (n):
    matX[i] = a + i * h

def A(matA):
    for i in range (1, n-1):
        matA[i][i-1] = p(a + i*h - h/2)
        matA[i][i+1] = p(a + i*h + h/2)
        matA[i][i] = - matA[i][i-1] - matA[i][i+1] - h*h*q(a+i*h)

# #kiem tra cheo troi hang
# def cheoTroiHang(array):
#     for i in range(len(array)):
#         sumRow = 0 
#         for j in range(len(array)):
#             sumRow = sumRow + np.abs(array[i][j])
#         sumRow = sumRow - np.abs(array[i][i])
#         if np.abs(array[i][i]) <= sumRow:
#             return False
#     return True

# def jacobiRow(A, b, x0, epsilon, n):
#     if (cheoTroiHang(A) == False):
#         print(" Ma tran khong cheo troi hang")
#         return x0
#     else:
#         print(A)
#         print(b)
#         k = 0
#         #tinh ma tran alpha beta
#         for i in range(len(A)):
#             temp = A[i][i]
#             for j in range (len(A)):
#                 A[i][j] = A[i][j] / temp
#             b[i] = b[i] / temp
#         alpha = np.eye(len(A)) - A
#         beta = b.copy()

#         #lap tim x 
#         kt = False
#         while (kt == False and k < n):
#             k = k + 1
#             x = alpha @ x0 + beta
#             print("Lan lap thu", k, ": ", x.transpose())
#             chuan = np.linalg.norm((x - x0), np.inf) / np.linalg.norm((x), np.inf)
#             if (chuan < epsilon):
#                 kt = True
#             else: 
#                 x0 = x  
#         return x

def jacobiRow(A, b, x0, epsilon, n):
    print(A)
    print(b)
    k = 0
        #tinh ma tran alpha beta
    for i in range(len(A)):
        temp = A[i][i]
        for j in range (len(A)):
            A[i][j] = A[i][j] / temp
        b[i] = b[i] / temp
    alpha = np.eye(len(A)) - A
    beta = b.copy()
    #quy = np.linalg.norm(alpha, np.inf) #Tinh chuan vo cung

        #lap tim x 
    kt = False
    while (kt == False and k < n):
        k = k + 1
        x = alpha @ x0 + beta
        print("Lan lap thu", k, ": ", x.transpose())
        chuan = np.linalg.norm(((x - x0) / (x)), np.inf)
        #chuan = np.linalg.norm((x - x0),np.inf)
        #if (quy * chuan /(1 - quy)) <= epsilon:
        if (chuan < epsilon):
            kt = True
        else: 
            x0 = x  
    return x

def BaiToanBienLoai1():
    matA1 = matA.copy()
    matB1 = matB.copy()
    matU1 = matU.copy()

    alpha = float(input("alpha = "))
    beta =  float(input("beta = "))

    A(matA1)

    matA1[0][0] = 1
    matA1[n-1][n-1] = 1
    matB1[0] = alpha
    matB1[n-1] = beta

    U = jacobiRow(matA1, matB1, matU1, epsilon, n)
   
    return U

def BaiToanBienLoai23():
    matA2 = matA.copy()
    matB2 = matB.copy()
    matU2 = matU.copy()

    xichma1 = float(input("xichma1 = "))
    xichma2 =  float(input("xichma2 = "))
    muy1 = float(input("muy1 = "))
    muy2 = float(input("muy2 = "))
  
    A(matA2)

    matA2[0][0] = -p(a+h/2) - (pow(h, 2)/2)*q(a) - xichma1
    matA2[0][1] = p(a+h/2) 
    matA2[n-1][n-2] = -p(b-h/2)
    matA2[n-1][n-1] = p(b-h/2) + (pow(h, 2)/2)*q(b) - xichma2
    matB2[0] = -(pow(h, 2)/2)*f(a) - muy1*h
    matB2[n-1] = (pow(h, 2)/2)*f(b) - muy2*h

    U = jacobiRow(matA2, matB2, matU2, epsilon, n)
   
    return U

def BaiToanHonHopLoai1va23():
    matA4 = matA.copy()
    matB4 = matB.copy()
    matU4 = matU.copy()

    alpha = float(input("alpha = "))
    xichma2 =  float(input("xichma2 = "))
    muy2 = float(input("muy2 = "))

    A(matA4)

    matA4[0][0] = 1
    matA4[n-1][n-2] = -p(b-h/2)
    matA4[n-1][n-1] = p(b-h/2) + (pow(h, 2)/2)*q(b) - xichma2
    matB4[0] = alpha
    matB4[n-1] = (pow(h, 2)/2)*f(b) - muy2*h

    U = jacobiRow(matA4, matB4, matU4, epsilon, n)
   
    return U

def BaiToanHonHopLoai23va1():
    matA5 = matA.copy()
    matB5 = matB.copy()
    matU5 = matU.copy()

    xichma1 = float(input("xichma1 = "))
    muy1 = float(input("muy1 = "))
    beta =  float(input("beta = "))


    A(matA5)

    matA5[0][0] = -p(a+h/2) - (pow(h, 2)/2)*q(a) - xichma1
    matA5[0][1] = p(a+h/2) 
    matA5[n-1][n-1] = 1
    matB5[0] = -(pow(h, 2)/2)*f(a) - muy1*h
    matB5[n-1] = beta

    U = jacobiRow(matA5, matB5, matU5, epsilon, n)
   
    return U


bai_toan = int(input("Nhap bai toan bien = "));

if (bai_toan == 1):
    U = BaiToanBienLoai1()
if (bai_toan == 2 or bai_toan == 3):
    U = BaiToanBienLoai23()
if (bai_toan == 4):
    U = BaiToanHonHopLoai1va23()
if (bai_toan == 5):
    U = BaiToanHonHopLoai23va1()

print ("u = ", U)

plt.plot(matX, U)
plt.show()


