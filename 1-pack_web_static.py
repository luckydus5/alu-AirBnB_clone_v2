#!/usr/bin/python3
"""Fabric script that generates a .tgz archive from the web_static folder."""
from fabric.api import local
from datetime import datetime


def do_pack():
    """Generate a .tgz archive of the web_static folder.

    Returns the archive path on success, otherwise None.
    """
    time = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_path = "versions/web_static_{}.tgz".format(time)
    try:
        local("mkdir -p versions")
        print("Packing web_static to {}".format(archive_path))
        local("tar -cvzf {} web_static".format(archive_path))
        return archive_path
    except Exception:
        return None
