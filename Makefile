.PHONY: install data lint format test clean

install:
	pip install -e ".[dev]"

data:
	@echo "Run notebooks in 01_exploration to validate raw data"

lint:
	ruff check src tests

format:
	black src tests

test:
	pytest

clean:
	rm -rf __pycache__ .pytest_cache .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
