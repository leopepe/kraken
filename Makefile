PHONY: all

virtualenv:
	virtualenv -p python3.4 venv/
	./venv/bin/python -m pip install -r requirements
install:
	./venv/bin/python setup.py install

docker:
	docker run --rm -v $(shell pwd):/worker -w /worker iron/python:3-dev pip install -t packages -r requirements
	docker build -t kraken:$(shell cat kraken/__version__.py | cut -d"=" -f2| sed 's/\"//g'|sed 's/\ //g') .

test:
	docker run --rm -v $(shell pwd):/worker -e "PYTHONPATH=/worker/packages" -w /worker iron/python:3 python3 -m kraken

clean:
	rm -rf venv/*
	rm -rf dist build
	rm -rf kraken.egg-info
	find . -name __pycache__ | xargs -I {} rm -rf {}
	find . -name *.pyc |xargs -I {} rm -rf {}
	rm -rf packages

all: virtualenv install
