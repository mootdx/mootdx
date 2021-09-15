from fabric.api import local
from fabric.api import task


@task
def test():
    """push github rev"""
    local('py.test tests -v')


@task
def push():
    """# push github rev"""
    local('git push origin develop --tags')
    # local('git push github develop --tags')


@task
def pull():
    """# push github rev"""
    local('git pull origin develop --tags')


@task
def help():
    """使用帮助"""
    text = open('README.rst').read()
    text = text
    print(text)
