#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 18 12:15:04 2018

@author: wojcik
"""
import numpy as np


mu = 1.849e-5
d = 7.63e-4
rho = 1.184 
sigma = 883
rho_prim = rho - sigma
g = 9.802 #New York Value
b = 6.17e-6
P = 76.01
V = 500
s = 4.71e-3

def _mu(a0, mu0=mu, P=P):
    return mu0 * ((1 + b/(a0*P))**-1)

def _a0(B, mu=mu):
    return ((9*B*mu*d)/(2*rho_prim*g))**0.5

def _e(A, a, mu):
    return (6*s*np.pi*a*mu*d*A)/V

B1 = [-27.9, -29.6, -28.2, -29.3, -29.4]

a = list(map(lambda B: _a0(1/B, _mu(_a0(1/B))), B1))
better_a = np.array(a).mean()
better_mu = _mu(better_a, mu)
