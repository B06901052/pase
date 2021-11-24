source ~/.bashrc
conda activate pase

python eval_test.py ${1:-""} ${2:-""} ${3:-""}
