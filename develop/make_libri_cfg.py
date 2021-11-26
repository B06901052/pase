import os
import argparse
import numpy as np


def check_ext(fname, exts):
    for ext in exts:
        if fname.endswith(ext):
            return True

    return False


class LibriParser(object):
    def __init__(self, args):
        self.path = args.libri_path
        self.splits = {
            "train": args.train,
            "valid": args.valid,
            "test": args.test,
        }
        self.datas = {
            "train": [],
            "valid": [],
            "test": [],
        }
        self.exts = args.exts

    def load(self):
        def ext_filter(fname): return check_ext(fname, self.exts)

        for split in self.splits:
            for s in self.splits[split]:
                path = os.path.join(self.path, s)
                for _, _, files in os.walk(path):
                    self.datas[split] += list(filter(ext_filter, files))

    def gen_data_scp(self, dirpath):
        for split in self.datas:
            path = os.path.join(dirpath, "{}.scp".format(split))
            with open(path, 'w') as f:
                text = "\n".join(self.datas[split])
                f.write(text)

    def gen_data_dict(self, dirpath):
        spks = set()
        spk2idx = dict()
        fname2idx = dict()
        for split in self.datas:
            for fname in self.datas[split]:
                idx = fname.find("_")
                spks.add(fname[:idx])

        for i, spk in enumerate(spks):
            spk2idx[spk] = i

        for split in self.datas:
            for fname in self.datas[split]:
                idx = fname.find("_")
                spk = fname[:idx]
                fname2idx[fname] = spk2idx[spk]

        fname2idx = np.array(fname2idx)
        path = os.path.join(dirpath, "libri_dict.npy")
        np.save(path, fname2idx, allow_pickle=True)


def getargs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--libri_path', type=str, help='path to libri')
    parser.add_argument('--dst_path', type=str,
                        help='dst path to store configuration files')
    parser.add_argument('--exts', action='append',
                        help='audio file extensions', default=[".flac", ".wav", ".mp3"])
    parser.add_argument('--train', action='append',
                        help='which splits should be used in train')
    parser.add_argument('--valid', action='append',
                        help='which splits should be used in valid')
    parser.add_argument('--test', action='append',
                        help='which splits should be used in test')
    return parser.parse_args()


if __name__ == "__main__":
    args = getargs()
    if not os.path.exists(args.dst_path):
        os.makedirs(args.dst_path)

    libri_parser = LibriParser(args)
    libri_parser.load()
    libri_parser.gen_data_scp(args.dst_path)
    libri_parser.gen_data_dict(args.dst_path)
