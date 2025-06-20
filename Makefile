# Some constants
PROJECT_NAME:=kernel-auditor
INSTALL_PATH:=/usr/share/
SYSTEMD_SERVICE_PATH:=/etc/systemd/system/
PWD=$(shell pwd)

.PHONY: tests

define find.functions
     @awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "%-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)
endef

help: ## Returns command documentations
help:
	@echo 'The following commands can be used'
	@echo ''
	@$(find.functions)

del_syswide: ## Removes kernel_auditor from system
del_syswide:
	sudo systemctl disable --now $(PROJECT_NAME).service
	sudo rm -r $(INSTALL_PATH)$(PROJECT_NAME)
	sudo rm -r $(SYSTEMD_SERVICE_PATH)$(PROJECT_NAME).service

make_syswide: ## Make kernel_auditor as a system service
make_syswide:
	sudo cp -r $(PWD) $(INSTALL_PATH)
	sudo cp -r others/$(PROJECT_NAME).service $(SYSTEMD_SERVICE_PATH)
	sudo systemctl enable --now $(PROJECT_NAME).service

remake_syswide: ## Redo kernel_auditor as a system service (useful for updating)
remake_syswide:
	sudo systemctl stop $(PROJECT_NAME)
	sudo cp -r $(PWD) $(INSTALL_PATH)
	sudo cp -r others/$(PROJECT_NAME).service $(SYSTEMD_SERVICE_PATH)
	sudo systemctl start $(PROJECT_NAME)
	sudo systemctl daemon-reload

clean: ## Clean __pycache__ trash
clean:
	sudo find . -type d -name "__pycache__" -exec rm -rf {} +

run: ## Run the server as default web-app
run:
	sudo python3 main.py

stop: ## Stop the service
stop:
	sudo systemctl stop $(PROJECT_NAME)

tests: ## Do tests
tests:
	sudo sh -c "PYTHONPATH=. pytest"