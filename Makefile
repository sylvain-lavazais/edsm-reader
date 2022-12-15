PWD=$(shell pwd)
.DEFAULT_GOAL := help

help: ## Print this message
	@echo  "$$(grep -hE '^\S+:.*##' $(MAKEFILE_LIST) | sort | sed -e 's/:.*##\s*/:/' -e 's/^\(.\+\):\(.*\)/\x1b[36m\1\x1b[m:\2/' | column -c2 -t -s :)"
.PHONY: help

.revolve-dep:
	@python -m pip install -r requirements.txt
.PHONY: .revolve-dep

db-local-apply: .revolve-dep ## Apply database migrations scripts
	@python -m yoyo --config yoyo-local.ini apply
.PHONY: db-local-apply

db-local-reset: ## Fully reset local db (use Docker)
	@docker compose -f docker/docker-compose.yml down -v || true
	@docker volume rm astraeus-db || true
	@docker volume create astraeus-db
	@docker compose -f docker/docker-compose.yml up -d
	@sleep 5
	@make db-local-apply
.PHONY: db-local-reset

install: .revolve-dep ## Run locally the application
	@rm -rf build dist
	@python -m build
	@pip install --force-reinstall --editable .
.PHONY: install

build: .revolve-dep ## Build the application
	@python -m build
