import json
import os.path
import uuid
from argparse import ArgumentParser
from threading import Thread

from flask import Flask, jsonify, request
from flask_cors import CORS

from demo import demo
from app_utils import write_log_to_txt, read_log, images2video

app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route('/track', methods=['POST'])
def track():
    """
    主要方法，使用模型对用户指定视频进行跟踪
    方法POST
    参数：
    input_dir: 输入的视频文件
    output_dir: 输出帧及视频的路径
    thres: 跟踪置信度
    gen_video: 是否生成跟踪视频
    """
    # get and check request
    j_data = json.loads(request.data)
    input_dir = j_data['input_dir']
    output_dir = j_data['output_dir']
    thres = j_data['thres']
    gen_video = j_data['gen_video']

    print(input_dir, output_dir, thres, gen_video)

    # if not os.path.isdir(input_dir):
    #     return jsonify(code=-1, msg="input dir not a folder")

    if not os.path.isdir(output_dir):
        return jsonify(code=-1, msg="output dir not exist or not a folder")

    # load args and change
    parser = ArgumentParser()
    opt = parser.parse_args()
    with open('commandline_args.txt', 'r') as f:
        opt.__dict__ = json.load(f)
    setattr(opt, 'input_video', input_dir)
    setattr(opt, 'output_root', output_dir)
    setattr(opt, 'conf_thres', float(thres))
    if gen_video:
        setattr(opt, 'output_format', 'video')

    # run demo
    uid = str(uuid.uuid4())
    suid = ''.join(uid.split('-'))

    def do_track(_opt, _suid):
        demo(opt, suid=suid)

    thread = Thread(target=do_track, kwargs={'_opt': opt, '_suid': suid})
    thread.start()
    write_log_to_txt(suid, '开始跟踪{}'.format(input_dir))
    write_log_to_txt(suid, '任务编号: {}'.format(suid))
    print('记录保存到log/{}.txt'.format(suid))

    return jsonify(code=0, msg="success", suid=suid)


@app.route('/track_frame', methods=['POST'])
def track_frame():
    """
    主要方法，使用模型对用户指定视频帧进行跟踪
    方法POST
    参数：
    input_dir: 输入的视频文件
    output_dir: 输出帧及视频的路径
    thres: 跟踪置信度
    gen_video: 是否生成跟踪视频
    """
    # get and check request
    j_data = json.loads(request.data)
    input_dir = j_data['input_dir']
    output_dir = j_data['output_dir']
    thres = j_data['thres']
    gen_video = j_data['gen_video']

    print(input_dir, output_dir, thres, gen_video)

    # if not os.path.isdir(input_dir):
    #     return jsonify(code=-1, msg="input dir not a folder")

    if not os.path.isdir(output_dir):
        return jsonify(code=-1, msg="output dir not exist or not a folder")

    uid = str(uuid.uuid4())
    suid = ''.join(uid.split('-'))

    # 根据视频帧生成对应视频
    write_log_to_txt(suid, '开始生成视频，读取{}中视频帧'.format(input_dir))
    video_path = images2video(input_dir, output_dir)
    write_log_to_txt(suid, '根据视频帧生成视频：{}'.format(video_path))
    print('video path:', video_path)

    # load args and change
    parser = ArgumentParser()
    opt = parser.parse_args()
    with open('commandline_args.txt', 'r') as f:
        opt.__dict__ = json.load(f)
    setattr(opt, 'input_video', video_path)
    setattr(opt, 'output_root', output_dir)
    setattr(opt, 'conf_thres', float(thres))
    if gen_video:
        setattr(opt, 'output_format', 'video')

    # run demo
    def do_track(_opt, _suid):
        demo(opt, suid=suid)

    thread = Thread(target=do_track, kwargs={'_opt': opt, '_suid': suid})
    thread.start()
    write_log_to_txt(suid, '开始跟踪{}'.format(input_dir))
    write_log_to_txt(suid, '任务编号: {}'.format(suid))
    print('记录保存到log/{}.txt'.format(suid))

    return jsonify(code=0, msg="success", suid=suid)


# 获取指定任务的记录
@app.route('/log', methods=['GET'])
def get_log():
    suid = request.args.get('suid')
    print('suid', suid)
    logs = read_log(suid)
    return jsonify(code=0, msg='success', logs=logs)


# main function
if __name__ == "__main__":
    app.run(debug=True, port=8090)
