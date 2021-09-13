import numpy as np
import pandas as pd
import os
import cv2


def create_image(frame_num, action_num, videofile_name, dir_path):
    dest_dir = 'Imagenet'
    frame_num = int(float(frame_num))
    action_num = str(int(float(action_num)))

    if not os.path.isdir(dest_dir):
        os.mkdir(dest_dir)

    cap = cv2.VideoCapture(dir_path + '/' + videofile_name + '.mp4')
    cap.set(1, frame_num)
    ret, frame = cap.read()
    if not os.path.isdir(dest_dir + '/' + action_num):
        os.mkdir(dest_dir + '/' + action_num)

    cv2.imwrite('{}/{}/{}.jpg'.format(dest_dir, action_num, videofile_name + '_' + str(frame_num)), frame)


def create_imagenet_dataset(dir_path):
    for file in os.listdir(dir_path):
        if file.endswith("LogoView.npy"):
            data = np.load(dir_path + '/' + file)
            for d in data:
                create_image(d[0], d[1], file[:-4], dir_path)


