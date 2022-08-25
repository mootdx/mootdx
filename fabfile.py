from fabric.api import local
from fabric.api import task
from git import Repo

repo = Repo(".")


@task(alias="t")
def test():
    """push github rev"""
    local("py.test tests -v")


@task(alias="lp")
def lp(branch=repo.active_branch.name):
    """# push github rev"""
    pull()
    push()


@task(alias="up")
def push(branch=repo.active_branch.name):
    """# push github rev"""
    local(f"git push origin {branch} --tags")
    local(f"git push github {branch} --tags")


@task(alias="pl")
def pull(branch=repo.active_branch.name):
    """# push github rev"""
    local(f"git pull origin {branch} --tags")
    local(f"git pull github {branch} --tags")


@task
def help():
    """使用帮助"""
    text = open("README.rst").read()
    print(text)
