#!/usr/bin/python3
"""Fabric script that distributes an archive to the web servers."""
from fabric.api import env, put, run
from os.path import exists

env.hosts = ['13.218.57.12', '44.202.228.82']


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

        # Upload the archive to /tmp/ on the server
        put(archive_path, "/tmp/{}".format(filename))

        # Create the release directory and uncompress the archive into it
        run("mkdir -p {}".format(release_path))
        run("tar -xzf /tmp/{} -C {}".format(filename, release_path))

        # Remove the uploaded archive from the server
        run("rm /tmp/{}".format(filename))

        # Move the contents up one level and clean the leftover folder
        run("mv {0}web_static/* {0}".format(release_path))
        run("rm -rf {}web_static".format(release_path))

        # Replace the current symlink with the new release
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(release_path))

        print("New version deployed!")
        return True
    except Exception:
        return False
