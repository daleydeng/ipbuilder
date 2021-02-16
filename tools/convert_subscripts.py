#!/usr/bin/env python
import os
import os.path as osp
from glob import glob
from subprocess import check_call

tpl = 'ffmpeg -i \"{src}\" \"{dst}\"'

def run_cmd(cmd):
    print (cmd)
    check_call(cmd, shell=True)

def main(*files, ext='.srt'):
    for f in files:
        dst_f = osp.splitext(f)[0] + ext
        if osp.exists(dst_f):
            continue

        run_cmd(tpl.format(src=f, dst=dst_f))


if __name__ == "__main__":
    import fire
    fire.Fire(main)
