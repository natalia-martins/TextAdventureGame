ifneq ("$(wildcard .env)","")
	include .env
	export
endif

.PHONY: run
run: ## Run the project.
	poetry run python -m src.app

.PHONY: install
install: ## Install Python package dependencies.
	python -m pip install --upgrade pip setuptools wheel poetry
	poetry lock
	poetry install --no-root

.PHONY: export-requirements
export-requirements: ## Export poetry managed packages to a requirements.txt (needed by Vercel).
	poetry export -f requirements.txt --output requirements.txt --without-hashes

.PHONY: patch
patch: ## Bump project version to next patch (bugfix release).
	poetry version patch

.PHONY: minor
minor: ## Bump project version to next minor (feature release).
	poetry version minor

.PHONY: clean
clean: ## Clean project's temporary files.
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.log' -exec rm -f {} +

.DEFAULT_GOAL := help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sed 's/Makefile://g' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'