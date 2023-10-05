#!/usr/bin/python3
""" a fabric file that contain three functions,
    one that creates a tgz of a directory,
    and another that uploads the file on severs to specific directories
    the last combines them
"""

from fabric.api import put, run, env, local
from datetime import datetime
import os

env.hosts = ["54.90.49.90", "54.165.247.60"]
env.user = 'ubuntu'


def do_pack():
    """ a function that creates and verbose a gzip directory of web_static dir
        and save it in versions directory """
    local("mkdir -p versions")
    path = "versions/web_static_{}.tgz"\
        .format(datetime.strftime(datetime.now(), "%Y%m%d%H%M%S"))
    res = local("tar -cvzf {} web_static".format(path), capture=True)
    if res.failed:
        return None
    return path


def do_deploy(archive_path):
    """ a function witch uploads a tgz file to the server in a specific way """
    if os.path.exists(archive_path) is False:
        return False
    try:
        path = archive_path.replace('/', ' ').replace('.', ' ').split()
        zname = path[1]
        fl_name = path[1] + '.' + path[2]
        dr = '/data/web_static/releases/{}/'.format(zname)
        put(archive_path, '/tmp/')
        run('mkdir -p {}'.format(dr))
        run('tar -xzf /tmp/{} -C {}/'.format(fl_name, dr))
        run('rm /tmp/{}'.format(fl_name))
        run('mv {}/web_static/* {}'.format(dr, dr))
        run('rm -rf {}/web_static'.format(dr))
        current_dir = '/data/web_static/current'
        run('rm -rf {}'.format(current_dir))
        run('ln -s {}/ {}'.format(dr, current_dir))
        return True
    except Exception:
        return False


def deploy():
    """ a function that creates the gzip of a directory and upload
        it to the server in s set of procedures
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
