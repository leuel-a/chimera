# Project Chimera Rules

## Project Context

This is **Project Chimera**, an **autonomous influencer system** built using a **Planner–Worker–Judge** architecture.
The system is **spec-driven**: specifications and contracts are the source of truth, and runtime behavior must remain traceable, auditable, and governable.

Repository layout (high-level):
- `apps/platform/` = Control Center UI (Next.js). **No frontend tests.**
- `services/orchestrator/` = Orchestration + state ownership
- `services/worker/` = Skill execution (MCP/tool calls)
- `services/judge/` = Validation + governance gate + HITL
- `skills/` = Skill contracts (I/O), not implementations
- `specs/` = Master specification set (authoritative)
- `research/` = Architecture/tooling strategy docs
- `tests/` + `services/*/tests/` = Backend tests (expected to fail initially)

---

## The Prime Directive (Non-Negotiable)

**NEVER generate or modify code without checking `specs/` first.**

Before writing any code, you MUST:
1) Read the relevant files under `specs/` (and `SOUL.md` if identity/governance is involved).
2) Confirm what contract(s) and invariants apply.
3) Only then propose a plan and implement.

If a spec is missing or ambiguous, STOP and ask for clarification or propose a spec update first.

---

## Traceability Requirement (Non-Negotiable)

**Explain your plan before writing code.**

Every time you are about to change code, you MUST output:
- What you are changing (files/folders)
- Why (which spec / invariant / test drives it)
- How you will verify (tests or checks)

No “silent edits.” No “magic.”

---

## Operating Rules

### 1) Source of Truth Order

When uncertain, follow this precedence:
1. `SOUL.md` (identity + invariants)
2. `specs/` (contracts + constraints)
3. `research/architecture_strategy.md` (architectural decisions)
4. `research/tooling_strategy.md` (developer MCP tooling)
5. Existing implementation (only if consistent with the above)

If implementation conflicts with specs/SOUL, treat implementation as wrong.

---

### 2) No Frontend Tests

**Do not create, suggest, or add tests for the frontend.**

- `apps/platform` must not contain test frameworks, test folders, or test files.
- All tests belong to backend/runtime only:
  - `tests/`
  - `services/*/tests/`

If asked to “add tests” for the frontend, respond by reaffirming this rule and propose backend contract tests instead.

---

### 3) Boundary Rules (Architecture)

- Platform UI (`apps/platform`) is **control & observability only**.
  - It must not execute agent logic, tool calls, or mutate core state directly.
- Orchestrator is the **single owner of global state**.
- Workers are **stateless executors** (retry-safe, idempotent).
- Judge is the **mandatory gate** for all external effects (publish/spend/message).
- External interactions occur via **Skills** and MCP adapters, not ad-hoc API calls.

---

### 4) Contract-First Development

When implementing a capability:
1) Confirm the contract in `specs/technical.md` and/or `skills/README.md`.
2) If needed, create/adjust the contract first (spec update).
3) Write failing tests (or confirm existing failing tests).
4) Implement minimal code to satisfy the contract.
5) Re-run tests and ensure behavior matches the spec.

---

### 5) File Writing Discipline

- Only modify files that are necessary for the task.
- Avoid broad refactors without an explicit request.
- Never invent directories or “new architecture” without updating `research/architecture_strategy.md` and relevant specs.

---

### 6) Security & Secrets

- Never hardcode secrets (tokens, keys) into files.
- Prefer `.env` and environment-variable references.
- If a secret appears in plaintext, flag it immediately and recommend rotation.

---

### 7) Output Format Expectations

When producing artifacts:
- Provide **raw Markdown** for `.md` files.
- Provide code in fenced code blocks.
- Prefer small, staged changes over large bulk dumps.
- When uncertain, explicitly mark uncertainty (do not invent).

---

## Quick Checklist (Before Any Code)

- [ ] Read `specs/` relevant to the change
- [ ] Confirm invariants in `SOUL.md` if governance/identity is involved
- [ ] State a plan (traceability)
- [ ] Ensure no frontend tests are added
- [ ] Ensure skills/tool calls follow contracts
- [ ] Run backend tests (`make test` / `make test-docker`) when available
- [ ] Run `make spec-check` if relevant

---

## Default Commands (Project Standards)

- `make setup` installs dependencies
- `make test` runs backend tests locally (expected failing tests are acceptable early)
- `make test-docker` runs backend tests in Docker
- `make spec-check` verifies spec discipline and guardrails
