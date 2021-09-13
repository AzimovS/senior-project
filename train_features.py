import os
import numpy as np
import pandas as pd


def load_data(dir_path):
    data = None
    for file in os.listdir(dir_path):
        if file.endswith("LogoView.npy"):
            if data is None:
                data = np.load(dir_path + '/' + file)
            else:
                d1 = np.load(dir_path + '/' + file)
                print(len(d1))
                data = np.concatenate((data, d1))
    pd_data = pd.DataFrame(data)
    print(pd_data)

load_data("data")