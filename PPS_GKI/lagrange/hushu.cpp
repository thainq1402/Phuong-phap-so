#include<bits/stdc++.h>
using namespace std;

const int N = 1e4 + 12;
#define FOR(i, a, b) for (int _ = a, __ = b, i = _; i <= __; i++)
#define FORD(i, a, b) for (int _ = a, __ = b, i = _; i >= __; i--)
#define FIX(n, x) cout << setprecision((int)n) << fixed << x << "\n";

int n;
long double dw[N]; 					// w'[x_i]
vector<long double> arr_wi;			// Hệ số của (x-x_1)(x-x_2)...(x-x_n)
vector<long double> arr_Lagrange;			// Hệ số của đa thức ns Lagrange


struct Data {
	long double x, y;
	bool operator < (const Data &newa) const{ //not so clear
		return x < newa.x;
	}
} a[N];

void Print(vector<long double> &v) {
	cout << "\nIn cac he so tu x^0 den x^" << v.size() - 1 << "\n";
	for (auto x : v) cout << x << " " ; cout << "\n\n";
}

vector<long double> hoocnerNhan(vector<long double> &arr, long double hs, long double xk) {				// arr nhân (hs * x + xk)  
	vector<long double> ret;
	ret.resize(arr.size() + 1);
	// neu arr chua co gi thi ret = hs*x + xk)
	if (arr.size() == 0) { 
		ret.resize(2);
		ret[0] = xk, ret[1] = hs;
		FORD(i, ret.size() - 1, 0) cout<<"\n"<<i<<"\t"<<ret[i];
		return ret;
	}

	FORD(i, ret.size() - 1, 0) {
		long double tmp = 0; 							// hệ số x^i
		if (i > 0) tmp += arr[i - 1] * hs;
		if (i < arr.size()) tmp += arr[i] * xk;
		ret[i] = tmp;
		cout<<"\n"<<i<<"\t"<<ret[i];
	}

	return ret;
}

vector<long double> hoocnerChia(vector<long double> &arr, long double hs, long double xk)	{			// arr chia (hs * x + xk)
	vector<long double> ret; ret.resize(arr.size() - 1);

	long double nho = 0;
	FORD(i, arr.size() - 1, 1) {
		long double val = (arr[i] - nho) / hs; 			// hệ số x^(i-1)
		nho = val * xk;
		ret[i - 1] = val;
	}

	return ret;
}

void Get_Lagrange(vector<long double> &arr_wi, int i) {
	vector<long double> ret = hoocnerChia(arr_wi, 1, -a[i].x); // w_{n+1}(x) / (x - x_i) 
	cout<<"\ndang xet o"<<i<<"\n";
	FOR(k, 0, ret.size() - 1)
	cout<<ret[k]<<"\t\t";
	long double val = a[i].y / dw[i]; //y_i / wd(x_i)
	//cout<<"\n val ="<<val;
	cout<<"\nhe so sau khi cap nhat lan thu "<<i<<"\n";
	FOR(k, 0, arr_Lagrange.size() - 1) 
		{
		arr_Lagrange[k] += ret[k] * val;
		cout<<arr_Lagrange[k]<<"\t\t";
		};
	//val là giá trị y_i / w'(x_i)
	// ret[k] là hệ số x^i của w_{n+1}(x) / (x - x_k) 
	//arr_Lagrange[k] là hệ số x^k của đa thức nội suy Lagrange, voi moi lan lap i thi cap nhat tong sigma

	return ;
}

void Init() {

    sort (a, a + n + 1); 

    cout << "Sap xep theo cac moc noi suy tang dan\n";
    FOR(i, 0, n) cout << a[i].x << " " << a[i].y << "\n"; cout << "\n";

    // Tính dw[i] = w'(x_i)
	cout<<"\n===========================================================";
	cout<<"\ntinh dw[i]:";
    FOR(i, 0, n) {
    	dw[i] = 1;
    	FOR(j, 0, n) if (i != j) dw[i] *= (a[i].x - a[j].x);
        // tinh ra ket qua cu the (dang so) voi tung x_i va luu vao dw[]
		cout<< "\nDw["<<i<<"]="<<dw[i];
    }

    // nhân arr_wi là hệ số của (x-x_1)(x-x_2)...(x-x_n)
	cout<<"\n===========================================================";
	cout<<"\ntinh w_n:";
    FOR(i, 0, n)
		{ 	cout<< "\nnhan voi (x"<<-a[i].x<<"):";
			arr_wi = hoocnerNhan(arr_wi, 1, -a[i].x); 
			//nhan da thuc (x-x_i)
		}

    // arr_Lagrange chứa hệ số của đa thức nội suy Lagrange
	cout<<"\n===========================================================";
	cout<<"\ncap nhat he so da thuc sau moi lan cong";
    arr_Lagrange.resize(arr_wi.size() - 1);
    FOR(i, 0, n) {
        Get_Lagrange(arr_wi, i);
    	// Cập nhật y_i.L_i(x) cho arr_Lagrange (cong tung Y_i.L_i(x) vao)
    }

    Print(arr_Lagrange);
}

long double Get_Value_y(long double value_x) {
	long double value_y = 0;

   	long double powx = 1; // lũy thừa của value_x
   	FOR(i, 0, arr_Lagrange.size() - 1) {
   		value_y += arr_Lagrange[i] * powx;
   		powx *= value_x;
   	}

   	//cout << "Gia tri da thuc ns Lagrange tai x = " << value_x << " bang " <<value_y << "\n";

   	return value_y;
}

main(){
    #define file "nsLagrange"
    freopen (file ".inp", "r", stdin);
    freopen (file ".out", "w", stdout);
    ios_base::sync_with_stdio(false);
    cin.tie(0);

    cin >> n; // số lượng mốc nội suy ban đầu 
    n -= 1;

    FOR(i, 0, n) cin >> a[i].x >> a[i].y; //input cac moc noi suy

    cout << fixed << setprecision(10); 
    
	Init(); // chuong trinh

    int nq;
    cin >> nq; // số lượng mốc nội suy cần tính 
    while(nq--) {
    	long double value_x;
    	cin >> value_x;
    	cout << "Gia tri da thuc ns Lagrange tai x = " << value_x << " bang " ;
    	cout << Get_Value_y(value_x) << "\n";
    }

}

