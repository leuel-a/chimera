#!/usr/bin/env bash
set -euo pipefail

required_files=(
  "SOUL.md"
  "specs/_meta.md"
  "specs/functional.md"
  "specs/technical.md"
  "specs/openclaw_integration.md"
  "research/architecture_strategy.md"
  "research/tooling_strategy.md"
)

for f in "${required_files[@]}"; do
  if [ ! -f "$f" ]; then
    echo "spec-check: missing required file: $f" >&2
    exit 1
  fi
done

# Non-negotiable: frontend tests are not allowed.
if [ -d "apps/platform" ]; then
  if find "apps/platform" -type d -name "__tests__" -print -quit | grep -q .; then
    echo "spec-check: frontend tests detected (apps/platform/**/__tests__/**)" >&2
    exit 1
  fi

  if find "apps/platform" -type f \( \
      -name "*.spec.js" -o -name "*.spec.jsx" -o -name "*.spec.ts" -o -name "*.spec.tsx" -o \
      -name "*.test.js" -o -name "*.test.jsx" -o -name "*.test.ts" -o -name "*.test.tsx" \
    \) -print -quit | grep -q .; then
    echo "spec-check: frontend test files detected (apps/platform/**/*.spec|test.*)" >&2
    exit 1
  fi
fi

# Scope rule: tests must live only in:
# - tests/
# - services/*/tests
# This catches Python test files outside those paths.
disallowed_py_tests=$(find . -type f \( -name "test_*.py" -o -name "*_test.py" \) \
  -not -path "./tests/*" \
  -not -path "./services/*/tests/*" \
  -not -path "./.venv/*" \
  -not -path "./node_modules/*" \
  -not -path "./apps/platform/*" \
  -not -path "./apps/platform/node_modules/*" \
  -not -path "./apps/platform/.next/*" \
  -not -path "./.git/*" \
  -print)

if [ -n "$disallowed_py_tests" ]; then
  echo "spec-check: disallowed test files found outside allowed paths:" >&2
  echo "$disallowed_py_tests" >&2
  exit 1
fi

echo "spec-check: OK"
