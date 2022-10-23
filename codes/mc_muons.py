#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 25 21:27:47 2018

@author: wojcik
"""

import numpy as np

#length in cm
X = 7.3
D = 1.0
H = 10.2

I0 = 8.4e-3
n = 1.85

def get_random_theta1():
  x = np.random.random()*X
  y = np.random.random()*D
  x_ = np.random.random()*X
  y_ = np.random.random()*D
  
  r = np.sqrt((x_-x)**2 + (y_ - y)**2 + H**2)
  theta = np.arccos(H/r)
  
  return theta

def get_random_from_cilinder(X, R):
    r = np.sqrt(np.random.random()) * R
    alpha = 2*np.pi*np.random.random()
    y = r*np.cos(alpha)
    z = r*np.sin(alpha)
    x = np.random.random()*X
    return x, y, z
    
def get_random_theta2():
    x, y, z = get_random_from_cilinder(X, D/2)
    x_, y_, z_ = get_random_from_cilinder(X, D/2)
    r = np.sqrt((x_-x)**2 + (y_ - y)**2 + (H + z_ - z)**2)
    theta = np.arccos((H + z_ - z)/r)
    return theta
  
def mc1(N):
    sigma = 0
    for i in range(N):
        theta = get_random_theta1()
        sigma += (np.cos(theta)**(n+1))*np.sin(theta)
        
    result = I0 * (sigma/N)
    
    return result

def mc2(N):
    sigma = 0
    for i in range(N):
        theta = get_random_theta2()
        sigma += (np.cos(theta)**(n))*np.sin(theta)
        
    result = I0 * (sigma/N)
    
    return result
  