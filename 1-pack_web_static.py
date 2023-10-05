#!/usr/bin/python3
""" a fabric script that generates an archive of the directory web_static """
from datetime import datetime
from fabric.api import local


def do_pack():
    """ a function that creates and verbose a gzip directory of web_static dir
        and save it in versions directory """
    local("mkdir -p versions")
    res = local("tar -cvzf versions/web_static_{}.tgz web_static"
                .format(datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")),
                capture=True)
    if res.failed:
        return None
    print(res)
    return res
