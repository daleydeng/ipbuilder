#!/usr/bin/env python
import os.path as osp
import sys
cur_dir = osp.dirname(__file__)
sys.path.insert(0, cur_dir+'/../')
from glob import glob
from ipbuilder.bilibili import BilibiliUploader, VideoPart
import toml
import click

def file_name(f):
    return osp.basename(osp.splitext(f)[0])

def check_length(name):
    assert len(name) < 76, f"name is too long: {name}:{len(name)}"

def main(video_f: str, bvid: str, cfg_f='~/.config/bilibili.toml'):

    cfg_f = osp.expanduser(cfg_f)
    assert osp.exists(cfg_f)
    cfg = toml.load(open(cfg_f))

    username = cfg['username']
    password = cfg['password']
    uploader = BilibiliUploader()
    uploader.login(username=username, password=password)

    parts = []
    name = file_name(video_f)
    check_length(name)
    vid = VideoPart(
        path=video_f,
        title=name,
        desc=name,
    )
    parts.append(vid)

    uploader.edit(
        bvid=bvid,
        parts=parts,
    )

if __name__ == "__main__":
    import typer
    typer.run(main)
