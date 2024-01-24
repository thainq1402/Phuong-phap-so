import numpy as np
from matplotlib import pyplot as plt

#Input
x0 = 0
y0 = 1
xn = 1
h = 0.1
n = 1 + int((xn - x0)/h)
def f(x,y):
	return  x + y
#
x = np.linspace(x0,xn,n)
y = np.zeros([n])
y[0] = y0
#Tính các giá trị y1,y2,y3 theo RK-4
for i in range(1,4):
	k1 = h*f(x[i-1],y[i-1])
	k2 = h*f(x[i-1]+h/2,y[i-1]+k1/2)
	k3 = h*f(x[i-1]+h/2,y[i-1]+k2/2)
	k4 = h*f(x[i-1]+h,y[i-1]+k3)
	y[i] =  y[i-1] + (k1 + 2*k2 + 2*k3 + k4)/6
#Tính các giá trị còn lại theo AB-4
for i in range(4,n):
    y[i] = y[i-1] + (55*f(x[i-1],y[i-1]) - 59*f(x[i-2],y[i-2]) + 37*f(x[i-3],y[i-3]) - 9*f(x[i-4],y[i-4]))*h/24
print("x_i\t           y_i")
for i in range(n):
	print (format(x[i],'6f'),"\t",format(y[i],'6f'))

plt.plot(x,y,'r')
plt.title("Ngoại suy Adam 4bước")
plt.show()



