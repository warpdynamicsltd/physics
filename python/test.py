#%%
import sympy as sp
sp.init_printing()

#%%
x = sp.Symbol('x')
k = sp.Symbol('k')
display(x)
n = sp.Symbol('n')

a_n = sp.Function('a')(n)
