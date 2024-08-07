#!/usr/bin/python3
"""fabric script that uploads a .tgz archive to my servers
. It also decompresses the archive in the servers"""
import os
from fabric.api import *


env.user = 'ubuntu'
env.hosts = ['54.226.24.96', '52.201.162.174']


def do_deploy(archive_path):
    """task that creates the archive"""
    if not os.path.exists(archive_path):
        return False

    copy_tgz = archive_path[:]
    copy_tgz = copy_tgz.split('/')
    copy_tgz = copy_tgz[-1]
    upload = put(f'{archive_path}', f'/tmp/{copy_tgz}')
    if upload.failed:
        return False
    copy = copy_tgz.split('.tgz')[0]
    comm = f'mkdir /data/web_static/releases/{copy}'
    result = run(comm)
    if result.failed:
        return False
    comm = f'tar -xzf /tmp/{copy_tgz} -C /data/web_static/releases/{copy}'
    result = run(comm)
    if result.failed:
        return False
    result = run(f'rm /tmp/{copy_tgz}')
    if result.failed:
        return False
    string_1 = f'mv /data/web_static/releases/{copy}/web_static/*'
    string_2 = f' /data/web_static/releases/{copy}'
    comm = f'{string_1}{string_2}'
    result = run(comm)
    if result.failed:
        return False
    comm = f'rm -rf /data/web_static/releases/{copy}/web_static'
    result = run(comm)
    if result.failed:
        return False
    comm = f'rm -rf /data/web_static/current'
    result = run(comm)
    if result.failed:
        return False
    comm = f'ln -s /data/web_static/releases/{copy} /data/web_static/current'
    result = run(comm)
    if result.failed:
        return False
    print("New version deployed!")
    return True
