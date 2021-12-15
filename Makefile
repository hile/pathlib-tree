
ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
MODULE := pathlib_tree
VERSION := $(shell awk '/^__version__/ {print $$3}' ${MODULE}/__init__.py)
SPHINX_FLAGS := -b html ./docs public
SPHINX_WEBSITE_FLAGS := --port 8100 --host localhost --open-browser --watch ${MODULE}

all: lint test

clean:
	@rm -rf build dist .DS_Store .pytest_cache .cache .eggs .tox .coverage coverage.xml htmlcov public
	@find . -name '__pycache__' -print0 | xargs -0 rm -rf
	@find . -name '*.egg-info' -print0 | xargs -0 rm -rf
	@find . -name '.DS_Store' -print0 | xargs -0 rm -rf
	@find . -name '*.pyc' -print0 | xargs -0 rm -rf

build:
	python setup.py build

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

upload: clean
	python3 setup.py sdist
	twine upload dist/*

tag-release:
	git tag --annotate ${VERSION} --message "Publish release ${VERSION}"
	git push origin ${VERSION}

.PHONY: all test
