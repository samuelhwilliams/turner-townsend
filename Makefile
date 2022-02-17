VERSION := $(shell cat version.txt)

.PHONY: build
build:
	docker build -t turner-townsend/${VERSION} --target production .
	docker build -t turner-townsend/${VERSION}.test --target test .

.PHONY: test
test: build
	docker run -t turner-townsend/${VERSION}.test

.PHONY: run
run:
	docker run -i turner-townsend/${VERSION}
