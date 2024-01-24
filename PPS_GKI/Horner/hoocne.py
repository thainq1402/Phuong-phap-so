#he so xep tu lon den be
with open('C:\\Users\\Trung Nguyen\\OneDrive\\Desktop\\PPSdithi\\PPS\\Horner\\input.txt') as f:
    coefficientA = [float(x) for x in next(f).split(' ')]

print(coefficientA)

print ("Nhap vao gia tri x: ")
xValue = float(input())

print ("Cap cua dao ham: ")
k = int(input())

def ValueCalculation(coefficientA):
    tempCoefficientB = coefficientA.copy()
    for index in range(1, len(coefficientA)):
        tempCoefficientB[index] = coefficientA[index] + tempCoefficientB[index - 1] * xValue
    return tempCoefficientB

#Tinh dao ham cap k 
#Theo cach thong thuong
def DifferentialCalculation(coefficientA):
    tempCoefficientA = coefficientA.copy()
    for count in range (k):
        for index in range(len(tempCoefficientA)):
            tempCoefficientA[index] = (len(tempCoefficientA) - 1 - index) * tempCoefficientA[index]
        tempCoefficientA.pop(len(tempCoefficientA) - 1)
    return tempCoefficientA
#Theo Horner
def HornerDifferentialCalculation(coefficientA):
    tempCoefficientA = coefficientA.copy()
    for count in range (k + 1):
        tempCoefficientB = tempCoefficientA.copy()
        for index in range(1, len(tempCoefficientA)):
            tempCoefficientA[index] = tempCoefficientB[index] + tempCoefficientA[index - 1] * xValue
        result = tempCoefficientA[-1]
        for i in range (1, k + 1):
            result = result * i
        tempCoefficientA.pop(len(tempCoefficientA) - 1)
    return result

#Nhan da thuc bac n voi da thuc nghiem
def MultipleCalculation (coefficientA):
    tempCoefficientA = coefficientA.copy()
    tempCoefficientA.append(0) 
    tempCoefficientB = tempCoefficientA.copy()
    #tempCoefficientB.append(-xValue * tempCoefficientA[-1])
    for index in range (1, len(tempCoefficientA)):
        tempCoefficientB[index] = tempCoefficientA[index] - tempCoefficientA[index - 1] * xValue
    return tempCoefficientB

result = ValueCalculation(coefficientA)[-1]
print ("Gia tri bieu thuc tai x = {} la {}".format(xValue, result))

print("Da thuc thuong co he so la, so cuoi la so du", ValueCalculation(coefficientA))

print("Tich da thuc do voi da thuc x - {} la {}".format(xValue, MultipleCalculation(coefficientA)))

result = DifferentialCalculation(coefficientA)
print ("He so cua phuong trinh sau dao ham {} la ".format(k, result))
print ("Gia tri dao ham cap {} cua bieu thuc tai x = {} la {}".format(k, xValue, ValueCalculation(result)[-1]))
print ("Gia tri dao ham cap {} cua bieu thuc tai x = {} tinh theo Horner la {}".format(k, xValue, HornerDifferentialCalculation(coefficientA)))