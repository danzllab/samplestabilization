# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 12:43:51 2023

@author: danzloptics_admin

stand-along script for data visualization while sample lock is running; to be executed in dedicated console
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from collections import deque
from io import StringIO
import time

# mpl.use('TkAgg')

# file_name = "D:\\dev\\minflux\\builds\\20221202\\dump.csv"
file_name = "..\\data\\sampleLock_0.csv"
n_samples = 1000
# t_display = 100
# n_samples = 10*t_display

dim = 2

fig, ax = plt.subplots(4, 1, sharex=True, num=1, clear=True)
plt.ion()
plt.show()

# for i in range(n_samples):
while True:
    with open(file_name) as file:
        q = deque(file, n_samples)
    data = pd.read_csv(StringIO("".join(q)), header=None, sep=",", usecols=range(7))
    # names=('x', 'y', 'z', 'ex', 'ey', 'ez'))
    # data = pd.read_csv(file_name, header=None, sep='\t', usecols=range(6), nrows=i)
    # if data[6][len(data)-1] - data[6][0] > t_display:
    #     data = data[data[6][len(data)-1] - data[6] < t_display]

    # k = 50
    # active_read = True
    # while active_read:
    #     with open(file_name) as file:
    #         q = deque(file, k)
    #     data = pd.read_csv(StringIO(''.join(q)), header=None, sep=',', usecols=range(7))
    #     if data[6][len(data)-1] - data[6][0] < t_display:
    #         k *= 2
    #     else:
    #         data = data[data[6][len(data)-1] - data[6] < t_display]
    #         active_read = False

    ax[0].clear()
    ax[1].clear()
    ax[2].clear()
    ax[3].clear()
    ax[0].plot(data[6][::-1], 1e3 * data[0 + dim][::-1], color="C0")
    # ax[1].plot(data[6][::-1], data[3+dim][::-1], color='C1')
    ax[1].plot(data[6][::-1], data[3][::-1], color="C1")
    ax[2].plot(data[6][::-1], data[4][::-1], color="C1")
    ax[3].plot(data[6][::-1], data[5][::-1], color="C1")

    ax[0].set_ylabel("stage position [nm]")
    ax[1].set_ylabel("error signal x")
    ax[2].set_ylabel("error signal y")
    ax[3].set_ylabel("error signal z")
    ax[3].set_xlabel("elapsed time [s]")

    for i in range(4):
        ax[i].grid(True)

    # break
    plt.pause(0.4)
    plt.tight_layout()
