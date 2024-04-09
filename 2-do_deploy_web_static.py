#!/usr/bin/python3
"""fabric script that uploads a .tgz archive to my servers
. It also decompresses the archive in the servers"""


import os
from fabric.api import *


def do_deploy(archive_path):
    """task that creates the archive"""
    if not os.path.exists(archive_path):
        return False
    env.user = 'ubuntu'
    env.hosts = ['100.24.244.250', '54.161.241.33']

    copy_tgz = archive_path[:]
    copy_tgz = copy_tgz.split('/')
    copy_tgz = copy_tgz[-1]
    upload = put(f'{archive_path}', f'/tmp/{copy_tgz}')
    if upload.failed:
        return False
    copy = copy_tgz.split('.tgz')[0]
    sudo(f'mkdir /data/web_static/releases/{copy}')
    result = sudo(f'tar -xzvf /tmp/{copy_tgz} -C /data/web_static/releases/{copy}')
    if result.failed:
        return False
    result = sudo(f'rm /tmp/{copy_tgz} /data/web_static/current')
    if result.failed:
        return False
    result = sudo(f'ln -s /data/web_static/releases/{copy} /data/web_static/current')
    if result.failed:
        return False
    return True
