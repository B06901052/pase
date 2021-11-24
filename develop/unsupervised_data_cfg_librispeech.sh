source ~/.bashrc
conda activate pase

python ./unsupervised_data_cfg_librispeech.py \
  --data_root ./corpora/LibriSpeech \
  --train_scp ./develop/data/train.scp \
  --valid_scp ./develop/data/valid.scp \
  --test_scp ./develop/data/test.scp \
  --libri_dict ./develop/data/libri_dict.npy \
  --cfg_file ./develop/data/data.cfg