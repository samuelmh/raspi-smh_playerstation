#
# Author: Samuel M.H. <samuel.mh@gmail.com>
# Description:
#    Make-based utility to manage the project.
#    Idea taken from:
#     - http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html

#
### PRECONFIG
#

PYTHON_VERSION := 3.6

#
### PATHS
#
LIBRARY = smh_playerstation


#Don't touch
PATH_PROJECT = $(shell dirname $(abspath $(lastword $(MAKEFILE_LIST))))
PATH_VENV = $(PATH_PROJECT)/venv
PATH_LIBRARY = $(PATH_PROJECT)/$(LIBRARY)
PATH_DATA = $(PATH_PROJECT)/data
PATH_CONFIG = $(PATH_LIBRARY)/config


#
### Autodocumenting thing, don't touch
#
.PHONY: help

.DEFAULT_GOAL := help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'



#
### Install the project
#
install: ## Create a development environment (virtualenv).
	@echo "Create the environment in "$(PATH_PROJECT)
	@virtualenv -p python$(PYTHON_VERSION) $(PATH_VENV)
	@echo "Install requirements"
	$(PATH_VENV)'/bin/pip' install -r $(PATH_PROJECT)'/deploy/requirements.txt'
	@echo "Create symbolic links"
	# Link to project
	@ln -s $(PATH_PROJECT) $(PATH_VENV)'/'
	# Link code to project library so it is in the PYTHONPATH
	@ln -s $(PATH_LIBRARY) $(PATH_VENV)'/lib/python$(PYTHON_VERSION)/site-packages/'
	# CONFIGURATION
	# Logging
	@ cp $(PATH_PROJECT)'/deploy/logging.conf' $(PATH_CONFIG)
	# Local configuration
	@echo "PATH_PROJECT='$(PATH_PROJECT)/'">$(PATH_CONFIG)'/config_local.py'
	@echo "PATH_DATA='$(PATH_DATA)/'">>$(PATH_CONFIG)'/config_local.py'
	@echo "PATH_CONFIG='$(PATH_CONFIG)/'">>$(PATH_CONFIG)'/config_local.py'
	# Data directory
	@mkdir -p -- $(PATH_DATA)
	@echo "Done"



#
### Run things
#

run-webserver: ## Start the HTTP microservice (development).
	$(PATH_VENV)'/bin/python' -m smh_playerstation.webserver.webserver


#
### Code checks
#

# check-pep8:  ##Run pep8 on all python files
# 	@find smh_pi_audiostation/ -name "*.py"|while read FNAME; do pep8 "$$FNAME"; done
#
# check-pyflakes: ##Run pyflakes on all python files
# 	@find smh_pi_audiostation/ -name "*.py"|while read FNAME; do pyflakes "$$FNAME"; done
#
# check-pylint: ##Run pylint on all python files
# 	@find smh_pi_audiostation/ -name "*.py"|while read FNAME; do pylint "$$FNAME"; done



#
### Tests
#

# test-all: ## Run all the tests.
# 	@echo "Running all tests"
# 	@python -m unittest test.whatever
