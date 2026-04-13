.PHONY: install test lint clean html serve lint-tests lint-all format check-type pylint-report

# Default target
.DEFAULT_GOAL := test

# Variables
PYTHON := python3
PYTEST := pytest
PYLINT := pylint
SPHINX_APIDOC := sphinx-apidoc
SPHINX_BUILD := sphinx-build
DOCS_DIR := docs
DOCS_BUILD := $(DOCS_DIR)/_build
DOCS_HTML := $(DOCS_BUILD)/html
SRC_DIR := wauth
TEST_DIR := test

# ─── Installation ───────────────────────────────────────────────

install:
	@echo "Installing project with development dependencies..."
	pip install -e ".[dev,docs]"

install-prod:
	@echo "Installing production dependencies only..."
	pip install -e .

# ─── Testing ────────────────────────────────────────────────────

test:
	@echo "Running tests with coverage..."
	$(PYTEST) $(TEST_DIR)/ -v --cov=$(SRC_DIR) --cov-report=term-missing --cov-report=html

test-quick:
	@echo "Running tests (no coverage)..."
	$(PYTEST) $(TEST_DIR)/ -v --tb=short

# ─── Linting ────────────────────────────────────────────────────

lint:
	@echo "Running Pylint on source code..."
	$(PYLINT) $(SRC_DIR)/ \
		--disable=import-error,no-member,no-name-in-module \
		--output-format=text \
		--fail-under=9.5

lint-tests:
	@echo "Running Pylint on test files..."
	$(PYLINT) $(TEST_DIR)/ \
		--disable=import-error,no-member,no-name-in-module,redefined-outer-name,protected-access,duplicate-code,redefined-builtin \
		--output-format=text \
		--fail-under=9.5

lint-all: lint lint-tests
	@echo "All lint checks passed (≥9.5 for both source and tests)"

# ─── Formatting ─────────────────────────────────────────────────

format:
	@echo "Formatting code with Black..."
	black $(SRC_DIR)/ $(TEST_DIR)/ examples/
	@echo "Sorting imports with isort..."
	isort $(SRC_DIR)/ $(TEST_DIR)/ examples/

check-format:
	@echo "Checking code format..."
	black --check $(SRC_DIR)/ $(TEST_DIR)/ examples/

# ─── Type Checking ──────────────────────────────────────────────

check-type:
	@echo "Running MyPy type checker..."
	mypy $(SRC_DIR)/ --ignore-missing-imports

# ─── Documentation (Sphinx) ─────────────────────────────────────

html:
	@echo "Building Sphinx documentation..."
	$(SPHINX_APIDOC) -o $(DOCS_DIR)/source $(SRC_DIR)/ --force --separate
	$(SPHINX_BUILD) -b html $(DOCS_DIR) $(DOCS_HTML)
	@echo "Documentation built at: $(DOCS_HTML)/index.html"

serve: html
	@echo "Starting local server for documentation preview..."
	cd $(DOCS_HTML) && $(PYTHON) -m http.server 8000

doc-clean:
	@echo "Cleaning documentation build artifacts..."
	rm -rf $(DOCS_DIR)/_build $(DOCS_DIR)/source

# ─── Reporting ──────────────────────────────────────────────────

pylint-report:
	@echo "Generating Pylint report..."
	$(PYLINT) $(SRC_DIR)/ $(TEST_DIR)/ \
		--disable=import-error,no-member,no-name-in-module,redefined-outer-name,protected-access,duplicate-code,redefined-builtin \
		--output-format=text > PYLINT_REPORT_RAW.txt 2>&1
	@echo "Report saved to PYLINT_REPORT_RAW.txt"

coverage-report:
	@echo "Generating detailed coverage report..."
	$(PYTEST) $(TEST_DIR)/ --cov=$(SRC_DIR) --cov-report=html
	@echo "Coverage report at: htmlcov/index.html"

# ─── Cleanup ────────────────────────────────────────────────────

clean: doc-clean
	@echo "Cleaning Python artifacts..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name ".coverage" -delete
	find . -type f -name "*.db" -delete
	rm -rf htmlcov/ .coverage
	@echo "Clean complete."

# ─── Full Quality Check ─────────────────────────────────────────

quality: lint-all test check-format
	@echo "============================================"
	@echo "  Full Quality Check — ALL PASSED"
	@echo "============================================"
