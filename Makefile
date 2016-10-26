.PHONY: all

all: virtualenv install

virtualenv:
	virtualenv -p python3.5 venv/
	./venv/bin/python -m pip install -r requirements
install:
	./venv/bin/python setup.py install

docker:
	docker run --rm -v $(shell pwd):/worker -w /worker iron/python:3-dev pip install -t packages -r requirements
	docker build -t kraken:$(shell cat kraken/__version__.py | cut -d"=" -f2| sed 's/\"//g'|sed 's/\ //g') .
	docker tag kraken:$(shell cat kraken/__version__.py | cut -d"=" -f2| sed 's/\"//g'|sed 's/\ //g') kraken:latest

docker-push:
	docker tag kraken:latest m4ucorp/plataformas-kraken:latest
	docker push m4ucorp/plataformas-kraken

test:
	docker run --rm -v $(shell pwd):/worker -e "PYTHONPATH=/worker/packages" -w /worker iron/python:3 python3 -m kraken

clean:
	sudo rm -rf venv/*
	sudo rm -rf dist build
	sudo rm -rf kraken.egg-info
	find . -name __pycache__ | xargs -I {} sudo rm -rf {}
	find . -name *.pyc |xargs -I {} sudo rm -rf {}
	sudo rm -rf packages

