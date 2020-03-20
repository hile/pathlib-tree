
MODULE := systematic_files
VERSION := $(shell awk '/^__version__/ {print $$3}' ${MODULE}/version.py)

all: lint test

clean:
	@rm -rf build dist .DS_Store .pytest_cache .cache .eggs .coverage .tox coverage
	@find . -name '__pycache__' -print0 | xargs -0 rm -rf
	@find . -name '*.egg-info' -print0 | xargs -0 rm -rf
	@find . -name '*.pyc' -print0 | xargs -0 rm -rf

build:
	python setup.py build

lint:
	pylint ${MODULE} tests setup.py
	flake8 | sort

test:
	tox

upload: clean
	python3 setup.py sdist bdist_wheel
	twine upload dist/*

tag-release:
	git tag -a ${VERSION} -m "Publish release ${VERSION}"
	git push origin ${VERSION}

.PHONY: all test
