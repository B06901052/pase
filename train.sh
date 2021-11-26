# config

libri_path="/mnt/diskb/corpora/LibriSpeech"
wav_path="/mnt/diskb/corpora/libri_wav"
task_name="libri_100h"
plus="+"
train_splits=("train-clean-100")
valid_splits=("dev-clean" "dev-other")
test_splits=("test-clean" "test-other")

# prepare data: make symlink

python develop/make_symlink.py \
	--libri_path "${libri_path}" \
	--dst_path "${wav_path}"

# prepare data: make data splits files (scp) and spk2idx (npy)

if  ! [ -f "./runs/${task_name}/cfg/libri_dict.npy" -a \
       	-f "./runs/${task_name}/cfg/train.scp" -a \
	   	-f "./runs/${task_name}/cfg/valid.scp" -a \
	   	-f "./runs/${task_name}/cfg/test.scp" ]; then

	# concatenate splits to single line command

	train_splits_str=""
	for split in ${train_splits[@]}; do
	  	train_splits_str="${train_splits_str}--train ${split} "
	done
	valid_splits_str=""
	for split in ${valid_splits[@]}; do
	  	valid_splits_str="${valid_splits_str}--valid ${split} "
	done
	test_splits_str=""
	for split in ${test_splits[@]}; do
	  	test_splits_str="${test_splits_str}--test ${split} "
	done

	python develop/make_libri_cfg.py \
	  	--libri_path "${libri_path}" \
	  	--dst_path "./runs/${task_name}/cfg" \
	  	$train_splits_str \
	  	$valid_splits_str \
	  	$test_splits_str
fi

# prepare data: make data cfg

if  ! [ -f "./runs/${task_name}/cfg/data.cfg" ]; then
	python unsupervised_data_cfg_librispeech.py \
		--data_root "${wav_path}" \
		--train_scp "./runs/${task_name}/cfg/train.scp" \
		--valid_scp "./runs/${task_name}/cfg/valid.scp" \
		--test_scp "./runs/${task_name}/cfg/test.scp" \
		--libri_dict "./runs/${task_name}/cfg/libri_dict.npy" \
		--cfg_file "./runs/${task_name}/cfg/data.cfg"
fi

# prepare data: make librispeech_stats.pkl

if  ! [ -f "./runs/${task_name}/cfg/librispeech_stats.pkl" ]; then
	python make_trainset_statistics.py \
		--data_root "${wav_path}" \
		--data_cfg "./runs/${task_name}/cfg/data.cfg"\
		--net_cfg "cfg/workers/workers${plus}.cfg" \
		--out_file "./runs/${task_name}/cfg/librispeech_stats.pkl" 
fi

# prepare data: prepare_openslr_rirs_cfg

python data/prep/prepare_openslr_rirs_cfg.py \
	--data_root "data/simulated_rirs_16k" \
	--out_file "cfg/distortions/pase+.cfg" \
	--existing_cfg "cfg/distortions/pase+.cfg"


# prepare data: modify distortions cfg

python ./develop/modify_distortions_cfg.py \
	--dtrans_cfg "cfg/distortions/pase+.cfg" \
	--overlap_dir "${wav_path}" \
	--overlap_list "./runs/${task_name}/cfg/test.scp"

python -u  train.py \
	`# hyperparameter` \
	--batch_size 8 \
	--epoch 400 \
	--warmup 10000000 \
	--min_lr 0.0005 \
	--fe_lr 0.001 \
	--lr_mode poly \
	--num_workers 8 \
	`# augmentation` \
	--random_scale True\
	--backprop_mode base\
	--chunk_size 32000 \
	--tensorboard True \
	`# model related` \
	--net_cfg cfg/workers/workers+.cfg \
	--fe_cfg cfg/frontend/PASE+.cfg \
    --dtrans_cfg cfg/distortions/pase+.cfg \
	`# path` \
	--save_path "./runs/${task_name}/ckpt" \
	--data_cfg "./runs/${task_name}/cfg/data.cfg" \
	--data_root "${wav_path}" \
	--stats "./runs/${task_name}/cfg/librispeech_stats.pkl"