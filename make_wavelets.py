import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pywt


with open("data.json", 'r') as f:
    d = json.load(f)

ids = sorted(d.keys())[:4]

for i in ids:
    heartbeats = d[i]["S1"][0][:4]

    fig, axs = plt.subplots(nrows=4, ncols=4, figsize=(20, 20))
    for hb, ax in zip(heartbeats, axs):
        ax[0].plot(hb)
        ax[0].spines['right'].set_visible(False)
        ax[0].spines['top'].set_visible(False)
        ax[0].set_ylabel('Scale')
        ax[0].set_xlabel('Time')

        # range of scales from 1 to n_scales
        n_scales = 128
        scales = np.arange(1, n_scales + 1)
        wavelets = ["mexh", "morl", "gaus5"]
        for i in range(1, 4):
            # continuous wavelet transform wavelet = "mexh"  # mexh, morl, gaus8, gaus4, 'sym5', 'coif5'
            coeffs1, freqs = pywt.cwt(hb, scales, wavelet=wavelets[i-1])
            # create scalogram
            ax[i].imshow(coeffs1, cmap='coolwarm', aspect='auto')
            ax[i].set_title(wavelets[i-1])
            ax[i].spines['right'].set_visible(False)
            ax[i].spines['top'].set_visible(False)
            ax[i].set_ylabel('Scale')
            ax[i].set_xlabel('Time')
    plt.show()
