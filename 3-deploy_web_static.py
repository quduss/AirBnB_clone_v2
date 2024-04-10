#!/usr/bin/python3
"""fabric scripts"""
from fabric.api import *
from datetime import datetime
import os


env.user = 'ubuntu'
env.hosts = ['100.24.244.250', '54.161.241.33']


def do_pack():
    """task that creates the archive"""
    # Create 'versions' directory if it doesn't exist
    if not os.path.exists('versions'):
        os.makedirs('versions')

    # Generate the filename based on current date and time
    now = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f'web_static_{now}.tgz'
    archive_path = os.path.join('versions', filename)

    # Compress the web_static folder into a .tgz archive
    result = local(f'tar -czvf {archive_path} web_static', capture=True)

    # Check if the archive was created successfully
    if result.succeeded:
        return archive_path
    else:
        return None


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
    return True


new_archive = do_pack()


def deploy():
    """creates and deploys new archive to my servers.
    It also decompresses the archive at each of the servers"""
    if new_archive is None:
        return False
    ret = do_deploy(new_archive)
    return ret
