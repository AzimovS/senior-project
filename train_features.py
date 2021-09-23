import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier


def train_features_extratrees(pd_data, **kwargs):
    x = pd_data.iloc[:, 2:]
    y = pd_data.iloc[:, 1]
    X_train, X_test, y_train, y_test = train_test_split(x, y.ravel(), test_size=0.2,
                                                        stratify=y, random_state=1)
    clf = None
    if kwargs['clf'] == 'extra':
        clf = ExtraTreesClassifier(n_estimators=kwargs['second'], random_state=kwargs['first'])
    elif kwargs['clf'] == 'kneigh':
        clf = KNeighborsClassifier(n_neighbors=kwargs['first'])
    else:
        clf = DecisionTreeClassifier(random_state=kwargs['first'])

    clf.fit(X_train, y_train)
    return round(clf.score(X_test, y_test), 4)


def load_data(dir_path):
    data = None
    for file in os.listdir(dir_path):
        if file.endswith("LogoView.npy"):
            if data is None:
                data = np.load(dir_path + '/' + file)
            else:
                d1 = np.load(dir_path + '/' + file)
                data = np.concatenate((data, d1))
    pd_data = pd.DataFrame(data)
    return pd_data
