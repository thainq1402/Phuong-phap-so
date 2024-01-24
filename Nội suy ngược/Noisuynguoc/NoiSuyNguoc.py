from logging import root
from math import *
from operator import index
from tkinter import FALSE, ROUND
import numpy
import matplotlib.pyplot as plt

def input_data():
    arr_x: list[float] = []
    arr_y: list[float] = []
    with open('C:\\Users\\Trung Nguyen\\OneDrive\\Desktop\\PPSdithi\\Noisuynguoc\\input.txt', 'r+') as f:
        for line in f.readlines():
            x_temp = float(line.split(' ')[0])
            y_temp = float(line.split(' ')[1])
            if x_temp in arr_x:
                continue
            arr_x.append(x_temp)
            arr_y.append(y_temp)
    f.close()
    return arr_x, arr_y

# Kiểm tra tính chất cách đều
def Equidistant(arr_x):
    _equidistant = arr_x[1] - arr_x[0]
    _check = 1;
    for i in range(1, len(arr_x)):
        _delta = arr_x[i] - arr_x[i-1]
        if abs(_delta - _equidistant) > 1e-7:
            print("Không cách đều")
            return False
    return True

# Phân hoạch đơn điệu
def Monotonous_Partition(arr): # Phân hoạch đơn điệu
    _extre_idx = [0] # Chỉ số của các điểm cực trị
    for i in range(1, len(arr) - 1):
        if arr[i] > max(arr[i-1], arr[i+1]) or arr[i] < min(arr[i-1], arr[i+1]):
            _extre_idx.append(i)     # Thêm chỉ số điểm cực trị vào vị trí tiếp theo của mảng
        else:
            continue
    _extre_idx.append(len(arr)-1)

    _mono_par = [] # Mảng chứa chỉ số của dãy đơn điệu
    for j in range(len(_extre_idx) - 1):
        _mono_par.append([x for x in range(_extre_idx[j], _extre_idx[j+1] + 1)])

    print("Phân hoạch đơn điệu:", _mono_par, "\n")
    return _mono_par


# Trích ra mảng con gồm các mốc nội suy thích hợp
def Extract_subarr(arr_x1, arr, y):
    # sgn = 1 nếu dãy tăng, sgn = -1 nếu dãy giảm
    _sgn = 1
    if arr[0] > arr[1]: _sgn *= -1
    arr = arr[::_sgn] # Nếu dãy giảm thì dùng [::sgn] để đảo ngược dãy lại thành dãy tăng
    arr_x1 = arr_x1[::_sgn]

    # Tìm chỉ số của 2 giá trị kề với y (Phương pháp chặt nhị phân) <chia đôi đến chết>
    _l_idx = 0
    _r_idx = len(arr) - 1
    while True:
        idx = int((_l_idx + _r_idx) / 2)
        if y > arr[idx]: _l_idx = idx
        else: _r_idx = idx

        if _r_idx - _l_idx == 1: break

    # In mảng con trích xuất (Tối đa 5 phần tử)
    if _l_idx + _r_idx + 1 >= len(arr):   # Trường hợp giá trị gần với y nhất nằm bên phải dãy
        _subarr = [arr[i] for i in range(max(_r_idx - 4, 0), _r_idx + 1)][::-1]
        _subarr_x = [arr_x1[i] for i in range(max(_r_idx - 4, 0), _r_idx + 1)][::-1]
        #_direct = -1
    else:   ## Trường hợp giá trị gần với y nhất nằm bên trái dãy/

        _subarr = [arr[i] for i in range(_l_idx, min(_l_idx + 5, len(arr)))]
        _subarr_x = [arr_x1[i] for i in range(_l_idx, min(_l_idx + 5, len(arr)))]
        #_direct = 1
    
    return [_subarr_x[::_sgn], _subarr[::_sgn]]


def Lagrang(arr_x, arr_y, y):
    _x = 0;
    for i in range(0, len(arr_x)):
        _denominator = 1    # Tử số
        _numerator = 1      # Mẫu số
        for j in range(0, len(arr_y)):
            if i != j:  
                _numerator = _numerator * (y - arr_y[j])        
                _denominator = _denominator * (arr_y[i] - arr_y[j])
        _x = _x + arr_x[i] * (_numerator / _denominator)
    return _x

def Nghiemkhongcachdeu(arr_x, arr_y, y, eps, choose):
    if choose == 2:
        _n = len(arr_x) - 1
        _p_heso = nsNewtonbatky(arr_y, arr_x, _n)
        _sol = P_n(y, _n, _p_heso)
        print("Hệ số: ", _p_heso)
        return _sol
    else:
        _sol = Lagrang(arr_x,arr_y,y)
        return _sol

def Nghiemcachdeu(arr_x, arr_y, y, eps, choose):
    if choose == 1:     # Lặp theo Newton tiến 
        _t = []
        _h = arr_x[1] - arr_x[0]
        for i in arr_x:
            _t.append((i - arr_x[0]) / _h)
        _p_heso = nsNewtontien(_t, arr_y, len(_t) - 1)
        _t0 = (y - arr_y[0]) / (arr_y[1] - arr_y[0])
        _sol = Lapnghiem(_p_heso, _t0, arr_y[1] - arr_y[0], y, eps)
        return arr_x[0] + _h * _sol
    elif choose == 2:       # Lặp theo Newton lùi
        _t = []
        _h = arr_x[1] - arr_x[0]
        _k = len(arr_y)
        for i in arr_x:
            _t.append((i - arr_x[_k - 1]) / _h)
        _p_heso = nsNewtontien(_t, arr_y, _k - 1)
        print("Hệ số: ", _p_heso)
        _t0 = (y - arr_y[_k - 1]) / (arr_y[_k - 1] - arr_y[_k - 2])
        _sol = Lapnghiem(_p_heso, _t0, arr_y[_k - 1] - arr_y[_k - 2], y, eps)
        return arr_x[_k-1] + _h * _sol



def Lapnghiem(p_heso, t0, delta_y, y0, eps):
    _deg = len(p_heso) - 1
    p_heso[_deg-1] = p_heso[_deg - 1] - delta_y
    _t = t0
    while (True):
        _t = (y0 - P_n(_t, _deg, p_heso)) / delta_y
        #print(P_n(_t, _deg, p_heso))
        if abs(_t - t0) < eps:
            break
        t0 = _t
        #print("t = ")
    return _t

def P_n(t, n, p_heso):
    _p = float(0)
    for i in range(n + 1):
        _p += p_heso[i] * t ** (n - i)
    return _p

def nhandathuc(prev, x):
    n = len(prev) + 1
    _xpoly = numpy.zeros(n)
    _xpoly[0] = 1
    _xpoly[n - 1] = -prev[n - 2] * x
    for i in range(1, n - 1):
        _xpoly[i] = -x * prev[i - 1] + prev[i]
    return _xpoly

def Bangtihieu(x, y, n):
    _BTH = numpy.zeros([n + 1, n + 1])
    for i in range(n + 1):
        _BTH[i, 0] = y[i]
    for j in range(1, n + 1):
        for i in range(n + 1 - j):
            _BTH[i, j] = (_BTH[i + 1, j - 1] - _BTH[i, j - 1]) / (x[i + j] - x[i])

    print("Bảng tỉ hiệu \n", _BTH)
    return _BTH[0, :n+1]

def Bangsaiphan(y, n):
    _BSP = numpy.zeros([n + 1, n + 1])
    for i in range(n + 1):
        _BSP[i, 0] = y[i]
    for j in range(1, n + 1):
        for i in range(n + 1 - j):
            _BSP[i, j] = (_BSP[i + 1, j - 1] - _BSP[i, j - 1])
    print("Bảng sai phân \n", _BSP)
    return _BSP[0, :n+1]


def nsNewtonbatky(x, y, n):
    _index = numpy.zeros(n + 1)
    _index[n] = y[0]
    _poly = [1]
    _BTH = Bangtihieu(x, y, n)
    for i in range(1, n + 1):
        _poly = nhandathuc(_poly, x[i - 1])
        for j in range(i + 1):
            _index[n - i + j] = _index[n - i + j] + _BTH[i] * _poly[j]
    return _index

def nsNewtontien(x, y, n):
    _index = numpy.zeros(n + 1)
    _index[n] = y[0]
    _poly = [1]
    _BSP = Bangsaiphan(y, n)
    for i in range(n+1):
        _BSP[i] = _BSP[i] / giaithua(i)
    for i in range(1, n + 1):
        _poly = nhandathuc(_poly, x[i - 1])
        for j in range(i + 1):
            _index[n - i + j] = _index[n - i + j] + _BSP[i] * _poly[j]
    return _index

#Tính giai thừa
def giaithua(n):
    _giai_thua = 1;
    if (n == 0 or n == 1):
        return _giai_thua;
    else:
        for i in range(2, n + 1):
            _giai_thua = _giai_thua * i;
        return _giai_thua;

def graphic(x, y, y0):
    xx = [min(x), max(x)]
    yy = [y0, y0]
    plt.scatter(x, y, s=30, cmap='palete')
    plt.plot(xx, yy)
    plt.show()

# Công thức nội suy ngược
def Inverse_interpolation(arr_x, arr_y, y, eps):
    # Kiểm tra xem giá trị y có nàm ngoài khoảng nội suy hay không
    if y > numpy.max(arr_y) or y < numpy.min(arr_y):
        print("Giá trị y nằm ngoài khoảng nội suy")
        return None
    _root = [] # Các nghiệm của phương trình f(x) = y
    _MPindex = 0;       # Biến đếm của khoảng nghiệm
    #graphic(arr_x, arr_y, y)
    for _idx_arr in Monotonous_Partition(arr_y):
        print("Với dãy đơn điệu có chỉ số", _idx_arr)
        # Nếu y không nằm trong khoảng đơn điệu nào thì loại khoảng đơn điệu đó
        _l = len(_idx_arr)
        arr     = [arr_y[i] for i in _idx_arr]   # Mảng chứa các điểm nội suy trong khoảng đơn diệu (y)
        arr_x1  = [arr_x[i] for i in _idx_arr]
        if y < min(arr_y[_idx_arr[0]], arr_y[_idx_arr[_l-1]]) or y > max(arr_y[_idx_arr[0]], arr_y[_idx_arr[_l-1]]):
            print("f(x) = y vô nghiệm tại khoảng này\n")
            continue

        elif Equidistant(arr_x) == False :  # Nếu không cách đều
            while True:
                print("Chọn phương pháp:")
                print("1. Nội suy Lagrang.")
                print("2. Nội suy Newton.")
                direct = int(input("Lựa chọn: "))
                if direct == 1 or direct == 2:
                    break
            #_root.append(Lagrang(arr_x, arr_y, y))
            x = Nghiemkhongcachdeu(arr_x1, arr, y, eps, direct)
            print("Nghiệm tìm được thứ (", _MPindex+1, "): ", x)
        else:   # Nếu cách đều
            extract = Extract_subarr(arr_x1,arr, y) 
            subarr_x  = extract[0]  
            subarr  = extract[1]            # Các điểm nội suy được chọn (chọn từ điểm gần điểm nội suy nhất)
            
            print("Khoảng tìm nghiệm thứ  (", _MPindex+1, "): ","\nx = ", subarr_x)
            print("y = ", subarr)
            while True:
                print("Chọn phương pháp:")
                print("1. Nội suy Newton tiến.")
                print("2. Nội suy Newton lùi.")
                direct = int(input("Lựa chọn: "))
                if direct == 1 or direct == 2:
                    break

            # Note: "direct" biểu thị hướng đi của công thức nội suy Newton
            #        direct = 1  : Nội suy Newton tiến
            #        direct = 2 : Nội suy Newton lùi
            #print("direct = ", direct)
            x = Nghiemcachdeu(subarr_x, subarr, y, eps, direct)
            print("Nghiệm tìm được thứ (", _MPindex+1, "): ", x)
            _root.append(x)

        _MPindex += 1
    #graphic(arr_x, arr_y, y)
    return _root         

arr_x, arr_y = input_data()
y     = 3.15
eps   = 1e-6 # Sai số

#arr_x = [1, 2, 4]
#arr_y = [2, 5, 23]  # n + 1 mốc nội suy
#y     = 12
#eps   = 0.0000001 # Sai số

#arr_x = [20, 25, 30]
#arr_y = [1.3010, 1.3979, 1.4771]  # n + 1 mốc nội suy
#y     = 1.35
#eps   = 0.0000001 # Sai số

#arr_x = [-1.2, -1, -0.8, -0.6, -0.4, -0.2, 0]
#arr_y = [-0.0188, 0.368, 0.5293, 0.4688, 0.1903, -0.301, -1]  # n + 1 mốc nội suy
#y     = 0.1
#eps   = 0.0000001 # Sai số

#arr_x = [-0.4, -0.35, -0.3, -0.25, -0.2 ]
#arr_y = [0.3376, 0.0886, -0.1309, -0.3242, -0.4944 ] # n + 1 mốc nội suy
#y     = 0
#eps   = 0.0000001 # Sai số
# đáp án x = -0.3305730138924643
            #-0.3304858375797089
            #-0.3305701567794744

#arr_x = [0.3376, 0.0886, -0.1309, -0.3242, -0.4944 ]
#arr_y = [-0.4, -0.35, -0.3, -0.25, -0.2 ] # n + 1 mốc nội suy
#y     = -0.3305730138924643
#eps   = 0.0000001 # Sai số

#arr_x = [0.88, 0.881, 0.882, 0.883]
#arr_y = [2.4109, 2.4133, 2.4157, 2.4181 ] # n + 1 mốc nội suy
#y     = 2.4142
#eps   = 0.0001 # Sai số
#Equidistant(arr_x)
Inverse_interpolation(arr_x, arr_y, y, eps)
#graphic(arr_x, arr_y, y)