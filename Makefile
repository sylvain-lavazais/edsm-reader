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
	@docker volume rm edsm-mirror-db || true
	@docker volume create edsm-mirror-db
	@docker compose -f docker/docker-compose.yml up -d
	@sleep 5
	@make db-local-apply
.PHONY: db-local-reset

edsm-full-import-system: ## Get a full system import from EDSM
	@echo "Getting the full system from EDSM, this task will..."
	@echo "1. Download the full systems file (2Gb space)"
	@echo "2. Uncompress it (>10Gb space)"
	@echo "3. Rework the file to be used by the application (as a JSON lines)"
	@echo "Are you sure? [y/N] " && read ans && [ $${ans:-N} = y ]
	@echo "=> Downloading file..."
	@curl -L -O -C - https://www.edsm.net/dump/systemsWithCoordinates.json.gz
	@echo "=> Uncompress file..."
	@gunzip systemsWithCoordinates.json.gz
	@echo "=> Rework file..."
	@sed -e 's/"},/"}/g' -i systemsWithCoordinates.json
	@sed -i '1d' systemsWithCoordinates.json
	@sed -i '$d' systemsWithCoordinates.json
	@echo "=> Task completed !"
.PHONY: edsm-full-import-system

install: .revolve-dep ## Run locally the application
	@rm -rf build dist
	@python setup.py bdist_wheel
	@pip install --force-reinstall dist/*.whl
.PHONY: install
