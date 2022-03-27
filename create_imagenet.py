import numpy as np
import pandas as pd
import os
import cv2
import tqdm
import datetime
from PIL import Image, ImageDraw
from PIL.ImageQt import ImageQt


def create_image(frame_num, action_num, videofile_name, dir_path, dest_dir):
    frame_num = int(float(frame_num))
    action_num = str(int(float(action_num)))
    cap = cv2.VideoCapture(dir_path + '/' + videofile_name + '.mp4')
    cap.set(1, frame_num)
    ret, frame = cap.read()
    if not os.path.isdir(dest_dir + '/' + action_num):
        os.mkdir(dest_dir + '/' + action_num)

    cv2.imwrite('{}/{}/{}.jpg'.format(dest_dir, action_num, videofile_name + '_' + str(frame_num)), frame)


def draw_ball(frame, np_array):
    # print(np_array)
    draw = ImageDraw.Draw(frame)
    x, y = frame.size
    start_x = 580
    start_y = 50
    # ball_x = int(float(np_array[3]) * x)
    # ball_y = int(float(np_array[4]) * y)
    # draw.rectangle((ball_x - 10, ball_y - 10, ball_x + 10, ball_y + 10), outline=(255, 255, 255), width=2)

    draw.ellipse((start_x, start_y, start_x + 30, start_y + 30), outline=(0, 0, 0), width=2)
    draw.ellipse((start_x - 10, start_y - 10, start_x + 40, start_y + 40), outline=(0, 0, 0), width=2)
    draw.ellipse((start_x - 20, start_y - 20, start_x + 50, start_y + 50), outline=(0, 0, 0), width=2)
    draw.rectangle((start_x - 25, start_y - 25, start_x + 55, start_y + 55), outline=(0, 0, 0), width=2)
    draw.line((start_x - 25, start_y - 25, start_x + 55, start_y + 55), fill=(0, 0, 0), width=2)
    draw.line((start_x - 25, start_y + 55, start_x + 55, start_y - 25), fill=(0, 0, 0), width=2)
    draw.line((start_x - 25, start_y + 15, start_x + 55, start_y + 15), fill=(0, 0, 0), width=2)
    draw.line((start_x - 25, start_y, start_x + 55, start_y + 30), fill=(0, 0, 0), width=2)
    draw.line((start_x - 25, start_y + 30, start_x + 55, start_y), fill=(0, 0, 0), width=2)
    return frame


def create_image_return(np_array, np_path):
    frame_num = int(float(np_array.iloc[0]))
    cap = cv2.VideoCapture(np_path[:-3] + 'avi')
    cap.set(1, frame_num)
    ret, frame = cap.read()
    if not ret:
        cap = cv2.VideoCapture(np_path[:-3] + 'mp4')
        cap.set(1, frame_num)
        ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = Image.fromarray(frame)
    original_width, original_height = frame.size
    frame = frame.resize((640, 360))
    frame = draw_ball(frame, np_array)
    # frame = ImageQt(frame)
    return frame, original_width, original_height


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
    return dest_dir


