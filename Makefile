#
# Install the scrips, configs and python modules
#

all: lint test

clean:
	@rm -rf build dist .DS_Store .cache .eggs .tox coverage
	@find . -name '*.egg-info' -print0|xargs -0 rm -rf
	@find . -name '*.pyc' -print0|xargs -0 rm -rf

build:
	python setup.py build

lint:
	pylint systematic_files tests setup.py
	flake8 | sort

test:
	tox

upload: clean
	python3 setup.py sdist bdist_wheel
	twine upload dist/*

.PHONY: all test
