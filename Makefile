# Sphinx variable
SPHINXOPTS    =
SPHINXBUILD   = python -msphinx
SPHINXPROJ    = ghevaluate
SOURCEDIR     = src/docs
BUILDDIR      = tmp


# Commands
default: help

init: ## install the requirements
	pip install -r requirements.txt
.PHONY: init

develop: init ## setup develop mode
	python setup.py develop
.PHONY: develop

test: ## run the tests
	flake8 --exclude=.git,build --ignore=E501 .
	py.test --cov=enasearch tests/
.PHONY: test

upload: ## upload on PyPi
	python setup.py register -r pypi
	python setup.py sdist upload -r pypi
.PHONY: upload

doc: ## generate HTML documentation
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	rm -rf docs
	mv "$(BUILDDIR)/html" docs
	rm -rf docs/_sources
.PHONY: doc

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.PHONY: help
