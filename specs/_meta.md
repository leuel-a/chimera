## Project Chimera – Master Specification Meta

### 1. System Identity and Vision

Project Chimera is an **autonomous influencer system operating at fleet scale**. It coordinates long‑lived AI agents that plan, execute, and govern influencer operations across many campaigns, personas, and platforms.

The system’s purpose is to **prove that autonomy can scale without losing governance, accountability, or trust**. Autonomy is treated as a liability unless it is:

- **Constrained by explicit governance**
- **Auditable end‑to‑end**
- **Interruptible at all times**

Chimera embodies a **Planner–Worker–Judge** pattern inside a **hub‑and‑spoke orchestration architecture**:

- **Planner (Strategist)**: Decomposes goals into a DAG of tasks.
- **Workers (Executors)**: Perform atomic work using external skills/tools.
- **Judges (Gatekeepers)**: Authorize or block all state commits and external effects.

Human operators **manage by exception** via a Platform UI, while the orchestrator and worker swarm drive day‑to‑day operations.

### 2. Scope and System Boundaries

#### 2.1 In‑Scope Capabilities

Chimera, as specified in this spec kit, is responsible for:

- **Campaign‑level autonomy**

  - Tracking goals, constraints, and budgets for many campaigns and personas.
  - Continuously replanning work based on performance and observations.

- **Content and interaction workflows**

  - Researching trends and context.
  - Generating and refining media assets (with an emphasis on video and social content).
  - Proposing posts, replies, and engagement actions.

- **Governance and safety**

  - Applying policy, safety, and brand constraints to all proposed actions.
  - Routing sensitive or low‑confidence actions to human review.
  - Maintaining full audit trails for decisions and external effects.

- **Spec‑Driven Development (SDD)**

  - Treating `specs/` as the **source of truth** for behavior and contracts.
  - Requiring that Planner, Worker, Judge, and Skills operate against machine‑readable schemas.

- **Agent social network participation**
  - Exposing Chimera as a protocol‑compliant node in an external network (e.g. OpenClaw‑style).
  - Advertising capabilities, identity, and governance posture rather than concrete implementations.

#### 2.2 Out‑of‑Scope / Non‑Responsibilities

Chimera explicitly does **not**:

- Become a general‑purpose AGI assistant or chat interface.
- Provide guarantees about specific social platform algorithms beyond best‑effort use of their public surfaces.
- Replace legal, financial, or compliance review for high‑risk decisions.
- Guarantee optimal creative quality; it optimizes for **governable consistency**, not artistic maximalism.
- Serve as a custodial financial system; when commerce is enabled it operates with non‑custodial patterns and strict gates.

These non‑goals are intentional guardrails; expanding into them requires explicit constitutional changes, not silent drift.

### 3. Architectural Frame

Chimera adheres to the following durable architectural patterns:

- **Planner–Worker–Judge as first‑class services**

  - Planning, execution, and judgment are structurally separated and communicate via typed envelopes.
  - No single service may unilaterally plan, execute, and approve the same action.

- **Hub‑and‑spoke orchestration**

  - A central orchestrator owns global state, task routing, and governance flows.
  - A worker swarm executes tasks as stateless, shared‑nothing processes.
  - Judges sit on the commit path for all external effects.

- **MCP‑mediated skills**

  - All external platform actions and advanced capabilities are exposed as **skills** with stable input/output contracts.
  - Core services never embed vendor‑specific SDKs; they call skills via a neutral protocol layer.

- **Governance‑first autonomy**

  - Confidence scores, risk tags, and budgets are first‑class fields in every task/result envelope.
  - Human‑in‑the‑loop (HITL) review is a normal operating mode, not an exceptional fallback.

- **Spec‑driven contracts**
  - Agent behaviors, API shapes, and storage schemas are defined here, then implemented.
  - When implementation disagrees with these specs, the implementation is considered defective.

### 4. What Chimera Is and Is Not

#### 4.1 What Chimera Is

- **A long‑lived autonomous influencer factory**

  - Manages many agents, campaigns, and personas over time.
  - Preserves memory, identity, and continuity per tenant and persona.

- **A governed orchestration system**

  - Every external action (publishing, messaging, spending) passes through a Judge gate.
  - Every decision and effect can be traced back to its originating goal, task, tools, and reviewers.

- **A protocol participant**
  - Designed to operate as a node in an agent network, exposing capabilities and status in a standardized way while shielding interior implementation.

#### 4.2 What Chimera Is Not

- **Not a monolithic “smart bot”**

  - No single process performs planning, execution, and approval.

- **Not a shadow‑IT integration layer**

  - It does not encourage ad‑hoc direct calls to social networks, wallets, or other APIs; all access is mediated through governed skills.

- **Not an engagement‑at‑any‑cost engine**
  - Engagement metrics are inputs to planning, not the single overriding objective.
  - The system’s identity and constitution prioritize safety, explainability, and control over raw reach.

### 5. Global Constraints and Invariants

The following constraints are treated as **hard invariants** for all components and integrations:

- **Explainability**

  - For every external effect, the system must be able to reconstruct:
    - The initiating goal and campaign.
    - The task DAG path taken.
    - The exact worker outputs, skill calls, and parameters.
    - The Judge decision and (where applicable) human reviewer rationale.

- **Interruptibility and override**

  - Human operators can pause campaigns, agents, or entire tenants without race conditions or partial side effects.
  - Judges and orchestrator must fail closed (no silent side effects) when critical dependencies are unavailable.

- **Separation of concerns**

  - Planner, Worker, and Judge remain distinct services with non‑overlapping authority.
  - The Platform UI never talks directly to databases, queues, or external platforms.

- **Idempotent execution**

  - Task execution and external side effects must be safe to retry.
  - Idempotency keys are part of the canonical contracts for operations that can double‑submit (e.g. publishing, payments).

- **Multi‑tenant isolation**

  - All state and interactions are scoped to a tenant context.
  - No cross‑tenant retrieval of memory, metrics, or secrets is permitted.

- **MCP‑only external actions**
  - External social, media, search, and commerce actions are executed **only** via governed skills/tool contracts.

Where implementation trade‑offs are required, they must respect these invariants first.

### 6. Stability Assumptions

The following aspects are expected to remain stable across many implementation iterations and technology refreshes:

- **Role topology**

  - The existence of Planner, Worker, Judge, Orchestrator, and Platform as separate concerns is stable.

- **Governance posture**

  - All external effects are gated by Judges and may be escalated to humans; there is no “fast path” that bypasses this.

- **Spec‑first workflow**

  - New behaviors, APIs, and schema changes are introduced by amending specs in this directory before code changes.

- **Protocol compatibility**

  - External networks (OpenClaw or successors) interact with Chimera via capabilities, intents, and governance profiles, not internal process APIs.

- **Polyglot persistence**
  - Different storage technologies may change over time, but the conceptual split between:
    - transactional truth,
    - high‑velocity media metadata,
    - semantic memory,
    - queues/locks,
      remains.

Any change that breaks these assumptions must be treated as a **constitutional change**, not a routine refactor.

### 7. Ambiguities and Open Questions

This meta spec tracks known ambiguities that materially affect downstream specs and implementations:

- **Ethics vs. engagement priority**

  - The project’s identity documents strongly imply that ethical alignment and safety should override raw engagement, but this is not formalized as a hard ordering of objectives.
  - **[OPEN]**: Confirm whether engagement‑driven objectives may ever override conservative safety defaults, and under what governance process.

- **External network protocol specifics**
  - OpenClaw (or similar) is treated here as a class of agent social networks, but concrete message types, authentication schemes, and capability taxonomies are not yet fixed.
  - **[OPEN]**: Align this spec with a concrete upstream protocol version once one is selected.

These open points should be resolved via updates to SOUL, the constitution, and this spec kit before implementing conflicting behavior.

### 8. Spec Kit Index

This meta file is the entry point for the Chimera spec kit. The core spec documents are:

- **`specs/_meta.md` (this file)**  
  High‑level vision, scope, invariants, and cross‑cutting constraints.

- **`specs/functional.md`**  
  Functional behavior described as user stories for Planner, Worker, Judge, human operators, and external networks. Focuses on observable behavior and acceptance intent.

- **`specs/technical.md`**  
  Technical contracts and structural guarantees, including:

  - Agent API envelopes and JSON schemas.
  - Database/entity relationship diagrams for tasks, results, media, and audit trails.
  - Global invariants for idempotency, concurrency control, and traceability.

- **`specs/openclaw_integration.md`**  
  Protocol‑level description of how Chimera exposes identity, capabilities, and governance posture to an external agent network. Includes assumptions and clearly marked uncertainties where upstream specifications are incomplete.

All new work on Planner, Worker, Judge, skills, or Platform integrations MUST trace back to one or more sections of these documents.
