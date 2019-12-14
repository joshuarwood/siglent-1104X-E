#!/usr/bin/env python3

r"""
@author Josh Wood
@date   Dec 13, 2019
@brief  Logs waveforms from a SIGLENT SDS 1104X-E scope
        usage: ./logger.py -c <channel> -o <dir> -n <number>
"""
import os
import time
import pyvisa
import argparse

from datetime import datetime

# arguments
p = argparse.ArgumentParser(
    prog="Waveform Logger",
    description="Waveform logger for SIGLENT SDS 1104X-E scope")
p.add_argument("-c", "--channels", nargs="+", default="C1",
               help="Scope channel (C1, C2, C3, C4)")
p.add_argument("-o", '--output', default="",
               help="Output directory")
p.add_argument("-n", "--num", type=int, default=1,
               help="Number of traces to record")
args = p.parse_args()

if isinstance(args.channels , str):
    args.channels = [args.channels]

if len(args.output):
    os.system("mkdir -p " + args.output)

chans = ["C1", "C2", "C3", "C4"]
for chan in args.channels:
    if chan not in ["C1", "C2", "C3", "C4"]:
        raise ValueError("Channel %s not in %s" % (chan, chans))

# connect to oscilloscope, assumes only one scope connected
rm = pyvisa.ResourceManager()
inst = rm.open_resource(rm.list_resources()[0])
inst.write_termination = '\n'
inst.read_termination = '\n'
inst.query_delay = 1
inst.timeout = 30000

# check connection
name = inst.query('*IDN?').strip()
print("\nConnected: " + name)

for i in range(args.num):

    # get timestamp
    t0 = time.time()
    ts = datetime.fromtimestamp(t0).strftime("%Y-%d-%mT%H:%M:%S")

    print("\n%s Acquiring ..." % ts)
    try:
        inst.write("ARM")
        for chan in args.channels:

            trigger = os.path.join(args.output, "waveform_%s_%s.txt" % (chan, ts))

            tdiv = inst.query("TDIV?")
            sara = inst.query("SARA?")
            vdiv = inst.query(chan + ":VDIV?")
            ofst = inst.query(chan + ":OFST?")

            # number of waveform points to sample
            sanu = int(float(inst.query("SANU? " + chan).split()[-1][:-3]))

            inst.write(chan + ":WF? DAT2")

            raw = []
            while len(raw) < int(22 + sanu + 2):
                raw.extend(list(inst.read_raw()))
            waveform = list(raw)[22:22 + sanu]

            f = open(trigger, "w")
            f.write(tdiv + "\n")
            f.write(sara + "\n")
            f.write(vdiv + "\n")
            f.write(ofst + "\n")
            f.write(" ".join([str(data) for data in waveform]))
            f.close()
            print(" - Saved " + trigger)

        # END for (chan)
        print(" - Completed in %.2f sec" % (time.time() - t0))
    except BaseException:
        print(" - Skipping due to read timeout")
# END for (i)

inst.close()
