import numpy as np
import pandas as pd
import os
import cv2
import tqdm
import datetime


def create_image(frame_num, action_num, videofile_name, dir_path, dest_dir):
    frame_num = int(float(frame_num))
    action_num = str(int(float(action_num)))

    cap = cv2.VideoCapture(dir_path + '/' + videofile_name + '.mp4')
    cap.set(1, frame_num)
    ret, frame = cap.read()
    if not os.path.isdir(dest_dir + '/' + action_num):
        os.mkdir(dest_dir + '/' + action_num)

    cv2.imwrite('{}/{}/{}.jpg'.format(dest_dir, action_num, videofile_name + '_' + str(frame_num)), frame)


def create_imagenet_dataset(dir_path):
    date = datetime.datetime.now()
    dest_dir = 'ImageFolder' + str(date.day) + str(date.month) + '_0'

    while os.path.isdir(dest_dir):
        dest_dir, num = dest_dir.split('_')
        dest_dir = dest_dir + '_' + str(int(num) + 1)

    os.mkdir(dest_dir)

    first_image = True
    for file in os.listdir(dir_path):
        if file.endswith("LogoView.npy"):
            data = np.load(dir_path + '/' + file)
            prev_frame = None
            prev_action = None
            prev_videofile_name = None
            for d in data:
                if first_image and prev_frame is None:
                    prev_frame = d[0]
                    prev_action = d[1]
                    prev_videofile_name = file[:-4]
                elif first_image and prev_action == d[1]:
                    continue
                elif first_image and prev_action != d[1]:
                    create_image(prev_frame, prev_action, prev_videofile_name, dir_path, dest_dir)
                    prev_frame = d[0]
                    prev_action = d[1]
                    prev_videofile_name = file[:-4]
                else:
                    create_image(d[0], d[1], file[:-4], dir_path, dest_dir)


