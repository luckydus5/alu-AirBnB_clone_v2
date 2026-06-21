#!/usr/bin/python3
"""Fabric script that packs and distributes an archive to the web servers."""
from fabric.api import env, put, run, local
from datetime import datetime
from os.path import exists

env.hosts = ['13.218.57.12', '44.202.228.82']


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


def do_deploy(archive_path):
    """Distribute an archive to the web servers and deploy it.

    Returns True if all operations succeed, otherwise False.
    """
    if not exists(archive_path):
        return False
    try:
        filename = archive_path.split("/")[-1]
        name = filename.split(".")[0]
        release_path = "/data/web_static/releases/{}/".format(name)

        put(archive_path, "/tmp/{}".format(filename))
        run("mkdir -p {}".format(release_path))
        run("tar -xzf /tmp/{} -C {}".format(filename, release_path))
        run("rm /tmp/{}".format(filename))
        run("mv {0}web_static/* {0}".format(release_path))
        run("rm -rf {}web_static".format(release_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(release_path))

        print("New version deployed!")
        return True
    except Exception:
        return False


def deploy():
    """Pack the web_static folder then deploy the archive to the servers.

    Returns the return value of do_deploy, or False if packing failed.
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
