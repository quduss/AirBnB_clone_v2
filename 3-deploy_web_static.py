#!/usr/bin/python3
"""fabric script that creates a .tgz archive and deploys
it to my servers. It also decompresses the archive
at each of the servers"""
import os
from fabric.api import *
from 1-pack_web_static import do_pack
from 2-do_deploy_web_static import do_deploy


env.user = 'ubuntu'
env.hosts = ['100.24.244.250', '54.161.241.33']


def deploy():
    """creates and deploys new archive to my servers.
    It also decompresses the archive at each of the servers"""
    new_archive = do_pack()
    if new_archive is None:
        return False
    ret = do_deploy(new_archive)
    return ret
