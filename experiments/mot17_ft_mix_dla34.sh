cd src
python train.py mot --exp_id mot17_ft_mix_cbamhead --load_model '../models/dla34_cbamhead_ep10.pth' --num_epochs 20 --lr_step '15' --data_cfg '../src/lib/cfg/mot17.json'
cd ..