import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pywt
import imageio


with open("data.json", "r") as f:
    d = json.load(f)

ids = sorted(d.keys())

for progress, i in enumerate(ids):
    print(progress, " / ", len(ids))
    person = d[i]
    sessions = sorted(person.keys())
    for session in sessions:
        for rec_nr, recording in enumerate(person[session]):
            for hb_nr, heartbeat in enumerate(recording):
                if len(heartbeat) != 100:
                    continue
                heartbeat = np.asarray(heartbeat)
                min, max = np.min(heartbeat), np.max(heartbeat)
                heartbeat = heartbeat / max
                n_scales = 128
                scales = np.arange(1, n_scales + 1)
                picture = np.zeros((128, 100, 3), float)

                for channel, wavelet in zip(range(3), ["mexh", "morl", "gaus5"]):
                    coeffs1, freqs = pywt.cwt(
                        heartbeat, scales, wavelet=wavelet)
                    picture[:, :, channel] = coeffs1

                min, max = np.min(picture), np.max(picture)
                picture = (picture - min) / (max - min) * (2**8 - 1)
                picture = picture.astype(np.uint8)

                name = f"db/{i}_{session}_{rec_nr}_{hb_nr}.png"
                imageio.imwrite(name, picture)

