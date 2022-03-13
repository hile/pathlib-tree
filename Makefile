
ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
MODULE := pathlib_tree
VERSION := $(shell awk '/^version =/ {print $$3}' pyproject.toml)
SPHINX_FLAGS := -b html ./docs public
SPHINX_WEBSITE_FLAGS := --port 8100 --host localhost --open-browser --watch ${MODULE}

all: lint test

clean:
	@rm -rf build dist .DS_Store .pytest_cache .cache .eggs .coverage coverage.xml public
	@find . -name '.DS_Store' -print0 | xargs -0r rm -rf
	@find . -name '__pycache__' -print0 | xargs -0r rm -rf
	@find . -name '*.egg-info' -print0 | xargs -0r rm -rf
	@find . -name '*.pyc' -print0 | xargs -0r rm -rf
	@find . -name '*.tox' -print0 | xargs -0r rm -rf
	@find . -name 'htmlcov' -print0 | xargs -0r rm -rf

build:
	poetry build

doc-devel:
	export PYTHONPATH=${ROOT_DIR}
	vaskitsa documentation generate ${ROOT_DIR}
	sphinx-autobuild ${SPHINX_WEBSITE_FLAGS} ${SPHINX_FLAGS}

doc:
	export PYTHONPATH=${ROOT_DIR}
	vaskitsa documentation generate ${ROOT_DIR}
	sphinx-build ${SPHINX_FLAGS}

lint:
	tox -e lint

test:
	tox -e unittest

publish: clean build
	poetry publish

tag-release:
	git tag --annotate ${VERSION} --message "Publish release ${VERSION}"
	git push origin ${VERSION}

.PHONY: all test
