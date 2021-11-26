# install env

conda env create -f ./env.yaml
conda activate pase
python setup.py install

# download data for augmentation and reverb

cd data
gdown --id 1oaWnurx0nHcUGpr5aiQ1La55S2USmA4p -O - --quiet | tar zxf -
gdown --id 1kDrUM97uoCtPm_kXMMtMkiHLvt26FWIT -O - --quiet | tar zxf -
wget https://www.openslr.org/resources/26/sim_rir_16k.zip
unzip -q sim_rir_16k.zip
cd ..