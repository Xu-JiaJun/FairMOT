import os
import time

import cv2
from PIL import Image


def images2video(dir_path, video_path):
    images = os.listdir(dir_path)
    images.sort(key=lambda x: int(x[:-4]))  # 从小到大排序
    fps = 15
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")

    im = Image.open(os.path.join(dir_path, images[0]))  # 用于获取图片尺寸，因此需要保持一致
    output_video_path = os.path.join(video_path, 'video.mp4')
    print(output_video_path)
    video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, im.size)
    for image_path in images:
        frame = cv2.imread(os.path.join(dir_path, image_path))
        print('将' + image_path + '加入视频')
        video_writer.write(frame)
    video_writer.release()

    return output_video_path


def write_log_to_txt(filename, context):
    dir_path = '../log'
    file_path = os.path.join(dir_path, filename + '.txt')
    if filename != '':
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time())))
            f.write(' ')
            f.write(context)
            f.write('\n')


def read_log(filename):
    line_list = []
    dir_path = '../log'
    file_path = os.path.join(dir_path, filename + '.txt')
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            line_list.append(line)
    return line_list
