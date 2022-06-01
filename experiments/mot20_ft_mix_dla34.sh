cd src
python train.py mot --exp_id mot20_ft_mix_cbamhead --load_model '../models/dla34_cbamhead_ep10.pth' --num_epochs 20 --lr_step '15' --data_cfg '../src/lib/cfg/mot20.json'
cd ..