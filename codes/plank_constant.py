#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 18 22:25:25 2018

@author: wojcik
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

V_A = [
 (1.49, 5.4),      
 (1.51, 7.4),
 (1.53, 9.9),
 (1.55, 12.7),
 (1.57, 16.5),
 (1.59, 21.3),
 (1.61, 28.2),
 (1.63, 36.0),
 (1.65, 51.4),
 (1.67, 71),
 (1.69, 113),
 (1.75, 225),
 (1.77, 314),
 (1.80, 387),
 (1.82, 470),
 (1.85, 640),
 (1.87, 785),
 (1.89, 955),
 (1.91, 1131),
 (1.92, 1334),
 (1.94, 1455),
 (1.96, 1709),
 (1.98, 1950),
 (2.00, 2500),
 (2.02, 2930),
 (2.04, 3310),
 (2.06, 3750),
 (2.08, 4030),
 (2.10, 4460),
 (2.12, 5130),
 (2.14, 5560),
 (2.16, 6260),
 (2.18, 6820),
 (2.20, 7280),
 (2.225, 8250),
 (2.24, 8760),
 (2.27, 9030),
 (2.3, 10870),
 (2.32, 11040),
 (2.36, 12690),
 (2.38, 13970),
 (2.40, 15000)]

V, A = list(zip(*V_A))
data = pd.read_csv("940nm.csv")
plt.figure(figsize=(12,12))
plt.title("Potential/Current characteristic of infrared LED (940nm)", size=14)
plt.xticks(np.arange(0, 1.3, 0.05))
plt.xlabel("Potential [V]")
plt.ylabel("Current [mA]")
plt.plot(data["V"], data["microA"]/1000)
plt.plot(data["V"], data["microA"]/1000, 'o')