import os
import json
import argparse


def getargs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dtrans_cfg', type=str, help='distortions_cfg path')
    parser.add_argument('--overlap_dir', type=str)
    parser.add_argument('--overlap_list', type=str)
    return parser.parse_args()


if __name__ == "__main__":
    args = getargs()
    with open(args.dtrans_cfg, 'r') as f:
        cfg = json.load(f)
    cfg["overlap_dir"] = args.overlap_dir
    cfg["overlap_list"] = args.overlap_list
    cfg["downsample_data_root"] = "data/filters"
    cfg["bandrop_data_root"] = "data/filters"
    cfg["noises_dir"] = [
        "data/noise_non_stationary/wavs",
        "data/noise_non_stationary/wavs_bg"
    ]

    with open(args.dtrans_cfg, 'w') as f:
        f.write(json.dumps(cfg, indent=0))
