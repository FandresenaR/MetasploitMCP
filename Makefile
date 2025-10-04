# Makefile for MetasploitMCP testing and development

.PHONY: help install-deps test test-unit test-integration test-options test-helpers test-tools coverage clean lint format start-msf stop-msf restart-msf

# Default target
help:
	@echo "Available targets:"
	@echo "  help           - Show this help message"
	@echo "  install-deps   - Install test dependencies"
	@echo "  start-msf      - Start msfrpcd daemon (from .env.local)"
	@echo "  stop-msf       - Stop msfrpcd daemon"
	@echo "  restart-msf    - Restart msfrpcd daemon"
	@echo "  test           - Run all tests"
	@echo "  test-unit      - Run unit tests only"
	@echo "  test-integration - Run integration tests only"
	@echo "  test-options   - Run options parsing tests only"
	@echo "  test-helpers   - Run helper function tests only"
	@echo "  test-tools     - Run MCP tools tests only"
	@echo "  coverage       - Run tests with coverage report"
	@echo "  coverage-html  - Run tests with HTML coverage report"
	@echo "  lint           - Run linting checks"
	@echo "  format         - Format code"
	@echo "  clean          - Clean up generated files"

# Install test dependencies
install-deps:
	python -m pip install -r requirements-test.txt

# Metasploit daemon management
start-msf:
	@./start-msfrpcd.sh

stop-msf:
	@./stop-msfrpcd.sh

restart-msf: stop-msf
	@sleep 2
	@./start-msfrpcd.sh

# Test targets
test:
	python run_tests.py --all

test-unit:
	python run_tests.py --unit

test-integration:
	python run_tests.py --integration

test-options:
	python run_tests.py --options

test-helpers:
	python run_tests.py --helpers

test-tools:
	python run_tests.py --tools

# Coverage targets
coverage:
	python run_tests.py --all --coverage

coverage-html:
	python run_tests.py --all --coverage --html
	@echo "Coverage report: file://$(PWD)/htmlcov/index.html"

# Code quality targets
lint:
	@echo "Running flake8..."
	-python -m flake8 MetasploitMCP.py tests/ --max-line-length=120 --ignore=E203,W503
	@echo "Running pylint..."
	-python -m pylint MetasploitMCP.py --disable=C0301,C0103,R0903,R0913

format:
	@echo "Running black code formatter..."
	-python -m black MetasploitMCP.py tests/ --line-length=120
	@echo "Running isort import formatter..."
	-python -m isort MetasploitMCP.py tests/

# Cleanup
clean:
	rm -rf __pycache__/
	rm -rf tests/__pycache__/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf *.pyc
	rm -rf tests/*.pyc
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} +

# Development targets
dev-setup: install-deps
	@echo "Development environment setup complete"

check: lint test
	@echo "All checks passed!"

# CI/CD targets
ci-test:
	python run_tests.py --all --coverage --verbose

# Quick test (no coverage)
quick-test:
	pytest tests/ -x -v

# Test with failure details
test-debug:
	pytest tests/ -v --tb=long --capture=no
