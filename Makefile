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
