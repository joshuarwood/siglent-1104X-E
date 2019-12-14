# siglent-1104X-E
Project for saving scope traces from SIGLENT 1104X-E scopes

# Requirements
mac OS 10.4
python3 with pyvisa, numpy, matplotlib packages installed via pip
ni-visa 19.5 or higher

# Usage
`./logger.py -c C1 -o waveforms -n 10` logs 10 waveforms from channel 1 to the folder `waveforms`
`./display.py <waveform.txt>` displays the contents of `waveform.txt`
