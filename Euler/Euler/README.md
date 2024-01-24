# Euler
Euler methods to solve ODEs

## Setup the environment
> From this point, the word "lib" will be used as "library" and "libs" as "libraries"

Necessary libs for this program are listed below:
* sympy
* matplotlib
* wolframalpha (This lib is used to get the exact solution from Wolfram Alpha)

### Install libs
To install these libs, run these commands in terminal:

```bash
pip install sympy matplotlib wolframalpha
```

### Requirements
The program was written with Python3, so the device must have Python3 (3.8.10 or later version) installed

## Step by step guide
This guide will help you to run the program normally without reading the code.
However, there are still tips written as comments in each file that help you to read the code easier.

### `main.py` file
This is the main file of the program and it's function is to solve a first order ODE with 3 methods
Forward Euler, Backward Euler, Trapezoidal.

* Step 1: Enter required data as the tutorial in the `Input/input.txt` file
> All values in the same line must be splitted by a comma.
> In the first line, either `^` or `**` are acceptable, but `e^x` must be replaced by `exp(x)`.

* Step 2: Run:

```bash
python main.py
```

* Step 3: Check files `Output/output.txt` and `Output/output.png` for the answer

### `main_hcomparation.py` file
Use only 1 method to solve an ODE with more than 1 step h and plot

* Step 1: Run:

```bash
python main_hcomparation.py
```

* Step 2: Enter f(x, y):

```bash
f(x, y) = 
```

* Step 3: Enter x0, y0, xn in one line and list of step h in the next line, all values in the same line are splitted by commas:

```bash
f(x, y) = -10*y
Enter x0, y0, xn: 0, 1, 3
Enter list of step size (h): 0.01, 0.05, 0.2, 0.21
```

* Step 4: Enter number that present the method used:
> `0` for Forward Euler method,
> `1` for Backward Euler method, 
> `2` for Trapezoidal method

```bash
f(x, y) = -10*y
Enter x0, y0, xn: 0, 1, 3
Enter list of step size (h): 0.01, 0.05, 0.2, 0.21
Method used: 0
```

* Step 5: Check file `Output/output_hcomparation.png` for the answer

### Solving system of ODEs
Input is editted directly in file `main_system.py`. For example:

* Step 1: Edit the file to match the problem

> Enter input values as below
```py
3   INPUT = {
4       "k" : 3,    # number of equation
5       "t0": 0,    
6       "tn": 3,
7       "h" : 0.01,
8   
9       "iv": (1, 1, 1)   # initial values
10  }
```

> Enter the system of ODEs as below, read comments in the file for more detail
```py
27  def stepSolve(t, y):
..  
46      return [
47          -5*y[0] + 5*y[1],
48          14*y[0] - 2*y[1] - y[2]*y[0],
49          -3*y[2] + y[0]*y[1]
50      ]
```

* Step 2: Run:

```bash
python main_system.py
```

* Step 3: Check files `Output/output_system.txt` and `Output/output_system.png` for the answer

### Solving higher order ODE
Input is editted directly in file `main_high.py`. For example:

* Step 1: Edit the file to match the problem

> Enter input values as below
```py
4   INPUT = {
5       "k" : 3,    # level of equation
6       "t0": 0,    
7       "tn": 5,
8       "h" : 0.1,
9   
10     "iv": (0, 1, 0)    # initial values
11  }
```

> Enter the ODE as below, read comments in the file for more detail
```py
27  def stepSolve(x, y):
..  
47      y_n = 2*y[2] + 8*y[1] + y[0] + x
48      
49      return [y[i+1] for i in range(len(y)-1)] + [y_n]
```

* Step 2: Run:

```bash
python main_high.py
```

* Step 3: Check files `Output/output_high.txt` and `Output/output_high.png` for the answer
