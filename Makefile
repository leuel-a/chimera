PROJECT_NAME := chimera
PY := uv
PYTEST := PYTHONPATH=. uv run pytest
TEST_IMAGE := $(PROJECT_NAME)-tests:local

# Backend-only test scope (frontend excluded by policy)
TEST_PATHS := tests services/*/tests

.PHONY: setup setup-py setup-node test test-docker spec-check clean

setup: setup-py setup-node

setup-py:
	$(PY) sync --frozen

setup-node:
	@if [ -f package-lock.json ]; then npm ci; fi
	@if [ -f apps/platform/package-lock.json ]; then (cd apps/platform && npm ci); fi

test:
	$(PYTEST) -q $(TEST_PATHS)

test-docker:
	docker build -f Dockerfile.test -t $(TEST_IMAGE) .
	docker run --rm $(TEST_IMAGE)

spec-check:
	bash ./scripts/spec_check.sh

clean:
	rm -rf .pytest_cache .mypy_cache __pycache__
