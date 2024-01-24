#include<bits/stdc++.h>

using namespace std;

double x[20],y[20],a[20],b[20],e[20];
double hs[20],mt[20][20];
double sp(int l, int k)
{
 if(l==1) return y[k+1]-y[k];
 else return sp(l-1,k+1)-sp(l-1,k);
}
int gt(int n)
{
 if(n==1) return 1;
 else return n*gt(n-1);
}
double luythua(double n, int k)
{
 if(k==0) return 1;
 else return (n*luythua(n,k-1));
}
void nhandt(int n, double c)
{
 b[0]=0;
 a[n]=b[n];
 for(int i=n-1;i>=0;i--)
   a[i]=b[i]-b[i+1]*c;
}
void newdt(double b[],double a[],int n)
{
 for(int i=0;i<=n;i++)
    b[i+1]=a[i];
}
void nhanmatranheso(int n, double a[], double b[][20], double c[])
{
 for(int i=1;i<=n;i++)
    for(int j=1;j<=n;j++)
    {
       c[n-i+1]+=a[j]*b[j][i];
    }
}
void inheso(double a[], int n)
{
 for(int i=1;i<=n;i++)
    printf("%lf ",a[i]);
    cout<<endl<<endl;
}

void inmtheso(int n, double mt[][20])
{
 for(int i=1;i<=n;i++)
 {
     for(int j=1;j<=n;j++)
       printf("%.lf ",mt[i][j]);
       cout<<endl;
 }
}
int main()
{
 freopen("g1.INP","r",stdin);
 freopen("g1.OUT","w",stdout);
 int n;
 scanf("%d",&n);
 for(int i=-n;i<=n;i++)
    scanf("%lf",&x[i]);
 for(int i=-n;i<=n;i++)
    scanf("%lf",&y[i]);
 a[0]=1;
 for(int i=0;i<2*n;i++)
 {
    newdt(b,a,i);
    int h=(i+1)/2;
    nhandt(i+1,luythua(-1,i+2)*h);
    hs[i+1]=sp(i+1,-(i+2)/2)/gt(i+1);
    for(int j=0;j<=2*n;j++)
        mt[i+1][2*n-j+1]=a[j];
 }
 nhanmatranheso(2*n,hs,mt,e);
 printf("Ma tran he so: \n");
 inmtheso(2*n,mt);
 printf("He so sai phan: \n");
 inheso(hs,2*n);
 e[0]=y[0];
 for(int i=2*n;i>=0;i--)
    printf("a%d: %lf \n",i,e[i]);
 double q,m[10];
 double xo;
 double ketqua=0;
 scanf("%lf",&xo);
  q = (xo-x[0])/(x[1]-x[0]);
 for(int i=2*n;i>=0;i--)
    ketqua+=e[i]*luythua(q,i);
 printf("\nf(%lf): %.lf",xo,ketqua);
}
