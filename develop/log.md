# PASE reproduce

## Environment Setup

* python <= 3.7

* install [codec2](https://github.com/drowe67/codec2)
  * follow the steps in [codec2](https://github.com/drowe67/codec2)
    * git, build-essential, cmake can be installed by conda
      * `conda install -c anaconda git conda-build cmake`
  * `conda install -c conda-forge codec2`
  * `pip install Cython`
  * `cp path_to_codec2/src path_to_miniconda3/envs/env_name/include/your_python_version/codec2`
  * `cp path_to_codec2/build_linux/codec2/version.h path_to_miniconda3/envs/env_name/include/your_python_version/codec2`
  * `pip install pycodec2`

* install [kaldi](https://github.com/kaldi-asr/kaldi/blob/master/INSTALL)
  * note that it could make parallelly(`make -j 8`)
  * remember install **irstlm**, which is not installed by default.

## Pretrain Steps

* ./develop/make_symlink.py
  * make symlinks of all librispeech data to one dir

```bash
python ./develop/make_symlink.py \
  --libri_path "/livingrooms/public/LibriSpeech" \
  --dst_path "./corpora/LibriSpeech"
```

* ./develop/make_cfg.py
  * input
    * corpora_path (no subdir, all things in it are audio files)

* ./data/prep/unsupervised_data_cfg_librispeech.py
  * input
    * corpora_path (no subdir, all things in it are audio files)
    * train_scp
      * e.g. data/libri_tr.scp
    * test_scp
      * e.g. data/libri_te.scp
    * libri_dict
      * a dict (store by numpy @@)
        * key: filename (not filepath)
        * value: spkid (int)
        * 

* make_trainset_statistics.sh
  * input
    * corpora (no subdir, all things in it are audio files)
      * load by PairWavDataset
        * inherit WavDataset
    * data_cfg
      * train_scp
        * e.g. data/libri_tr.scp
      * test_scp
        * e.g. data/libri_te.scp
