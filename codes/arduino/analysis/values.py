#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 30 01:05:40 2018

@author: wojcik
"""

#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

def to_intervals(series):
    return series.values[1:] - series.values[:-1]

def cute_error(a, b):
    error = (max(a,b)-min(a,b))/2
    order = int(np.log10(error))
    return (round((a+b)/2, -order+1), round(error, -order+1))

#%%
#data = pd.read_csv('../data/2geiger_comp_J305_on_2_M4011_on_3_20181229', sep='|')
data = pd.read_csv('../data/2geiger_comp_SBM20_8903_on_2_SBM20_8904_on_3_20190111_2', sep='|')
data.columns = ['zone', 'time', 'ts', 'res']
data.set_index("time", inplace=True)

data2 = data[data['res'] == 'PIN2']
data3 = data[data['res'] == 'PIN3']

print("measurment time: %f" % (data['ts'].max() - data['ts'].min()))

print("discharges2: %i" % len(data2))
print("discharges3: %i" % len(data3))

intervals2 = to_intervals(data2['ts'])
intervals3 = to_intervals(data3['ts'])

print("waiting2: %f" % intervals2.mean())
print("waiting3: %f" % intervals3.mean())
print("std2: %f" % intervals2.std())
print("std3: %f" % intervals3.std())

e2 = 3*intervals2.std()/np.sqrt(len(data2))
e3 = 3*intervals3.std()/np.sqrt(len(data3))

print("est waiting2:", cute_error(intervals2.mean() - e2, intervals2.mean() + e2))
print("est waiting3:", cute_error(intervals3.mean() - e3, intervals3.mean() + e3))

print("est lambda2:", cute_error(1/(intervals2.mean() - e2), 1/(intervals2.mean() + e2)))
print("est lambda3:", cute_error(1/(intervals3.mean() - e3), 1/(intervals3.mean() + e3)))

#%%
simult_data = pd.read_csv('../data/2geiger_79mm_SBM20_8903_on_2_SBM20_8904_on_3_20190113', sep='|')
simult_data.columns = ['zone', 'time', 'ts', 'res']
simult_data['delta'] = simult_data['res'].apply(lambda k: int(k.split(',')[1]))

print("start: %s" % simult_data['time'][0])
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

print("***DELTA***")
print(Counter(simult_data['delta']))
beta = simult_data['delta'].mean()
print("mean delta t: %f" % beta)
print("std delta: %f" % simult_data['delta'].std())
th = simult_data['delta'].mean() + 3*simult_data['delta'].std()
print("limit: %f" % (th))



