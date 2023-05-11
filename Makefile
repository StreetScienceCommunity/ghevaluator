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
	pip install --editable .
.PHONY: develop

build: init ## build
	python -m build
.PHONY: build

test: ## run the tests
	flake8 --exclude=.git,build --ignore=E501 .
	py.test --cov=enasearch tests/
.PHONY: test

upload: build ## upload on PyPi
	python -m twine upload dist/*
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
