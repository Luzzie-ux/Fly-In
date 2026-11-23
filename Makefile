
PKG_MANAGER = uv
INTERPRETER = python3
DEBUGGER = pdb
RM_DIRS = __pycache__ .mypy_cache
LINTER = flake8 .
TY = mypy .
TYFLAGS = --warn-return-any \
		  --warn-unusued-ignores \
		  --ignore-missing-imports \
		  --disallow-untyped-defs \
		  --check-untyped-defs
install:
	$(PKG_MANAGER) sync
	$()
run:
	$(INTERPRETER) -m fly-in
debug:
	$(DEBUGGER)
clean:
	@rm -rf $(RM_DIRS)
lint:
	$(LINTER)
	$(TY) $(TYFLAGS)

lint-strict: TYFLAGS = --strict
lint-strict: lint

