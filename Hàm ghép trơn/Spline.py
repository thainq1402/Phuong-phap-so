import numpy as np
import matplotlib.pyplot as plt

# region Xu ly du lieu
def data():
    global x,y,size
    x = []
    y = []
    with open('C:\\Users\\Nguyen Quoc Thai\\OneDrive\\Desktop\\PPSdithi\\Hàm ghép trơn\\VD1.txt','r+') as f:
        for line in f.readlines():
            x.append(float(line.split(' ')[0]))
            y.append(float(line.split(' ')[1]))            
    x = np.asarray(x)
    y = np.asarray(y)
   
    return x,y
def bubble_sort(arr_1,arr_2):
    n = len(arr_1)
    swapped = False
    for i in range(n-1):
        for j in range(0, n-i-1):
            if arr_1[j] > arr_1[j + 1]:
                swapped = True
                arr_1[j], arr_1[j + 1] = arr_1[j + 1], arr_1[j]
                arr_2[j], arr_2[j + 1] = arr_2[j + 1], arr_2[j]
        if not swapped:
            break
    return arr_1, arr_2

# def bubble_sort(arr_1,arr_2): # ham sap xep cac moc noi suy tang dan 
#     n = len(arr_1)
#     swapped = False
#     for i in range(n-1):   
#         for j in range(0, n-i-1):
#             if arr_1[j] > arr_1[j + 1]:
#                 swapped = True
#                 arr_1[j], arr_1[j + 1] = arr_1[j + 1], arr_1[j]
#                 arr_2[j], arr_2[j + 1] = arr_2[j + 1], arr_2[j]      
#         if not swapped:
#             return arr_1,arr_2

def binary_search(Gtri_xapxi,array,low,high): # OK
    mid=(low+high)//2 # never over fvi_tri
    #base case
    if low == high : # sau khi thu gọn đến mức vi_tri == high sẽ tự return điểm gần x0 nhất 
        return low
    else:
        if array[mid] < Gtri_xapxi :
            return binary_search(Gtri_xapxi,array,mid+1,high)
        elif array[mid] == Gtri_xapxi:
            return mid
        else:
            return binary_search(Gtri_xapxi,array,low,mid)
# endregion

#region Sppline1
def spline1(x,y): # in ra các hàm xấp xỉ spline bậc 1 DONE
    size = len(x)-1 # tính từ 0 
    digits = 3 # số chữ số sau dấu phẩy 
    khoang_cach = np.diff(x) # array khoang cach giua cac moc noi suy
    for i in range(1,size+1):
        print(f"S1[{x[i-1]}-{x[i]}] = ({round(y[i-1]/khoang_cach[i-1],digits)})*({x[i]}-x) + ({round(y[i]/khoang_cach[i-1],digits)})*(x-{x[i-1]})")

def xap_xi_spline1(x,y,xap_xi): # ham xap xi bang spline bac 1
    size = len(x)-1
    vi_tri = binary_search(xap_xi,x,0,size)-1
    khoang_cach = x[vi_tri+1]-x[vi_tri]
    ket_qua = ((y[vi_tri]/khoang_cach)*(x[vi_tri+1]-xap_xi)
                 + (y[vi_tri+1]/khoang_cach)*(xap_xi-x[vi_tri]))
    return ket_qua
#endregion

#region Spline 2  Done
def xap_xi_spline2(x,y,xap_xi):
    size=len(x)-1
    m = np.zeros(size+1)
    m = tinh_m_spline2(x,y)
    vi_tri = binary_search(xap_xi,x,0,size)
    if x[vi_tri] < xap_xi:
        vi_tri = vi_tri+1
    khoang_cach = x[vi_tri]-x[vi_tri-1]
    ket_qua = ((-m[vi_tri-1]/(2*khoang_cach))*(x[vi_tri]-xap_xi)**2
                + (m[vi_tri]/(2*khoang_cach))*(xap_xi-x[vi_tri-1])**2 
                +  (y[vi_tri]-m[vi_tri]*khoang_cach*0.5)  )
    return ket_qua

def spline2(x,y):
    size = len(x)-1
    khoang_cach= np.diff(x)
    digits = 3 # số chữ số đăng sau dấu phẩy 
    m = np.zeros(size+1)
    m = tinh_m_spline2(x,y)
    for i in range(1,size+1):
        print(f"S2[{x[i-1]};{x[i]}] = {round(-m[i-1]/(2*khoang_cach[i-1]),digits)} * ({x[i]}-x)^2"
                + f" + {round(m[i]/(2*khoang_cach[i-1]),digits)} * (x-{x[i-1]})^2 "
                + f" + {y[i]-m[i]*khoang_cach[i-1]*0.5}")

def tinh_m_spline2(x,y):
    size = len(x)-1
    khoang_cach = np.diff(x)
    m = np.zeros(size+1)
    m[0]=(y[1]-y[0])/(khoang_cach[0])
    for i in range(1, size+1):
        m[i] = -m[i-1]+(2/khoang_cach[i-1])*(y[i]-y[i-1])
    return m
#endregion

#region Spline 3

# Hàm sẽ return lại các mảng tham số alpha,lamda,beta,muy,m
def tinh_tham_so_spline3(x,y):  
    size = len(x)-1 # 4
    khoang_cach = np.diff(x)
    m = np.zeros(size+1)
    lamda = np.zeros(size+1)
    alpha = np.zeros(size+1)
    beta = np.zeros(size+1)
    d = np.zeros(size+1)
    muy = np.zeros(size+1)

    #tinh dao ham tai 2 diem bien
    dham_0 = (y[1]-y[0])/(x[1]-x[0])
    dham_n = (y[size]-y[size-1])/(x[size]-x[size-1])

    d[0] = 6/khoang_cach[0]*((y[1]-y[0])/khoang_cach[0]-dham_0)
    d[size] = 6/khoang_cach[size-1]*(dham_n-(y[size]-y[size-1])/khoang_cach[size-1])

    # tinh lamda
    for i in range(1,size):
        lamda[i] = khoang_cach[i]/(khoang_cach[i-1]+khoang_cach[i])
        muy[i]=khoang_cach[i-1]/(khoang_cach[i-1]+khoang_cach[i])
    muy[size] = 1-lamda[size]    

    #alpha[1] = -lamda[0]/2
    alpha[1] = -1/2
    beta[1]=d[0]/2
    for i in range(1,size):
        d[i]=(6/(khoang_cach[i-1]+khoang_cach[i]))*((y[i+1]-y[i])/khoang_cach[i]-(y[i]-y[i-1])/khoang_cach[i-1])
    for i in range(1,size):
        alpha[i+1] = lamda[i]/(-2-alpha[i]*muy[i])
        beta[i+1]=(beta[i]*muy[i]-d[i])/(-2-alpha[i]*muy[i])

    m[size] = (muy[size]*beta[size]-d[size])/(-2-muy[size]*alpha[size]) #m[n]

    for i in range(size-1,-1,-1):
        m[i] = alpha[i+1]*m[i+1]+beta[i+1]

    return m 

def xap_xi_spline3(x,y,xap_xi):
    size = len(x)-1
    m=np.zeros(size+1)
    m = tinh_tham_so_spline3(x,y)
    # vi_tri = binary_search(xap_xi,x,0,size)-1
    vi_tri = binary_search(xap_xi,x,0,size)
    if x[vi_tri] < xap_xi :
        vi_tri=vi_tri+1

    khoang_cach = x[vi_tri] - x[vi_tri-1]

    ket_qua = ((m[vi_tri-1]/(6*khoang_cach))*(x[vi_tri]-xap_xi)**3
                +((m[vi_tri])/(6*khoang_cach)*(xap_xi-x[vi_tri-1])**3)
                +(y[vi_tri-1]-(m[vi_tri-1]*khoang_cach**2)/6)*(x[vi_tri]-xap_xi)/khoang_cach
                +(y[vi_tri]-(m[vi_tri]*khoang_cach**2)/6)*(xap_xi-x[vi_tri-1])/khoang_cach
                )
            
    return ket_qua

def spline3(x,y):
    size = len(x)-1
    khoang_cach= np.diff(x)
    digits = 3 # so chu so sau dau phay
    m = np.zeros(size+1)
    m = tinh_tham_so_spline3(x,y)
    for i in range(1,size+1):
        print(f"S3[{x[i-1]};{x[i]}]=  {round(m[i-1]/(6*khoang_cach[i-1]),digits)}*({x[i]}-x)^3"
            f"+ {round(m[i]/(6*khoang_cach[i-1]),digits)}*(x-{x[i-1]})^3"
            f"+ {round((y[i-1]-(m[i-1]*khoang_cach[i-1]**2/6))/khoang_cach[i-1],digits)}*({x[i]}-x)"
            f"+ {round((y[i]-(m[i]*khoang_cach[i-1]**2/6))/khoang_cach[i-1],digits)}*(x-{x[i-1]})")
#endregion

#region Ve do thi 
def  ve_do_thi(x,y):
    size = len(x)-1
    toa_do = np.linspace(x[0],x[size],1000)
    y1=[]
    y2=[]
    y3=[]

    for i in toa_do:
        y1.append(xap_xi_spline1(x,y,i))
        y2.append(xap_xi_spline2(x,y,i))
        y3.append(xap_xi_spline3(x,y,i))
    
    fig,axs = plt.subplots()

    plt.title("Hàm ghép trơn")
    axs.plot(toa_do,y1,label='Spline 1',color = 'blue')
    axs.plot(toa_do,y2,label='Spline 2', color = 'green')
    axs.plot(toa_do,y3,label='Spline 3',color = 'red')
    axs.grid(True)
    axs.legend()
    plt.scatter(x,y)
    plt.show()

#endregion

def main():
    #region Xử lý dữ liệu đầu vào 
    x,y = data()
    # x,y = bubble_sort(x,y) # sap xep cac moc noi suy tang dan
    x,y = bubble_sort(x,y)
    #endregion

    #region Xấp xỉ 
    gtri_xap_xi = float(input("\nNhap gia tri xap xi : "))
    
    print("\nGiá trị xấp xỉ spline 1: {}".format(xap_xi_spline1(x,y,gtri_xap_xi)))
    spline1(x,y)
    print("======================================================================")
    print("\nGiá trị xấp xỉ spline 2: {}".format(xap_xi_spline2(x,y,gtri_xap_xi)))
    spline2(x,y)
    print("======================================================================")
    print("\nGiá trị xấp xỉ spline 3 : {}".format(xap_xi_spline3(x,y,gtri_xap_xi)))
    spline3(x,y)
    print("\n")
    #endregion

    #region Vẽ đồ thị 
    ve_do_thi(x,y)
    #endregion
    

if __name__=='__main__':
    main()

