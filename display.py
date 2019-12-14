#!/usr/bin/env python3

r"""
@author Josh Wood
@date   Dec 13, 2019
@brief  Displays waveform files created with logger.py
        usage: ./display.py <waveform.txt>
"""

import io
import os
import sys
import numpy as np
import matplotlib.pyplot as plt

def display(path, png=None):

    f = open(path)

    tdiv = float(f.readline().split()[-1][:-1])
    sara = float(f.readline().split()[-1][:-4])
    vdiv = float(f.readline().split()[-1][:-1])
    offset = float(f.readline().split()[-1][:-1])
    waveform = np.array([int(data) for data in f.readline().split()]) 
    waveform[waveform > 127] -= 255 

    v = waveform * (vdiv / 25) - offset
    t = - tdiv * 14 / 2 + np.arange(v.size) / sara
    pwr = 10**int(np.log10(t.max()))
    t /= pwr

    plt.plot(t, v)
    plt.xlabel("time [%.2e s]" % pwr)
    plt.ylabel("voltage [V]")
    plt.title(os.path.basename(path))
    if png:
        plt.savefig(png)
    else:
        plt.show()
    plt.clf()

# END display()

if __name__ == "__main__":
    display(sys.argv[1])

