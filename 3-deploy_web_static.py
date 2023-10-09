#!/usr/bin/python3
"""web application deployment with Fabric module"""
from datetime import datetime
import os
from fabric.api import env, local, put, run, runs_once


env.hosts = ["54.209.215.140", "52.87.217.9"]
"""list host server IP addresses."""

@runs_once
def do_pack():
    """
        Archives static files
    """
    if not os.path.isdir("versions"):
        os.mkdir("versions")
    crnt_time = datetime.now()
    res_oupt = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        crnt_time.year,
        crnt_time.month,
        crnt_time.day,
        crnt_time.hour,
        crnt_time.minute,
        crnt_time.second
    )
    try:
        print("Packing web_static to {}".format(res_oupt))
        local("tar -cvzf {} web_static".format(res_oupt))
        archize_size = os.stat(res_oupt).st_size
        print("web_static packed: {} -> {} Bytes".format(res_oupt, archize_size))
    except Exception:
        res_oupt = None
    return res_oupt


def do_deploy(archive_path):
    """
        Deploys static files to host servers.
        Args:
            archive_path: Path to archived static files.
    """
    if not os.path.exists(archive_path):
        return False
    success = False
    f_name = os.path.basename(archive_path)
    dir_name = f_name.replace(".tgz", "")
    dir_path = "/data/web_static/releases/{}/".format(dir_name)
    try:
        put(archive_path, "/tmp/{}".format(f_name))
        run("mkdir -p {}".format(dir_path))
        run("tar -xzf /tmp/{} -C {}".format(f_name, dir_path))
        run("rm -rf /tmp/{}".format(f_name))
        run("mv {}web_static/* {}".format(dir_path, dir_path))
        run("rm -rf {}web_static".format(dir_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(dir_path))
        print('New version deployed!')
        success = True
    except Exception:
        success = False
    return success


def deploy():
    """
        Archives and deploys static files to host servers.
    """
    archv_path = do_pack()
    return do_deploy(archv_path) if archv_path else False
