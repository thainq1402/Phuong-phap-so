from math import *

with open('Input.txt','r+') as f:
    x = [float(i) for i in f.readline().split()]
    y = [float(i) for i in f.readline().split()]
a = float(input("Tinh dao ham tai: "))
n = len(x) - 1
h = (x[n]-x[0])/n
t = int((a - x[0])/h)

def HamBac1(): #2 mốc
    if t < n:
        P1 = (y[t+1]-y[t])/h
    if t == n:
        P1 = (y[t]-y[t-1])/h
    print("Gia tri cua dao ham theo xap xi da thuc bac 1 la:",P1)

def HamBac2(): #3 mốc
    # P2 = (y[k]*(2t-3) - y[k+1]*(4t-4) + y[k+2]*(2t-1))/2h
    if t == 0: 
        P2 = (-3*y[t] + 4*y[t+1] - y[t+2])/(2*h)
    if 0 < t < n:
        P2 = (-y[t-1]+ y[t+1])/(2*h)
    if t == n :
        P2 = (y[t-2] -4*y[t-1] + 3*y[t])/(2*h)
    print("Gia tri cua dao ham theo xap xi da thuc bac 2 la:",P2)
 
def HamBac3(): 
      '''4 mốc: (x[k],x[k+1],x[k+2],x[k+3])
         Công thức tổng quát
         P3 = (y[k]*(-11+12t-3t^2) + y[k+1]*(18-30t+9t^2) + y[k+2]*(-9+24t-9t^2) + y[k+3]*(2-6t+3t^2))/6h '''
      if t == 0: #Sử dụng CT tính tại x[k]
        P3 = (-11*y[t] + 18*y[t+1] - 9*y[t+2] + 2*y[t+3])/(6*h)
      if 0 < t < n-1: #Sử dụng CT tính tại x[k+1]
        P3 = (-2*y[t-1] - 3*y[t] + 6*y[t+1] - y[t+2])/(6*h)   
      if t == n - 1:   #Sư dụng CT tính tại x[k+2]
        P3 = (y[t-2] - 6*y[t-1] + 3*y[t] + 2*y[t+1])/(6*h)
      if t == n:   #Sử dụng CT tính tại x[k+3]   
        P3 = (-2*y[t-3] + 9*y[t-2] - 18*y[t-1] + 11*y[t])/(6*h)    
      print("Gia tri cua dao ham theo xap xi da thuc bac 3 la:",P3)

HamBac1()
HamBac2()
HamBac3()





