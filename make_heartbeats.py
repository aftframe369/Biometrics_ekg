import os
import re
import json
import numpy as np
import matplotlib.pyplot as plt
from scipy import fft, signal
import neurokit2 as nk

#prawdopodobnie nie działa i wszystko co z niego powinno być w loader.py już tam jest

SR = 250
window = 50

with open("raw_data.json", 'r') as f:
    d = json.load(f)

r = (sorted(d.keys()))
for i in r:
    sa = np.asarray(d[i]['S1'][0])
    sa = sa[:np.argmax(sa)-50]
    _, rpeaks = nk.ecg_peaks(sa, sampling_rate=250)
    heartbeat = []
    for peak in rpeaks["ECG_R_Peaks"]:
        heartbeat.append(sa[peak-window:peak+window])
    x = np.arange(0, len(sa))
    _, (ax1, ax2) = plt.subplots(1,2)
    ax1.plot(x, sa)
    ax1.scatter(rpeaks["ECG_R_Peaks"], sa[rpeaks["ECG_R_Peaks"]] )
    ax2.plot(heartbeat[0])
    # ax2.plot(xb, sb)
    plt.show()
