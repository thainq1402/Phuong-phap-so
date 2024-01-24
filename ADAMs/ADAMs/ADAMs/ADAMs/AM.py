import numpy as np
from matplotlib import pyplot as plt

#Giá trị nhập vào
x0 = 0
y0 = 1
xn = 1
h = 0.1
n = 1 + int((xn - x0)/h) 

def f(x,y):
    return x + y
#
x = np.linspace(x0,xn,n)
y = np.zeros([n])
y[0] = y0
for i in range(1,n):
    k1 = h*f(x[i-1],y[i-1])
    k2 = h*f(x[i-1]+h/2,y[i-1]+k1/2)
    k3 = h*f(x[i-1]+h/2,y[i-1]+k2/2)
    k4 = h*f(x[i-1]+h,y[i-1]+k3)
    y[i] =  y[i-1] + (k1 + 2*k2 + 2*k3 + k4)/6
    print(y[i])
#Tính các giá trị còn lại bằng AM-4
for i in range(4,n):
    y[i] = y[i-1] + ( 9*f(x[i],y[i]) + 19*f(x[i-1],y[i-1]) - 5*f(x[i-2],y[i-2]) + f(x[i-3],y[i-3]))*h/24 

print("x_i\t         y_i")
for i in range(n):
    print (format(x[i],'6f'),"\t",format(y[i],'6f'))

plt.plot(x,y,'r')
plt.title("Nội suy Adam 4 bước")
plt.show()




