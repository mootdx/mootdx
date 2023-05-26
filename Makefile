.PHONY: clean clean-test clean-pyc clean-build docs help
.DEFAULT_GOAL := help
define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"
VERSION := 0.10.4

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test # remove all build, test, coverage and Python artifacts


unix:
	find . "*.txt" | xargs dos2unix
	find . "*.md" | xargs dos2unix
	find . "*.py" | xargs dos2unix
	dos2unix Makefile

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	rm -fr .temp/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*.~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

lint:
	flake8 --max-line-length=200

cov: clean-test
	poetry run py.test -v --cov=mootdx --cov-report=html

fmt:
	black -l 120 -t py36 -t py37 -t py38 -t py39 -t py310 .

test: # run tests quickly with the default Python
	@poetry run pytest tests

test-all:
	tox

docs:
	poetry run mkdocs serve

archive: clean
	git archive --format zip --output ../mootdx-master.zip master

package: clean ## 编译并打包
	#poetry run python setup.py sdist
	#poetry run python setup.py bdist_wheel
	@poetry build -vv
	ls -lh dist

cleanup: ## 清理开发环境
	poetry env remove 3.9

prepare: clean ## 准备开发环境
	git config user.email ibopo@126.com
	git config pull.rebase false
	git config user.name bopo
	poetry install --sync


#pull:
#	git pull origin `git symbolic-ref --short -q HEAD` --tags
#	git pull github `git symbolic-ref --short -q HEAD` --tags
#	git pull gitee `git symbolic-ref --short -q HEAD` --tags
#
#push: pull
#	git push origin `git symbolic-ref --short -q HEAD` --tags
#	git push github `git symbolic-ref --short -q HEAD` --tags
#	git push gitee `git symbolic-ref --short -q HEAD` --tags

bestip:
	@poetry run python -m mootdx bestip -v

#patch:
#	poetry run bumpversion patch
#	poetry run python setup.py sdist
#	poetry run python setup.py bdist_wheel
#	poetry run twine upload dist/* --verbose


history: ## 显示增量修改日志
	# https://commitizen-tools.github.io/commitizen/
	#pip install commitizen -i https://pypi.tuna.tsinghua.edu.cn/simple
	cz changelog --incremental --dry-run

publish: clean ## 打包并发布
	#cz bump --dry-run --increment patch
	#cz bump --yes -ch -cc --increment patch --dry-run
	poetry publish --build --skip-existing --dry-run

docker: # build docker image of CI/CD.
	mkdir -p .temp
	poetry export --without-hashes --with test -E all -o .temp/requirements.txt
	docker build . -t mootdx:build
	docker-squash mootdx:build -t mootdx:squash

release: ## 发布版本并生成修改日志.
	# https://commitizen-tools.github.io/commitizen/
	# https://keepachangelog.com/zh-CN/
	#cz bump --dry-run --yes -ch -cc --increment {MAJOR,MINOR,PATCH}
	cz bump --yes -ch -cc --increment patch --dry-run
