import os
# import numpy as np
# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import ExtraTreesClassifier
# from sklearn.neighbors import KNeighborsClassifier
# from sklearn.tree import DecisionTreeClassifier
#
#
# def train_features(pd_data, **kwargs):
#     y = pd_data.iloc[:, 1]
#     pd_data.pop(1)
#     x = pd_data
#     X_train, X_test_file, y_train, y_test = train_test_split(x, y.ravel(), test_size=0.2,
#                                                         stratify=y, random_state=1)
#
#     print(len(X_test_file))
#     X_test = X_test_file.iloc[:, 1:-1]
#     X_train = X_train.iloc[:, 1:-1]
#     clf = None
#     if kwargs['clf'] == 'extra':
#         clf = ExtraTreesClassifier(n_estimators=kwargs['second'], random_state=kwargs['first'])
#     elif kwargs['clf'] == 'kneigh':
#         clf = KNeighborsClassifier(n_neighbors=kwargs['first'])
#     else:
#         clf = DecisionTreeClassifier(random_state=kwargs['first'])
#
#     clf.fit(X_train, y_train)
#     return round(clf.score(X_test, y_test), 5), clf, (X_test_file, y_test)
#
#
# def load_data(dir_path):
#     data = None
#     print(dir_path)
#     for file in os.listdir(dir_path):
#         print(file)
#         if file.endswith(".npy") and 'coordinates' not in file and 'velocity' not in file:
#             if data is None:
#                 data = np.load(dir_path + '/' + file)
#                 print(len(data))
#                 dir_path_np = np.repeat(dir_path + '/' + file, len(data)).reshape(-1, 1)
#                 data = np.concatenate((data, dir_path_np), axis=1)
#             else:
#                 d1 = np.load(dir_path + '/' + file)
#                 dir_path_np = np.repeat(dir_path + '/' + file, len(d1)).reshape(-1, 1)
#                 d1 = np.concatenate((d1, dir_path_np), axis=1)
#                 data = np.concatenate((data, d1))
#     print(len(data))
#     pd_data = pd.DataFrame(data)
#     return pd_data
#
#
def get_list_valid_files(dir_path):
    list_of_files = []
    all_files = os.listdir(dir_path)
    for file in all_files:
        if file.endswith(".npy") and (file[:-4] + '.mp4' in all_files or file[:-4] + '.avi' in all_files):
            list_of_files.append(os.path.join(dir_path, file))
    list_of_files.sort()
    return list_of_files
