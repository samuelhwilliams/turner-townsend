VERSION := $(shell cat version.txt)

.PHONY: venv
venv:
	python3.10 -m venv venv
	./venv/bin/pip install -r requirements-test.txt

.PHONY: build
build:
	docker build -t turner-townsend/${VERSION} --target production .
	docker build -t turner-townsend/${VERSION}.test --target test .

.PHONY: test
test: build
	docker run -t turner-townsend/${VERSION}.test

.PHONY: run-local
run-local: venv
	./venv/bin/python main.py

.PHONY: run
run:
	docker run -i turner-townsend/${VERSION}