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
VERSION := 0.10.1

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts


unix:
	find . "*.txt" | xargs dos2unix
	find . "*.md" | xargs dos2unix
	find . "*.py" | xargs dos2unix
	dos2unix Makefile

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*.~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

lint: ## check style with flake8
	flake8 --max-line-length=200

cov: clean-test
	poetry run py.test -v --cov=mootdx --cov-report=html

fmt:
	black -l 120 -t py36 -t py37 -t py38 -t py39 -t py310 .

test: ## run tests quickly with the default Python
	# unset https_proxy http_proxy all_proxy
	# poetry run py.test tests -v
	poetry run pytest tests -v

coverage: ## check code coverage quickly with the default Python
	poetry run coverage report -m
	poetry run coverage html
	$(BROWSER) htmlcov/index.html

test-all: ## run tests on every Python version with tox
	tox

docs: ## generate Mkdocs HTML documentation, including API docs
	poetry run mkdocs serve

release: test dist history ## package and upload a release
	poetry run twine upload dist/* --verbose

archive: clean
	git archive --format zip --output ../mootdx-master.zip master

dist: clean ## builds source and wheel package
	#poetry run python setup.py sdist
	#poetry run python setup.py bdist_wheel
	@poetry build -vv
	ls -lh dist

install: clean ## install the package to the active Python's site-packages
	python setup.py install

requirements:
	python -m pip install -r requirements.dev -r requirements.txt -r tests/requirements.txt

pull:
	git pull origin `git symbolic-ref --short -q HEAD` --tags
	git pull github `git symbolic-ref --short -q HEAD` --tags
	git pull gitee `git symbolic-ref --short -q HEAD` --tags

push: pull
	git push origin `git symbolic-ref --short -q HEAD` --tags
	git push github `git symbolic-ref --short -q HEAD` --tags
	git push gitee `git symbolic-ref --short -q HEAD` --tags

bestip:
	@poetry run python -m mootdx bestip -v

patch:
	poetry run bumpversion patch
	poetry run python setup.py sdist
	poetry run python setup.py bdist_wheel
	poetry run twine upload dist/* --verbose

history: ## show commit incremental changelog
	#pip install commitizen -i https://pypi.tuna.tsinghua.edu.cn/simple
	cz bump --dry-run --increment patch

publish: clean ## package and upload a release
	poetry publish --build --username="$(USERNAME)" --password="$(PASSWORD)" --skip-existing --dry-run

docker: ## build docker image of CI/CD.
	docker build . -t mootdx:$(VERSION)
