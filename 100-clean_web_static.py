#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Web application deployment with Fabric module.
"""
from datetime import datetime
from fabric.api import local, put, run, env, cd, lcd

env.user = 'ubuntu'
env.hosts = ["54.209.215.140", "52.87.217.9"]


def do_pack():
    """
        Targging project directory into packages as .tgz
    """
    dt_now = datetime.now().strftime("%Y%m%d%H%M%S")
    local('sudo mkdir -p ./versions')
    pack_path = './versions/web_static_{}'.format(dt_now)
    local('sudo tar -czvf {}.tgz web_static'.format(pack_path))
    pack_name = '{}.tgz'.format(pack_path)
    if pack_name:
        return pack_name
    else:
        return None


def do_deploy(archive_path):
    """
        Deploy boxing package file (tgz)
    """
    try:
        archv = archive_path.split('/')[-1]
        path = '/data/web_static/releases/' + archv.strip('.tgz')
        curr = '/data/web_static/current'
        put(archive_path, '/tmp')
        run('mkdir -p {}'.format(path))
        run('tar -xzf /tmp/{} -C {}'.format(archv, path))
        run('rm /tmp/{}'.format(archv))
        run('mv {}/web_static/* {}'.format(path, path))
        run('rm -rf {}/web_static'.format(path))
        run('rm -rf {}'.format(curr))
        run('ln -s {} {}'.format(path, curr))
        print('New version deployed!')
        return True
    except:
        return False


def deploy():
    """
    Function call do_pack and do_deploy
    """
    archv_path = do_pack()
    ans = do_deploy(archv_path)
    return ans


def do_clean(number=0):
    """
    Keep cleanning thy repositories
    """
    if number == 0 or number == 1:
        with lcd('./versions/'):
            local("ls -lv | rev | cut -f 1 | rev | \
            head -n +1 | xargs -d '\n' rm -rf")
        with cd('/data/web_static/releases/'):
            run("sudo ls -lv | rev | cut -f 1 | \
            rev | head -n +1 | xargs -d '\n' rm -rf")
    else:
        with lcd('./versions/'):
            local("ls -lv | rev | cut -f 1 | rev | \
            head -n +{} | xargs -d '\n' rm -rf".format(number))
        with cd('/data/web_static/releases/'):
            run("sudo ls -lv | rev | cut -f 1 | \
            rev | head -n +{} | xargs -d '\n' rm -rf".format(number))
