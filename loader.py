import os
import re
import json
import numpy as np
import matplotlib.pyplot as plt
import neurokit2 as nk

print(os.curdir)

database = {}
errors =""

def preprocess(input):
    window = 50
    data = input
    data = data[:np.argmax(data)-50]
    _, rpeaks = nk.ecg_peaks(data, sampling_rate=250)
    heartbeat = []
    for peak in rpeaks["ECG_R_Peaks"]:
        heartbeat.append(data[peak-window:peak+window])
    return heartbeat

def read_files(names, path):
    all_readings = []
    for n in names:
        file = os.path.join(path, n)
        with open(file, 'r') as f:
            data = f.readlines()
        data = list(map(lambda x: float(x.strip()), data))
        all_readings.append(preprocess(data))
    return all_readings


for dirpath, dirnames, names in os.walk("data"):
    search = re.search("Session-(\d.*)/(\d*)$", dirpath)
    try:
        id = search.group(2)
        session = "S"+search.group(1)
        if id in database:
            database[id][session] = read_files(names, dirpath)
        else:
            database[id] = {session: read_files(names, dirpath)}
    except AttributeError as e:
        print(e)
        errors+=dirpath+"\n"


# print(json.dumps(database, indent=4))
# # print(errors)

with open('data.json', 'w') as f:
    json.dump(database, f, indent=4)
