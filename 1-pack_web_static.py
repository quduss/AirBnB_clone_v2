#!/usr/bin/python3
"""fabric script that creates a .tgx archive from all
files in the web_static directory of AirBnB_v2"""


from datetime import datetime
import os
from fabric.api import *


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
