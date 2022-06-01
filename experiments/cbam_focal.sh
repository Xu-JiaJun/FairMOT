cd src
python train.py mot --exp_id cbamblock_focal_dla34 --load_model '../models/fairmot_dla34.pth' --data_cfg '../src/lib/cfg/data.json' --gpus 0,1 --id_loss focal
cd ..