import os
import errno
import argparse
from typing import get_args


def getargs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--libri_path', type=str, help='path to libri')
    parser.add_argument('--dst_path', type=str,
                        help='dst path to where you want to put symlink')
    parser.add_argument('--extention', action='append',
                        help='audio file extensions', default=[".flac", ".wav", ".mp3"])
    return parser.parse_args()


def check_ext(fname, exts):
    for ext in exts:
        if fname.endswith(ext):
            return True

    return False


if __name__ == "__main__":
    args = getargs()
    for pardir, subdirs, files in os.walk(args.libri_path):
        for f in files:
            if check_ext(f, args.extention):
                src = os.path.join(pardir, f)
                dst = os.path.join(args.dst_path, f)
                try:
                    os.symlink(src, dst)
                except OSError as e:
                    if e.errno == errno.EEXIST:
                        pass
                    else:
                        print("fail: ", src)
