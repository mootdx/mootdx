# -*- coding: utf-8 -*-
# httperf --hog --server=127.0.0.1 --port=8000 --uri=/api/version/ --timeout=10 --num-conns=200 --rate=5
import os

from fabric.api import put as _put
from fabric.api import run as _run
from fabric.api import cd, env, local, task
from fabric.context_managers import prefix
from fabric.contrib import project

HERE = os.path.abspath(os.path.dirname(__file__))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

env.hosts = ['root@103.200.97.164']

env.excludes = (
    "*.pyc", "*.db", ".DS_Store", ".coverage", ".git", ".hg", ".tox", ".idea/", '__pycache__',
    'assets/', 'runtime/', 'node_modules', '*.ipynb', 'init', '*.rdb', 'scripts/data', 'tests')

env.remote_dir = '/home/site/browser'
env.local_dir = '.'


@task
def pv():
    from glob import glob
    local('''pip freeze > freeze.txt''')
    
    for rs in glob('requirements/*.txt'):
        pv = dict([(x.strip().split('==')[0].lower(), x.strip().lower()) for x in open('freeze.txt')])
        rq = [x.strip().replace('_','-') for x in open(rs)]

        for k,v in enumerate(rq):
            v = v.strip().replace('_','-')
            
            if pv.get(v):
                rq[k] = pv.get(v)
        
        with open(rs,'w') as fs:
            fs.writelines(map(lambda x:x.strip()+'\n', rq))
            print('[+] ' + rs)
        

    local('''rm -rf freeze.txt''')

@task(alias='cw')
def crawl():
    ''' 采集数据 '''
    local('''scrapy crawl article -a id=1 -a do_action=yes''')

@task
def cov():
    ''' 测试代码覆盖率 '''
    local('python manage.py jenkins --settings=config.settings.test --enable-coverage  --coverage-format html -v2')
    local('open reports/coverage/index.html')


@task(alias='l')
def lift():
    '''
    一键启动开发环境的各种服务
    '''
    local('honcho start')


@task
def start(conf='local'):
    '''
    启动开发服务器
    '''
    local('python manage.py runserver --settings=config.settings.%s' % conf)


@task
def setup(conf=None):
    '''安装项目所需的包'''
    envs = '' if conf is None else '/' + conf
    local('pip install -r requirements%s.txt' % envs)

    if not os.path.exists('.env'):
        local('cp deploy/config/env.server .env')

    conf = 'local' if conf is None else conf
    mm(conf=conf)
    local('python manage.py createsuperuser --settings=config.settings.%s' % conf)
    # local('python manage.py runserver --settings=config.settings.%s' % conf)


def venv():
    with prefix('source /usr/local/bin/virtualenvwrapper.sh'):
        _run('mkvirtualenv browser')

    with prefix('pyenv shell drf3'), cd(env.remote_dir):
        _run('pip install -r requirements_dev.txt')


def supervisor():
    _put('config/supervisor.conf', '/etc/supervisor/conf.d/browser.conf')


def schedule(action='check'):
    local('python schedule.py %s' % action)
    # with prefix('pyenv shell drf3'), cd(env.remote_dir):
    #     local('python schedule.py %s' % action)


@task
def d2u():
    '''dos 文件格式转 unix 格式'''
    local('find . -name "*.html" -exec dos2unix {} \;')
    local('find . -name "*.py" -exec dos2unix {} \;')
    local('find . -name "*.css" -exec dos2unix {} \;')
    local('find . -name "*.js" -exec dos2unix {} \;')


@task
def script(script=None):
    '''运行自定义脚本'''
    local('python manage.py runscript %s --traceback' % script)


@task
def test(v='v1'):
    ''' 运行测试 '''
    local('''python manage.py test --settings=config.settings.test --traceback -%s''' % v)


def static():
    local('python manage.py collectstatic --dry-run -c --noinput')
    # with prefix('pyenv shell drf3'), cd(env.remote_dir):
    #     _run('python manage.py collectstatic --dry-run -c --noinput')


def push():
    local_dir = os.getcwd() + os.sep
    return project.rsync_project(remote_dir=env.remote_dir, local_dir=local_dir, exclude=env.excludes, delete=True)


def pull():
    with prefix('pyenv shell drf3'), cd(env.remote_dir):
        _run('git pull')
        _run('pip install -r requirements.txt')

    migrate()

    _run('/usr/bin/supervisorctl reØ browser')


def migrate():
    with prefix('pyenv shell drf3'), cd(env.remote_dir):
        _run('''DJANGO_SETTINGS_MODULE='config.settings.local' python manage.py migrate''')


def restart():
    with prefix('pyenv shell drf3'), cd(env.remote_dir):
        _run('/usr/bin/supervisorctl restart browser')


@task
def mm(conf='local'):
    ''' 执行数据库变更 '''
    local('python manage.py makemigrations --settings=config.settings.%s' % conf)
    local('python manage.py migrate --settings=config.settings.%s' % conf)


@task
def ur():
    '''上传项目文件 & 重启服务'''
    push()
    restart()


@task
def um():
    '''上传项目文件 & 合并数据库'''
    push()
    migrate()


@task
def umr():
    '''上传项目文件 & 合并数据库 & 重启服务'''
    push()
    migrate()
    restart()


def pyc():
    ''' 编译 `py` 文件成 `pyc` '''
    local('''python -m compileall .''')


@task(alias='cl')
def clean():
    ''' 清理项目运行缓存 '''
    local('find . -name "*.sql" | xargs rm -rf')
    local('find . -name "*.pyc" | xargs rm -rf')
    local('find . -name "*.bak" | xargs rm -rf')
    local('find . -name "*.log" | xargs rm -rf')
    local('find . -name ".DS_Store" | xargs rm -rf')


def clean_static(migrate=None):
    local('rm -rf assets/static/*')


def clean_migrate():
    local('''find service -path '*migrations/[0-9]*.py' | xargs rm -rf''')
    local('''rm -rf db.sqlite3''')


@task(alias='dc')
def distclean():
    ''' 彻底清理项目 别名 dc
    '''
    clean()
    clean_static()
    clean_migrate()


@task
def pack(path=None):
    ''' 打包项目 path 参数为存放路径'''
    import datetime
    today = datetime.date.today()

    local('tar zcfv %s/%s.tgz '
          '--exclude=.git '
          '--exclude=.tox '
          '--exclude=.svn '
          '--exclude=.env '
          '--exclude=.idea '
          '--exclude=*.tgz '
          '--exclude=*.pyc '
          '--exclude=.cache '
          '--exclude=.vagrant '
          '--exclude=tests '
          '--exclude=assets/media/**/* '
          '--exclude=assets/static/**/* '
          '--exclude=manual '
          '--exclude=storage '
          '--exclude=database '
          '--exclude=.DS_Store '
          '--exclude=.phpintel '
          '--exclude=.template '
          '--exclude=db.sqlite3 '
          '--exclude=Vagrantfile .' % (path, today))


@task(alias='c')
def check():
    '''检查整个项目是否潜在的问题'''
    local('python manage.py check')
