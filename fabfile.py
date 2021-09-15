# -*- coding: utf-8 -*-
import glob
import os

import environ
# import fabtools
from fabric.api import cd, env, local, put
from fabric.api import run as remote
from fabric.api import sudo, task
from fabric.contrib import project
from fabtools import require

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)

etc = environ.Env()
etc.read_env('.fabric')
env.disable_known_hosts = True
env.use_ssh_config = True
env.key_filename = [
    '~/.ssh/id_rsa',
]

env.passwords = {
}

env.roledefs = {
    'dev': {
        'hosts': ['vagrant@127.0.0.1:2222'],
    },
    'pre': {
        'hosts': ['pi@raspberrypi'],
    },
    'rel': {
        'hosts': ['ubuntu@27.0.0.1:2222'],
    }
}

env.excludes = (
    "*.pyc",
    '*.tgz',
    ".DS_Store",
    ".coverage",
    ".*",
    ".git",
    ".hg",
    ".tox",
    ".idea/",
    "docs/",
    "mkdocs.yml",
    ".pytest_cache/",
    'runtime',
    'tests',
    '__pycache__',
    'db.sqlite3',
    'Procfile',
    'README.md',
    '.fabric',
    '.env',
    'README.md',
    'Pipfile',
    'fixtures/',
    'deploy',
    'tests',
    'fabfile.py',
    '.pre-commit-config.yaml',
    'env.*',
)

env.remote_dir = etc('FABRIC_REMOTE_PATH', default='/home/www/ponder/server')
env.project = etc('FABRIC_PROJECT_NAME', default='ponder')
env.local_dir = '.'


def parse_requirements(filename):
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


def remote_exist(file_path):
    return int(remote(f"test -e {file_path} && echo 1 || echo 0")) == 1


def local_exist(file_path):
    return int(local(f"test -e {file_path} && echo 1 || echo 0")) == 1


@task
def help():
    text = open('README.md').read()
    text = text
    print(text)


@task
def echo(msg='hello world'):
    remote(f'echo {msg}')


@task
def setup():
    # Require some Debian/Ubuntu packages
    require.deb.packages([
        'imagemagick',
        'libxml2-dev',
    ])

    # Require a Python package
    # with fabtools.python.virtualenv('/home/myuser/env'):
    #     require.python.package('pyramid')

    # Require an email server
    # require.postfix.server('example.com')

    # # Require a PostgreSQL server
    # require.postgres.server()
    # require.postgres.user('myuser', 's3cr3tp4ssw0rd')
    # require.postgres.database('myappsdb', 'myuser')

    # # Require a supervisor process for our app
    # require.supervisor.process('myapp',
    #     command='/home/myuser/env/bin/gunicorn_paster /home/myuser/env/myapp/production.ini',
    #     directory='/home/myuser/env/myapp',
    #     user='myuser'
    #     )

    # # Require an nginx server proxying to our app
    # require.nginx.proxied_site('example.com',
    #     docroot='/home/myuser/env/myapp/myapp/public',
    #     proxy_url='http://127.0.0.1:8888'
    #     )

    # # Setup a daily cron task
    # fabtools.cron.add_daily('maintenance', 'myuser', 'my_script.py')


@task
def plan(action='check'):
    """crontab 任务部署"""
    # 上传 schedule.py
    put('schedule.py', env.remote_dir)
    PYTHONPATH = f'/home/{env.user}/.pyenv/versions/{env.project}'

    # 切换远程目录
    with cd(env.remote_dir):
        # 运行 schedule.py update
        remote(f'{PYTHONPATH}/bin/pip install click plan')
        remote(f'{PYTHONPATH}/bin/python schedule.py {action}')
        # 删除 schedule.py
        remote('rm -rf schedule.py')


@task
def doctor():
    """自动诊断"""
    pass


@task
def docs():
    """部署docs文档"""
    # 编译文档
    local('mkdocs build')

    # 上传文档
    remote_dir = os.path.join(env.remote_dir, '..', 'manual')
    project.rsync_project(remote_dir=remote_dir,
                          local_dir='./site',
                          delete=True)

    # 删除文档
    local('rm -rf site')


@task
def rel(version=None):
    """发布版本"""
    # 更新文件
    sync()

    # 更新数据
    mkmg()

    # 重启服务
    rest()


@task
def script(name=None):
    project.rsync_project(local_dir='scripts',
                          remote_dir=env.remote_dir + '/scripts',
                          delete=True)
    with cd(env.remote_dir):
        remote(f'{env.py_bin} manage.py runscript {name}')
        remote('rm -rf scripts')


@task
def key(mode='dev'):
    local(
        f'DJANGO_SETTINGS_MODULE=config.settings.{mode} python manage.py drf_create_key'
    )


@task
def envs():
    ''' 环境变量 '''
    from prettytable import PrettyTable
    tab = PrettyTable(["KEY", "VALUE"])
    tab.align["KEY"] = "l"
    tab.align["VALUE"] = "l"
    tab.padding_width = 1

    env.roledefs = []
    _ = [tab.add_row([k, v]) for k, v in env.items() if k != 'excludes']
    print(tab)


@task
def one():
    stop()
    sync()
    migr()
    rest()


@task
def genconf(tpl=None, vars=None):
    from jinja2 import Environment, FileSystemLoader
    environment = Environment(loader=FileSystemLoader("."))
    template = environment.get_template(tpl)
    content = template.render(**vars)

    tpl = tpl.replace('./deploy/', './deploy/.fabric/')

    os.path.isdir(os.path.dirname(tpl)) or os.makedirs(os.path.dirname(tpl))

    with open(tpl, 'w') as fp:
        fp.write(content)

    print('[+]', tpl)


@task
def conf():
    '''同步配置'''
    envs = dict(etc.ENVIRON)
    envs.update(env)

    for tpl in glob.glob("./deploy/**/*.conf", recursive=True):
        genconf(tpl, envs)

    put('./deploy/.fabric/supervisor/server.conf',
        f'/etc/supervisor/conf.d/{env.project}.conf',
        use_sudo=True)

    put('./deploy/.fabric/nginx/default.conf',
        f'/etc/nginx/sites-enabled/{env.project}.conf',
        use_sudo=True)


@task
def jobs():
    ''' 显示jobs '''
    local('python manage.py runjobs -l -v2')


@task
def init(mode='dev'):
    ''' 初始化安装 '''
    local('cp env.server .env')
    mode = f'DJANGO_SETTINGS_MODULE=config.settings.{mode}'

    local(f'{mode} python manage.py migrate')
    local(f'{mode} python manage.py loaddata fixtures/dumps.json')


@task
def cron(action='check'):
    ''' crontab 相关操作 '''
    local(f'python schedule.py {action}')


@task
def lint():
    ''' python 代码风格校验 '''
    local('''pycodestyle **/*.py''')


@task
def su(mode='dev'):
    ''' 创建超级用户 '''
    mode = f'DJANGO_SETTINGS_MODULE=config.settings.{mode}'
    local(
        '{} python manage.py createsuperuser --email ibopo@126.com --username bopo'
            .format(mode))


@task
def dep():
    ''' 安装系统依赖 '''
    py = etc('FABRIC_PYTHON_PATH', default='/root/.pyenv/versions/3.7.4')
    os.path.exists('requirements.txt') or local(
        'pip-compile --output-file=requirements.txt requirements/pre.txt')
    put('requirements.txt', '/tmp/requirements.txt')
    remote(f'{py}/bin/pip install -r /tmp/requirements.txt')
    remote('rm -rf /tmp/requirements.txt')


@task
def dev(host='0.0.0.0:8000'):
    ''' 运行开发服务器 '''
    settings = f'DJANGO_SETTINGS_MODULE=config.settings.dev'
    local(f'{settings} python manage.py runserver_plus {host}')


@task
def pre(mode='pre'):
    ''' 运行开发服务器 '''
    settings = f'DJANGO_SETTINGS_MODULE=config.settings.{mode}'
    # https = '--cert runtime/certs' if ssl else ''
    https = ''
    hosts = '127.0.0.1:8000'
    local(f'{settings} python manage.py runserver_plus {https} {hosts}')


@task
def web():
    ''' 运行开发服务器 '''
    hosts = '127.0.0.1:8000'
    import webbrowser
    webbrowser.get(r'open -a /Applications/Google\ Chrome.app %s').open(
        f'http://{hosts}')


@task
def sh(mode='dev'):
    ''' 运行开发服务器 '''
    local(
        f'DJANGO_SETTINGS_MODULE=config.settings.{mode} python manage.py shell_plus'
    )


@task
def test(environment='dev'):
    ''' 执行项目代码测试 '''
    local(
        'DJANGO_SETTINGS_MODULE=config.settings.{env} py.test -v tests'.format(
            env=environment))


@task
def cov():
    ''' 测试代码覆盖率 '''
    local(
        'python manage.py jenkins --settings=config.settings.dev --enable-coverage --coverage-format html -v2'
    )
    local('open reports/coverage/index.html')


@task
def mock(app=''):
    ''' 填充 mock 数据 '''
    app = f'_{app}' if app else ''
    local(f'python manage.py runscript mock{app} -v3')


@task
def mm(mode='dev'):
    ''' 数据库 migration 操作 '''
    local(
        f'DJANGO_SETTINGS_MODULE=config.settings.{mode} python manage.py makemigrations'
    )
    local(
        f'DJANGO_SETTINGS_MODULE=config.settings.{mode} python manage.py migrate'
    )


@task
def mkmg(mode='pre'):
    ''' 服务器端数据库 migration 操作 '''
    PYTHONPATH = f'/home/{env.user}/.pyenv/versions/{env.project}'
    with cd(env.remote_dir):
        remote(
            f'DJANGO_SETTINGS_MODULE=config.settings.{mode} {PYTHONPATH}/bin/python manage.py makemigrations'
        )
        remote(
            f'DJANGO_SETTINGS_MODULE=config.settings.{mode} {PYTHONPATH}/bin/python manage.py migrate'
        )


@task
def load(mode='dev'):
    ''' 导入开发数据 '''
    local(
        f'DJANGO_SETTINGS_MODULE=config.settings.{mode} python manage.py loaddata fixtures/auth.json'
    )
    local(
        f'DJANGO_SETTINGS_MODULE=config.settings.{mode} python manage.py loaddata fixtures/dump.json'
    )


@task
def dump(mode='dev'):
    ''' 导出开发数据 '''
    local(
        f'DJANGO_SETTINGS_MODULE=config.settings.{mode} python manage.py dumpdata --exclude auth.permission --exclude contenttypes -o fixtures/dump.json'
    )


@task
def require(mode='pre'):
    ''' 更新 requirements.txt 内的版本 '''
    local(
        f'pip-compile --output-file requirements.txt requirements/{mode}.txt --trusted-host mirrors.aliyun.com -v'
    )


@task
def wsgi(worker='egg:meinheld#gunicorn_worker', host='127.0.0.1', port=5000):
    ''' 启动 wsgi 服务 '''
    settings = 'DJANGO_SETTINGS_MODULE=config.settings.pre'
    local(
        f'{settings} gunicorn config.wsgi:application -k {worker} -w 4 -b {host}:{port}'
    )


@task
def fmt(path='.'):
    ''' 整理文件导入格式 '''
    try:
        import yapf
    except ImportError as e:
        print('如果出错请安装 yapf (pip install yapf)')
        raise e

    local(f'isort --recursive {path}')
    local(f'yapf -i -r {path} -vv --style=google')


@task
def unix():
    ''' 文本文件 windows 格式转 unix 格式 '''
    local('find . "*.txt" | xargs dos2unix')
    local('find . "*.md" | xargs dos2unix')
    local('find . "*.py" | xargs dos2unix')
    local('dos2unix Makefile')


@task
def stat():
    ''' 更新静态文件 '''
    with cd(env.remote_dir):
        remote('python manage.py collectstatic --noinput')


@task
def sync():
    ''' 同步服务器代码 '''
    project.rsync_project(remote_dir=env.remote_dir,
                          local_dir=env.local_dir,
                          exclude=env.excludes,
                          delete=True)


@task
def migr():
    ''' 合并数据文件 '''
    with cd(env.remote_dir):
        remote('''/root/.pyenv/versions/3.6.5/bin/python manage.py migrate''')


@task()
def rest():
    ''' 重启服务 '''
    # sudo('/etc/init.d/nginx reload')
    # sudo('/etc/init.d/supervisor reload')
    sudo('/usr/bin/supervisorctl restart ponder_server')


@task
def stop():
    ''' 停止服务 '''
    sudo('/usr/bin/supervisorctl stop ponder_server')


@task
def pack():
    ''' 文件打包 '''
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
