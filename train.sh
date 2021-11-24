source ~/.bashrc
conda activate pase

python -u  train.py --batch_size 16 --epoch 400 --save_path model/100h_pase+_ckpt \
	       --num_workers 8 --warmup 10000000 --net_cfg cfg/workers/workers+.cfg \
	       --fe_cfg cfg/frontend/PASE+.cfg --data_cfg develop/data/data_100h.cfg \
	       --min_lr 0.0005 --fe_lr 0.001 --data_root corpora/LibriSpeech/ \
	       --dtrans_cfg cfg/distortions/pase+.cfg \
	       --stats develop/data/librispeech100h_tmp_stats.pkl \
	       --chunk_size 32000 \
	       --tensorboard False \
	       --backprop_mode base\
	       --random_scale True\
	       --lr_mode poly