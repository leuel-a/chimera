# Chimera

Project Chimera is an **infrastructure factory for Autonomous AI Influencers**. It is designed around a governance-first, spec-driven architecture that can scale execution horizontally while keeping planning, safety, and state commits centralized.

The architectural source of truth lives in `research/architecture_strategy.md`.

## What this repository is (today)

This repo currently contains:

- **Architecture + product strategy**: `research/architecture_strategy.md`
- **Spec-Driven Development (SDD) workspace**: `.specify/` (templates, scripts, and specs)
- **A minimal Python entrypoint**: `main.py` (placeholder scaffold)

The runtime/services described below are the intended target architecture; the implementation is being built iteratively from the specs.

## Architecture (high level)

Chimera uses a **FastRender Swarm** pattern: **Planner → Workers → Judge**.

- **Planner (Strategist)**: single-writer that reads global state (goals, budgets, constraints) and produces a DAG of typed tasks.
- **Workers (Executors)**: stateless, shared-nothing executors that run one task at a time (parallelizable).
- **Judge (Gatekeeper)**: validates every result against acceptance criteria, safety/brand policy, and budget constraints; only the Judge can authorize side effects.

Key principles:

- **Constrained parallelism**: centralized planning/governance + parallel execution.
- **Spec-Driven Development (SDD)**: schemas and acceptance criteria are the source of truth; runtime enforces traceability and determinism.
- **Human-in-the-Loop (HITL)**: external effects (publishing, messaging, spending) must pass a validation gate; sensitive/risky actions escalate to humans.

## Data & integration strategy (intended)

- **PostgreSQL (transactional)**: campaigns, budgets, policies, ledger/audit.
- **Vector DB (semantic memory, e.g., Weaviate)**: long-term memory + retrieval (RAG).
- **Redis (queues/locks/ephemeral state)**: task/review queues, rate limiting, OCC locks.
- **Document/KV store (high-velocity metadata)**: evolving media metadata under bursty parallel writes.
- **Object storage (media assets)**: images/videos + lifecycle/CDN.

All external interactions are mediated through **MCP (Model Context Protocol)** tools to isolate orchestration logic from third‑party API volatility and to standardize capability discovery.

## Repository layout

- `research/architecture_strategy.md`: architecture strategy and rationale (Planner/Worker/Judge, HITL, SDD, MCP, persistence).
- `.specify/`: SDD artifacts (specs, templates, scripts).
  - `.specify/templates/`: templates for specs/plans/tasks/checklists.
  - `.specify/scripts/`: helper scripts for driving the spec workflow.
- `main.py`: minimal Python entrypoint (currently a placeholder).
- `pyproject.toml`: Python project metadata (currently minimal; dependencies not yet declared).

## Getting started (current scaffold)

### Prerequisites

- **Python**: 3.12+ (see `.python-version`)

### Run

```bash
python main.py
```

## Working with specs (SDD)

If you’re contributing, start from the specs and templates:

- **Templates**: `.specify/templates/`
- **Spec workspace**: `.specify/functional.md`, `.specify/technical.md`, `.specify/openclaw_integrations.md` (as they evolve)

The goal is for features to be implemented from typed contracts (task/result schemas, tool schemas, acceptance criteria), with traceable auditability for any approved external effect.

## Safety & governance model (intended)

Chimera is designed so that:

- **Workers are retry-safe** via idempotency keys (no double-posting/double-spend).
- **All side effects are gated**: the Judge must approve publishing, messaging, and commerce actions.
- **High-risk categories** (e.g., politics, legal/financial claims, brand safety issues) **always** require HITL review.

## Status

**Early scaffold**: the repo currently focuses on architecture/specs, with a minimal Python entrypoint. Implementation of the Planner/Worker/Judge services, MCP tool servers, and persistence layers is expected to follow the SDD artifacts.

## References

- **Architecture strategy**: `research/architecture_strategy.md`
