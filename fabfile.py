from fabric.api import local
from fabric.api import task

from git import Repo
repo = Repo(".")


@task
def test():
    """push github rev"""
    local('py.test tests -v')


@task(alias='gp')
def push(branch=repo.active_branch.name):
    """# push github rev"""
    local(f'git push origin {branch} --tags')
    local(f'git push github {branch} --tags')


@task(alias='gl')
def pull(branch=repo.active_branch.name):
    """# push github rev"""
    local(f'git pull origin {branch} --tags')
    local(f'git pull github {branch} --tags')


@task
def help():
    """使用帮助"""
    text = open('README.rst').read()
    text = text
    print(text)
