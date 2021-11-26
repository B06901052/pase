import os
import errno
import argparse


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

    # make dst dir
    if not os.path.exists(args.dst_path):
        os.makedirs(args.dst_path)

    # find all audio files and create symlink to them (placed at dst_path)
    for pardir, subdirs, files in os.walk(args.libri_path):
        for f in files:
            # check whether is audio file
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
