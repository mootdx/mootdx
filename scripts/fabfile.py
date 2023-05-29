from fabric.api import local
from fabric.api import task
from git import Repo

repo = Repo('.')

# pip install fabric3 gitpython

@task(alias='t')
def test():
    """执行本地测试"""
    local('py.test tests -v')


@task(alias='sync')
def sync(branch=repo.active_branch.name):
    """同步所有仓库"""
    pull(branch)
    push(branch)


@task(alias='push')
def push(branch=repo.active_branch.name):
    """推送同步所有仓库"""
    local(f'git push origin {branch} --tags')
    local(f'git push github {branch} --tags')
    local(f'git push gitee {branch} --tags')


@task(alias='pull')
def pull(branch=repo.active_branch.name):
    """拉取同步所有仓库"""
    local(f'git pull origin {branch} --tags')
    local(f'git pull github {branch} --tags')
    local(f'git pull gitee {branch} --tags')


@task
def fetch(branch=repo.active_branch.name):
    """同步所有仓库到本地"""
    local(f'git fetch gitee {branch}')
    local(f'git fetch origin {branch}')
    local(f'git fetch github {branch}')


@task
def help():
    """使用帮助"""
    text = open('README.rst').read()
    print(text)
