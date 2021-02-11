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

def main(src_d: str, title: str, cfg_f='~/.config/bilibili.toml', copyright=2, tid=208, tag='', desc='', source='course', jobs=1):

    cfg_f = osp.expanduser(cfg_f)
    assert osp.exists(cfg_f)
    cfg = toml.load(open(cfg_f))

    username = cfg['username']
    password = cfg['password']
    if not desc:
        desc = title

    uploader = BilibiliUploader()
    uploader.login(username=username, password=password)
    jobs = int(jobs)
    parts = []
    for video_f in sorted(glob(src_d+'/*.mp4')):
        name = file_name(video_f)
        vid = VideoPart(
            path=video_f,
            title=name,
            desc=name,
        )
        parts.append(vid)

    avid, bvid = uploader.upload(
        parts=parts,
        copyright=copyright,
        title=title,
        tid=tid,
        tag=tag,
        desc=desc,
        source=source,
        thread_pool_workers=jobs,
    )

if __name__ == "__main__":
    import typer
    typer.run(main)
