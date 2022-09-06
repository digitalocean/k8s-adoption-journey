##########################################################
#                                                        #
#   Kubernetes Adoption Journey documentation Makefile   #
#                                                        #
##########################################################

PYTHON3_CMD         ?= python3
PIP3_CMD            ?= pip3
VIRTUALENV_CMD      ?= virtualenv
MKDOCS_CMD          ?= mkdocs

# if changing VENV_FOLDER, .gitignore must be changed as well
VENV_FOLDER               ?= .venv
PROJ_REQUIREMENTS_FILE    ?= requirements.txt
export DOCS_DIR           ?= docs
export SITE_DIR           ?= site
export SITE_URL           ?= https://k8s-adoption-journey.github.io

.ONESHELL:
ENV_PREFIX=$(shell $(PYTHON3_CMD) -c "if __import__('pathlib').Path('$(VENV_FOLDER)/bin/$(PIP3_CMD)').exists(): print('$(VENV_FOLDER)/bin/')")

.PHONY: create-venv
create-venv:
	@$(PIP3_CMD) install virtualenv
	@$(VIRTUALENV_CMD) $(VENV_FOLDER)

.PHONY: install
install: create-venv
	@$(ENV_PREFIX)$(PIP3_CMD) install -r $(PROJ_REQUIREMENTS_FILE)

# Pass arguments to mkdocs directly
# This way, you can run: 
#	- `make new` to create a new project
#	- `make build` to build a project
#	- `make serve` to serve a project static content locally
#	etc.
# Also, everything happens in a Python virtual env
.PHONY: Makefile
%: install Makefile
	@$(ENV_PREFIX)$(MKDOCS_CMD) $@

.PHONY: help
help: install
	@$(ENV_PREFIX)$(MKDOCS_CMD) --help

.PHONY: clean
clean:
	@echo "Cleaning up python venv ..."
	@rm -rf $(VENV_FOLDER)
	@echo "Cleaning up mkdocs site ..."
	@rm -rf $(SITE_DIR)
