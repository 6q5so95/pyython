from sympy import Symbol
from sympy.plotting import plot
from sympy import exp

x = Symbol("x")
plot(1/(1 + exp(-12*x + 12)), (x,0,1))

