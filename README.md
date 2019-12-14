# Siglent-1104X-E
Project for saving scope traces from SIGLENT 1104X-E scopes.

# Requirements
mac OS 10.4
python3 with the following packages installed via pip:
   - pyvisa      >= 1.10.1
   - numpy       >=1.16.4
   - matplotlib  >=2.2.3
ni-visa 19.5 or higher

# Usage
`./logger.py -c C1 -o waveforms -n 10` logs 10 waveforms from channel 1 to the folder `waveforms`
`./display.py -i <waveform.txt>` displays the contents of `waveform.txt`
