#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 01:09:37 2018

@author: wojcik
"""
#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def to_intervals(series):
    return series.values[1:] - series.values[:-1]

def cute_error(a, b):
    error = (max(a,b)-min(a,b))/2
    order = int(np.log10(error))
    return (round((a+b)/2, -order+1), round(error, -order+1))

#%%
#data = pd.read_csv('../data/2geiger_comp_SBM20_8903_on_2_SBM20_8904_on_3_20190111_2', sep='|')
data = pd.read_csv('../data/2geiger_flat_SBM20_8903_on_2_SBM20_8904_on_3_20190202', sep='|')
data.columns = ['zone', 'time', 'ts', 'res']
data.set_index("time", inplace=True)

#%%
data.index = pd.to_datetime(data.index)
data['PIN2'] = (data['res'] == 'PIN2').astype(int)
data['PIN3'] = (data['res'] == 'PIN3').astype(int)

period = 60
width = 10
std = 3

moving = data[['PIN2','PIN3']].resample(str(period) + 'S').sum()
#moving = moving.rolling(period).mean()
moving2 = moving.rolling(width, win_type='gaussian').mean(std=std)

plt.figure(figsize=(7,7))
plt.plot(moving2.index, moving2['PIN3']/period, moving2['PIN2']/period)

gamma = sum(data['PIN3'])/(data['ts'][-1] - data['ts'][0])
N = 20469
test_data = []
t = 0
for i in range(0, N):
    t += np.random.exponential(1/gamma)
    test_data.append((t, 1))
    
df = pd.DataFrame(test_data, columns=['time', 'sample'])
df.set_index("time", inplace=True)
df.index = pd.to_datetime(df.index, unit='s')

m = df[['sample']].resample(period).sum()
m.fillna(0, inplace=True)
#moving = moving.rolling('100T').mean()
m2 = m.rolling(width, win_type='gaussian').mean(std=std)
plt.figure(figsize=(7,7))
plt.plot(m2.index, m2['sample'])

#%%
data2 = data[data['res'] == 'PIN2']
data3 = data[data['res'] == 'PIN3']

#%%
# How probable is spontanous symulatnous click
both_gamma = len(data)/(data['ts'][-1] - data['ts'][0])
dt = 0.6e-4
p = 1 - np.exp(-dt*gamma)
print((1/p)*both_gamma)