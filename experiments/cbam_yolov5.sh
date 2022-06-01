cd src
python train.py mot --exp_id yolov5s_cbam --data_cfg '../src/lib/cfg/data_all.json' --lr 5e-4 --batch_size 12 --wh_weight 0.5 --multi_loss 'fix' --arch 'yolo' --reid_dim 64 --gpus 0,1
cd ..