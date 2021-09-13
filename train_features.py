import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier


def train_features(pd_data):
    x = pd_data.iloc[:, 2:]
    y = pd_data.iloc[:, 1]
    X_train, X_test, y_train, y_test = train_test_split(x, y.ravel(), test_size=0.2,
                                                        stratify=y, random_state=1)
    elf = ExtraTreesClassifier(n_estimators=100, random_state=0)
    elf.fit(X_train, y_train)
    print("Accuracy with 40 points:", elf.score(X_test, y_test))


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
    train_features(pd_data)

load_data("data")