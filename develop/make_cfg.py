import os
import argparse
import numpy as np


class LibriParser(object):
    def __init__(self, config):
        self.path = config["path"]
        self.splits = config["splits"]
        self.datas = {
            "train": [],
            "valid": [],
            "test": [],
        }
        self.ext = config["ext"]

    def load(self):
        def ext_filter(fname): return fname.endswith(self.ext)

        for split in self.splits:
            for s in self.splits[split]:
                path = os.path.join(self.path, s)
                for pardir, subdirs, files in os.walk(path):
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
    # TODO: make config yaml
    # TODO: extension should support multi
    parser = argparse.ArgumentParser()
    parser.add_argument('--libri_path', type=str, help='path to libri')
    parser.add_argument('--dst_path', type=str,
                        help='dst path to store configuration files')
    parser.add_argument('--extension', action='append',
                        help='audio file extensions', default=[".flac", ".wav", ".mp3"])
    return parser.parse_args()


if __name__ == "__main__":
    args = getargs()
    config = {
        "path": args.libri_path,
        "splits": {
            # , "train-clean-360", "train-other-500"
            "train": ["train-clean-100"],
            "valid": ["dev-clean", "dev-other"],
            "test": ["test-clean", "test-other"],
        },
        "ext": ".flac",
    }
    libri_parser = LibriParser(config)
    libri_parser.load()
    libri_parser.gen_data_scp("./develop/data")
    libri_parser.gen_data_dict("./develop/data")
