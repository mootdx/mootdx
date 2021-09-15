# -*- coding: utf-8 -*-
import os

from fabric.api import local
from fabric.api import task

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)


@task
def test():
    # push github rev
    local('py.test tests -v')


@task
def push():
    # push github rev
    local('git push origin develop --tags')
    local('git push github develop --tags')


@task
def pull():
    # push github rev
    local('git pull origin develop --tags')
    local('git pull github develop --tags')


@task
def help():
    text = open('README.md').read()
    text = text
    print(text)


@task
def pack():
    """ 文件打包 """
    local('tar zcfv ./release.tgz '
          '--exclude=.git '
          '--exclude=.tox '
          '--exclude=.env '
          '--exclude=.idea '
          '--exclude=*.tgz '
          '--exclude=*.pyc '
          '--exclude=.vagrant '
          '--exclude=assets/media/* '
          '--exclude=assets/static/* '
          '--exclude=runtime/* '
          '--exclude=.DS_Store '
          '--exclude=.phpintel '
          '--exclude=.template '
          '--exclude=db.sqlite3 '
          '--exclude=Vagrantfile .')
