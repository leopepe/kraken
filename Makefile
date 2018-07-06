.PHONY: all
ORG?=leopepe

all: config-virtualenv install

config-virtualenv:
	virtualenv -p python3.5 venv/
	./venv/bin/python -m pip install -r requirements
install: config-virtualenv
	./venv/bin/python setup.py install

docker-build:
	docker run --rm -v $(shell pwd):/worker -w /worker iron/python:3-dev pip install -t packages -r requirements
	docker build -t kraken:$(shell cat kraken/__version__.py | cut -d"=" -f2| sed 's/\"//g'|sed 's/\ //g') .
	docker tag kraken:$(shell cat kraken/__version__.py | cut -d"=" -f2| sed 's/\"//g'|sed 's/\ //g') kraken:latest

docker-push: docker-build
	docker tag kraken:latest ${ORG}/kraken:latest
	docker push ${ORG}/kraken

test:
	docker run --rm -v $(shell pwd):/worker -e "PYTHONPATH=/worker/packages" -w /worker iron/python:3 python3 -m kraken

clean:
	sudo rm -rf venv/*
	sudo rm -rf dist build
	sudo rm -rf kraken.egg-info
	find . -name __pycache__ | xargs -I {} sudo rm -rf {}
	find . -name *.pyc |xargs -I {} sudo rm -rf {}
	sudo rm -rf packages

