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
import matplotlib.dates as mdates
from collections import Counter

def to_intervals(series, dt=1):
    return series.values[dt:] - series.values[:-dt]

def cute_error(a, b, shift=0):
    error = (max(a,b)-min(a,b))/2
    order = int(np.log10(error)) - shift
    return (round((a+b)/2, -order+1), round(error, -order+1))

#%%
data = pd.read_csv('../data/2geiger_flat_SBM20_8903_on_2_SBM20_8904_on_3_20190202', sep='|')
#data = pd.read_csv('../data/vertical_close_20181229', sep='|')
data.columns = ['zone', 'time', 'ts', 'res']
data.set_index("time", inplace=True)
data['sample'] = 1
data['delta'] = data['res'].apply(lambda k: int(k.split(',')[1]))
data = data[data.delta <= 36]
data.index = pd.to_datetime(data.index)

#%%
simult_data = data
print("start: %s" % simult_data.index[0])
t = simult_data['ts'].max() - simult_data['ts'].min()
intervals = to_intervals(simult_data['ts'])
print("measurment time: %f" % t)
print("number of events: %i" % len(simult_data))
print("mean lambda: %f" % (len(simult_data)/t))
print("mean waiting: %f" % intervals.mean())
print("std waiting: %f" % intervals.std())
e = 3*intervals.std()/np.sqrt(len(simult_data))
print("est waiting:", cute_error(intervals.mean() - e, intervals.mean() + e))
print("est lambda:", cute_error(1/(intervals.mean() - e), 1/(intervals.mean() + e)))
print(Counter(simult_data['delta']))

#%%
period = 60
width = 60
std = 18

moving = data.resample(str(period) + 'S').sum()
moving.fillna(0, inplace=True)
#moving = moving.rolling('100T').mean()
moving2 = moving.rolling(width, win_type='gaussian').mean(std=std)

plt.figure(figsize=(15,10))
hfmt = mdates.DateFormatter('%Y-%m-%d\n%H:%M:%S')

ax = plt.gca()
#ax.format_xdata = mdates.DateFormatter('%Y')
ax.xaxis.set_major_formatter(hfmt)
ax.grid()
ax.plot(moving2.index, moving2['sample']/period)

#%%
gamma = sum(data['sample'])/(data['ts'][-1] - data['ts'][0])
N = len(data)
test_data = []
t = data['ts'][0]
for i in range(0, N):
    t += np.random.exponential(1/gamma)
    test_data.append((t, t, 1))
    
df = pd.DataFrame(test_data, columns=['time', 'ts', 'sample'])
df.set_index("time", inplace=True)
df.index = pd.to_datetime(df.index, unit='s')

m = df[['sample']].resample(str(period) + 'S').sum()
m.fillna(0, inplace=True)
#moving = moving.rolling('100T').mean()
m2 = m.rolling(width, win_type='gaussian').mean(std=std)
plt.figure(figsize=(15,10))
ax = plt.gca()
ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
plt.plot(m2.index, m2['sample']/period)

# How probable is spontanous symulatnous click
# this is not entirely accurate
#both_gamma = len(data)/(data['ts'][-1] - data['ts'][0])
#dt = 0.6e-4
#p = 1 - np.exp(-dt*gamma)
#print((1/p)*both_gamma)

#%%
k = 3
d4 = to_intervals(data['ts'], k)
r4 = to_intervals(df['ts'], k)
bins = np.arange(0, 4, 0.25)
plt.figure(figsize=(10,10))
plt.grid()
#plt.ylim((0, 2.5))
#plt.hist(np.log10(d4), bins=bins, normed=True)
plt.hist(np.log10(d4), bins=bins, normed=True)
plt.show()

plt.figure(figsize=(10,10))
plt.grid()
#plt.ylim((0, 2.5))
plt.hist(np.log10(r4), bins=bins, normed=True)
plt.show()


#%%
T = 10
plt.figure(figsize=(15,10))
data['series'] = 1
data['series'][:-k] = 1 - (d4 <= k*T).astype(int)
data['rnd'] = 1
data['rnd'][:-k] = 0.5 - (r4 <= k*T).astype(int)
plt.plot(data.index, data['series'], '.')
plt.plot(data.index, data['rnd'], '.',c='red')