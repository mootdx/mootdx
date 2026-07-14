.PHONY: help clean test test-network test-vipdoc build install lint

PYTHON ?= python
TDXDIR ?=

help:
	@echo "make test                 Run deterministic pytest suite"
	@echo "make test-network         Run live-network tests"
	@echo "make test-vipdoc TDXDIR=  Run against a local TDX root/vipdoc"
	@echo "make build                Build a wheel with pip"

clean:
	rm -rf build dist .pytest_cache .tox htmlcov
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	find . -type f -name '*.py[co]' -delete

install:
	$(PYTHON) -m pip install -e .

test:
	$(PYTHON) -m pytest

test-network:
	$(PYTHON) -m pytest -m network

test-vipdoc:
	test -n "$(TDXDIR)"
	MOOTDX_TDXDIR="$(TDXDIR)" $(PYTHON) -m pytest tests/integration

lint:
	$(PYTHON) -m compileall -q mootdx tests

build: clean
	$(PYTHON) -m pip wheel --no-deps --no-build-isolation --wheel-dir dist .
