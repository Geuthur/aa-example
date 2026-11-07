# Makefile fragment for development tasks

# Install the app as an editable package in the current Python environment
PHONY: dev-install
dev-install: check-python-venv
	@echo "Installing $(GENERAL__APPNAME) as editable package…"
	@pip install -e $(DEVELOPMENT__BASE_DIR)

# Uninstall the app from the current Python environment
PHONY: dev-uninstall
dev-uninstall: check-python-venv
	@echo "Uninstalling $(GENERAL__APPNAME)…"
	@pip uninstall -y $(GENERAL__APPNAME)

# Create a new app from this template: rename the package, the repository name
# and the verbose name in every text file and path (see scripts/init_app.py --help)
.PHONY: init-app
init-app:
	@if [ -z "$(NAME)" ] || [ -z "$(APPNAME)" ] || [ -z "$(VERBOSE)" ]; then \
		echo "Usage: make init-app NAME=<package> APPNAME=aa-<name> VERBOSE=\"AA <Name>\" [INIT_ARGS=\"--drop-migrations --drop-template-override --dry-run\"]"; \
		exit 1; \
	fi
	@python3 scripts/init_app.py --package "$(NAME)" --app-name "$(APPNAME)" --verbose-name "$(VERBOSE)" $(INIT_ARGS)

.PHONY: help
help::
	@echo "  $(TEXT_UNDERLINE)Development:$(TEXT_UNDERLINE_END)"
	@echo "    dev-install                 Install the app as editable package"
	@echo "    dev-uninstall               Uninstall the app"
	@echo "    init-app                    Create a new app from this template (NAME, APPNAME, VERBOSE)"
	@echo ""
