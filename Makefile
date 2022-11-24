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
BRANCH := `git symbolic-ref --short -q HEAD`

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
	poetry run py.test tests -v

test-all: ## run tests on every Python version with tox
	tox

coverage: ## check code coverage quickly with the default Python
	coverage run --source mootdx -m pytest
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/mootdx.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ mootdx
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

release: dist ## package and upload a release
	poetry run twine upload dist/* --verbose

archive: clean
	git archive --format zip --output ../mootdx-master.zip master

dist: clean ## builds source and wheel package
	poetry run python setup.py sdist
	poetry run python setup.py bdist_wheel
	ls -lh dist

install: clean ## install the package to the active Python's site-packages
	python setup.py install

requirements:
	python -m pip install -r requirements.dev -r requirements.txt -r tests/requirements.txt

pull:
	git pull origin $(BRANCH) --tags
	git pull github $(BRANCH) --tags
	git pull gitee $(BRANCH) --tags

push: pull
	git push origin $(BRANCH) --tags
	git push github $(BRANCH) --tags
	git push gitee $(BRANCH) --tags

bestip:
	@poetry run python -m mootdx bestip -v

patch:
	poetry run bumpversion patch
	poetry run python setup.py sdist
	poetry run python setup.py bdist_wheel
	poetry run twine upload dist/* --verbose

