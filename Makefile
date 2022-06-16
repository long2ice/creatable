checkfiles = creatable/ tests/ conftest.py
py_warn = PYTHONDEVMODE=1

up:
	@poetry update

deps:
	@poetry install -E mysql -E postgres

style: deps
	@isort -src $(checkfiles)
	@black $(checkfiles)

check: deps
	@black --check $(black_opts) $(checkfiles) || (echo "Please run 'make style' to auto-fix style issues" && false)
	@pflake8 $(checkfiles)
	@mypy $(checkfiles)

test: deps
	$(py_warn) pytest

build: deps
	@poetry build

ci: check test
