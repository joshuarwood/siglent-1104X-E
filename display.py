#!/usr/bin/env python3

r"""
@author Josh Wood
@date   Dec 13, 2019
@brief  Displays waveform files created with logger.py
        usage: ./display.py -i <waveform.txt> [-s]
"""

import io
import os
import argparse
import numpy as np
import matplotlib.pyplot as plt

def rescale(a):
    i = int(np.log10(a.max()))
    if i < 0:
        i -= 1
    pwr = 10**i

    return  a / pwr, pwr

def display(path, save=False):

    f = open(path)

    tdiv = float(f.readline().split()[-1][:-1])
    sara = float(f.readline().split()[-1][:-4])
    vdiv = float(f.readline().split()[-1][:-1])
    offset = float(f.readline().split()[-1][:-1])
    waveform = np.array([int(data) for data in f.readline().split()]) 
    waveform[waveform > 127] -= 255 

    v = waveform * (vdiv / 25) - offset
    v, vpwr = rescale(v)

    t = - tdiv * 14 / 2 + np.arange(v.size) / sara
    t, tpwr = rescale(t)

    fig = plt.figure(figsize=[7,4])
    plt.plot(t, v)
    plt.xlabel("time [%.2e s]" % tpwr)
    plt.ylabel("voltage [%.2e V]" % vpwr)
    plt.title(os.path.basename(path))
    plt.grid()
    if save:
        png = path.replace(".txt",".png")
        print("Saving " + png)
        plt.savefig(png, dpi=200)
    else:
        plt.show()
    plt.clf()

# END display()

p = argparse.ArgumentParser(
    prog="Waveform Display",
    description="Waveform display for SIGLENT SDS 1104X-E scope")
p.add_argument("-i", '--input', required=True, help="Input file")
p.add_argument("-s", "--save", action="store_true", help="Save a png image")

if __name__ == "__main__":
    args = p.parse_args()
    if args.input[-4:] != ".txt":
        raise ValueError("Input file must end with .txt")
    display(args.input, args.save)
