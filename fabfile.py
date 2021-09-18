from fabric.api import local
from fabric.api import task


@task
def test():
    """push github rev"""
    local('py.test tests -v')


@task
def push(branch='develop'):
    """# push github rev"""
    local(f'git push origin {branch} --tags')
    local(f'git push github {branch} --tags')


@task
def pull(branch='develop'):
    """# push github rev"""
    local(f'git pull origin {branch} --tags')
    local(f'git pull github {branch} --tags')


@task
def help():
    """使用帮助"""
    text = open('README.rst').read()
    text = text
    print(text)
