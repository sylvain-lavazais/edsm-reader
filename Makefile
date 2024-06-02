
##  --------
##@ Database
##  --------

db-local-apply: ## Apply database migrations scripts
	@echo "===> $@ <==="
	@python -m yoyo --config yoyo-local.ini apply
.PHONY: db-local-apply

db-local-reset: ## Fully reset local db (use Docker)
	@echo "===> $@ <==="
	@docker compose -f docker/docker-compose.yml down -v || true
	@docker volume rm astraeus-db || true
	@docker volume create astraeus-db
	@docker compose -f docker/docker-compose.yml up -d
	@sleep 5
	@make db-local-apply
.PHONY: db-local-reset

##  -------
##@ Install
##  -------

install: ## Install locally the application
	@echo "===> $@ <==="
	@rm -rf build dist
	@python -m build
	@pip install --force-reinstall --editable .
.PHONY: install

build: ## Build the application
	@echo "===> $@ <==="
	@python -m build

##  ----
##@ Run
##  ----

run: ## Run locally the application
	@echo "===> $@ <==="
	@python -m edsm-reader
.PHONY: run

##  ----
##@ Misc
##  ----

.DEFAULT_GOAL := help
APPLICATION_TITLE := Astraeus - edsm-reader \n ================
.PHONY: help
# See https://www.thapaliya.com/en/writings/well-documented-makefiles/
help: ## Display this help
	@awk 'BEGIN {FS = ":.* ##"; printf "\n\033[32;1m ${APPLICATION_TITLE}\033[0m\n\n\033[1mUsage:\033[0m\n  \033[31mmake \033[36m<option>\033[0m\n"} /^[%a-zA-Z_-]+:.* ## / { printf "  \033[33m%-25s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' ${MAKEFILE_LIST}

##@
