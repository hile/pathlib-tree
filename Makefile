ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
MODULE := $(shell basename ${ROOT_DIR} | tr - _)
VERSION := $(shell awk '/^version =/ {print $$3}' pyproject.toml)

VENV_DIR := ${HOME}/.venv/${MODULE}
VENV_BIN := ${VENV_DIR}/bin
PIP := ${VENV_DIR}/bin/pip

SPHINX_FLAGS := -b html ./docs public
SPHINX_WEBSITE_FLAGS := --port 8100 --host localhost --open-browser --watch ${MODULE}

all: unittest coverage lint

${VENV_BIN}:
	python3 -m venv ${VENV_DIR}
	. ${VENV_BIN}/activate; pip install poetry
	. ${VENV_BIN}/activate; poetry install
virtualenv: ${VENV_BIN}

clean:
	@rm -rf build dist .DS_Store .pytest_cache .cache .eggs .coverage coverage.xml public
	@find . -name '__pycache__' -print0 | xargs -0r rm -rf
	@find . -name '*.egg-info' -print0 | xargs -0r rm -rf
	@find . -name '*.pyc' -print0 | xargs -0r rm -rf
	@find . -name '*.tox' -print0 | xargs -0r rm -rf
	@find . -name 'htmlcov' -print0 | xargs -0r rm -rf

build: virtualenv
	source ${VENV_BIN}/activate; poetry build

doc-devel: virtualenv
	export PYTHONPATH=${ROOT_DIR}
	source ${VENV_BIN}/activate; vaskitsa documentation generate ${ROOT_DIR}
	source ${VENV_BIN}/activate; sphinx-autobuild ${SPHINX_WEBSITE_FLAGS} ${SPHINX_FLAGS}

doc: virtualenv
	export PYTHONPATH=${ROOT_DIR}
	source ${VENV_BIN}/activate; vaskitsa documentation generate ${ROOT_DIR}
	source ${VENV_BIN}/activate; sphinx-build ${SPHINX_FLAGS}

unittest: virtualenv
	source ${VENV_BIN}/activate && poetry run coverage run --source "${MODULE}" --module pytest

coverage: virtualenv
	source ${VENV_BIN}/activate && poetry run coverage html
	source ${VENV_BIN}/activate && poetry run coverage report

lint: virtualenv
	source ${VENV_BIN}/activate && poetry run flake8
	source ${VENV_BIN}/activate && poetry run pycodestyle "${MODULE}" tests
	source ${VENV_BIN}/activate && poetry run pylint "${MODULE}" tests

publish: virtualenv clean build
	source ${VENV_BIN}/activate && poetry publish

tag-release:
	git tag --annotate ${VERSION} --message "Publish release ${VERSION}"
	git push origin ${VERSION}

.PHONY: all test
