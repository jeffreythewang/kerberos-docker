# GNU Make 4.1

SHELL = /usr/bin/env bash

TEST = "./test"
SCRIPT = "./script"

.PHONY: usage
usage:
	@echo "targets include: usage gen-conf pre-build build install test stop start clean"

.PHONY: gen-conf
gen-conf:
	@source $(SCRIPT)/build-python-env.sh; \
	$(SCRIPT)/get-env.sh; \
	$(SCRIPT)/generate_docker_compose.py


.PHONY: pre-build
pre-build: gen-conf
	@$(SCRIPT)/pre-build.sh

.PHONY: build
build: pre-build
	@$(SCRIPT)/create-network.sh
	@$(SCRIPT)/build.sh

.PHONY: create
create: build
	@$(SCRIPT)/create.sh

.PHONY: init
init: start
	@$(SCRIPT)/init.sh

.PHONY: install
install: create init

.PHONY: test
test:
	@cd $(TEST); ./test.bats

.PHONY: stop
stop:
	@$(SCRIPT)/stop.sh

.PHONY: start
start:
	@$(SCRIPT)/start.sh

.PHONY: clean
clean: stop
	@$(SCRIPT)/clean.sh
