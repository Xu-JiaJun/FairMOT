cd src
python train.py mot --exp_id mot16_ft_mix_dla --load_model '../models/fairmot_dla34.pth' --num_epochs 30 --lr_step '15' --data_cfg '../src/lib/cfg/mot17.json'
cd ..