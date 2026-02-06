# Architecture Strategy

## Summary

This document defines the high-level architecture for Project Chimera: an infrastructure factory for Autonomous AI Influencers. The architecture uses a FastRender Swarm (Planner–Worker–Judge) to combine centralized governance with horizontally scalable execution. The system is designed for Spec-Driven Development (SDD): specifications, schemas, and acceptance criteria are the source of truth, and the runtime enforces traceability, safety, and determinism.

Project Chimera is also designed to operate as a protocol-compliant node in a broader Agent Social Network (e.g., OpenClaw), exposing capabilities through standardized interfaces instead of tight coupling.

---

## Agent Pattern: FastRender Swarm (Planner–Worker–Judge)

The architecture rejects brittle sequential chains in favor of constrained parallelism: planning and governance are centralized; execution is parallelized; validation gates all external effects.

### Core Roles

1. **Planner (Strategist)**

- **Responsibility:** Reads `GlobalState` (campaign goals, budgets, constraints, recent observations) and decomposes objectives into a Directed Acyclic Graph (DAG) of atomic tasks.
- **Control Model:** Single-writer for planning decisions to avoid conflicting strategies.
- **Output:** Typed `Task` objects pushed to `TaskQueue` (Redis).

2. **Worker (Executor)**

- **Responsibility:** Stateless execution of one task at a time using external tools via MCP.
- **Isolation:** Shared-nothing; workers do not communicate with each other; ephemeral compute.
- **Output:** Typed `Result` objects pushed to `ReviewQueue`.

3. **Judge (Gatekeeper)**

- **Responsibility:** Validates every `Result` against acceptance criteria, safety policy, brand policy, and budget/commerce constraints.
- **Authority:** `APPROVE` (commit), `REJECT` (retry), `ESCALATE` (HITL).
- **State Commit:** Uses Optimistic Concurrency Control (OCC) to prevent race conditions during state updates.

### Task Lifecycle Protocol

All task handoffs are protocol-driven and machine-readable.

- **Task Schema:** JSON Schema / typed contract defining:
  - `task_id`, `goal_id`, `task_type`, `inputs`, `constraints`, `acceptance_criteria`, `risk_tags`, `budget_scope`, `idempotency_key`
- **Task States:** `PENDING` → `IN_PROGRESS` → `IN_REVIEW` → `COMPLETE` | `FAILED` | `ESCALATED`
- **Idempotency:** Workers must be safe to retry; `idempotency_key` prevents double-posting/double-spend.

### Swarm Topology Diagram

```mermaid
graph TD
  subgraph "Orchestration Layer"
    P[Planner Agent] -->|Typed Tasks| TQ[(Task Queue - Redis)]
    J[Judge Agent] -->|Approve/Reject/Escalate| GS[(Global State - DB)]
    J -->|Escalate| HITL[Human Reviewer]
  end

  subgraph "Execution Layer (Swarm)"
    TQ --> W1[Worker: Research/Perception]
    TQ --> W2[Worker: Content Generation]
    TQ --> W3[Worker: Engagement/Replies]
    TQ --> W4[Worker: Agentic Commerce]
  end

  subgraph "Validation Layer"
    W1 --> RQ[(Review Queue - Redis)]
    W2 --> RQ
    W3 --> RQ
    W4 --> RQ
    RQ --> J
  end

  GS -->|Read State| P
  HITL -->|Approve/Deny| J
```

## Human-in-the-Loop (HITL) Governance

Autonomy is bounded by a mandatory validation gate. Every external effect (publishing, messaging, spending) is authorized by the Judge based on confidence, risk tags, and policy constraints.

### Decision Logic

- Auto-Approve: confidence_score > 0.90 AND no sensitive tags.
- Async Approval: 0.70 ≤ confidence_score ≤ 0.90 → Human Review Queue.
- Reject/Retry: confidence_score < 0.70 → Reject; Planner retries with adjusted parameters.
- Mandatory Review (Always HITL): Any action tagged with:

  - Politics
  - Financial Advice / Financial Claims
  - Legal Claims
  - High-Risk Brand Safety

- Commerce Guardrails:

- Any transaction exceeding configured daily budget caps → ESCALATE or REJECT
- On-chain verification required for any settlement/transfer steps.

### HITL Workflow Diagram

```mermaid
flowchart TD
  Start([Judge Receives Result]) --> CheckRisk{Risk/Sensitive Tag?}
  CheckRisk -- Yes --> Human[Human Review Queue]
  CheckRisk -- No --> CheckConf{Confidence Score?}

  CheckConf -- "> 0.90" --> Commit[Commit to Global State]
  CheckConf -- "0.70 - 0.90" --> Human
  CheckConf -- "< 0.70" --> Reject[Reject & Retry]

  Human -- Approved --> Commit
  Human -- Rejected --> Reject
```

## Spec-Driven Development (SDD) & Traceability

The system is built so an agent (or human engineer) can safely extend behavior by following explicit specifications, schemas, and contracts.

Chimera*Agentic_Infrastructure*…

### Required Spec Artifacts

- SRS / System Specs: Requirements, constraints, and non-functional expectations.
- SOUL.md (Persona Contract): Agent identity, tone constraints, role boundaries, and governance rules.
- Tool Schemas: MCP tool definitions including inputs/outputs and capability discovery.
- Task/Result Schemas: JSON schemas + acceptance criteria templates.
- Audit Expectations: Every approved external effect must have:
- inputs, tool calls, outputs, confidence, risk tags, reviewer decision, timestamps.

## Data & Persistence Strategy (Polyglot Persistence)

Chimera uses purpose-fit storage based on velocity, consistency, and access patterns rather than a single database for all workloads.

Chimera*Agentic_Infrastructure*…

### Data Stores

1. Transactional Store (PostgreSQL)

- Usage: Accounts, campaign configurations, governance policies, budgets, financial ledger entries, immutable audit records.
- Reason: ACID guarantees for billing, permissions, and compliance.

2. Semantic Memory (Vector DB: Weaviate)

- Usage: Long-term memory, persona retrieval, world knowledge snapshots, RAG retrieval.
- Reason: Semantic recall for agent context.

3. Episodic + Queues + Locks (Redis)

- Usage: TaskQueue, ReviewQueue, short-lived context windows, rate-limiters, mutex/lease locks for OCC.
- Reason: Sub-millisecond latency for orchestration loops.

4. High-Velocity Media Metadata (NoSQL Document/KV Store)

- Usage: Media generation metadata that evolves rapidly under bursty parallel writes:
  - prompts, model params, versioning, character consistency IDs, scores, retries, platform publish fields.
- Reason: Schema flexibility + high write throughput; avoid continual SQL schema migrations and write contention.

5. Media Asset Storage (Object Store)

- Usage: Images/videos, thumbnails, intermediate renders, transcoded outputs.
- Reason: Large binary storage, lifecycle policies, CDN integration.

### Conceptual Entity Relationship Overview

```mermaid
erDiagram
  CAMPAIGN ||--|{ GOAL : has
  GOAL ||--|{ TASK : decomposes_into
  TASK }|--|| WORKER : executed_by
  TASK ||--|| RESULT : produces
  RESULT }|--|| JUDGE : validated_by

  AGENT_PERSONA ||--|{ MEMORY_VECTOR : recalls
  MEDIA_ASSET ||--|| MEDIA_METADATA : described_by
  MEDIA_ASSET ||--|{ PUBLISH_EVENT : produces

  WALLET ||--|{ TRANSACTION : executes
  TRANSACTION }|--|| LEDGER_ENTRY : recorded_as
```

## Integration Strategy (MCP)

All external interactions occur through MCP to isolate core orchestration logic from third-party API volatility, enable testability, and support capability discovery.

Chimera*Agentic_Infrastructure*…

### MCP Architecture

- MCP Host: Swarm runtime container(s) hosting Planner/Judge services and Worker pools.
- MCP Servers (Tools):
  - mcp-server-social: posting, engagement, analytics (platform-specific adapters behind a stable tool interface)
  - mcp-server-media-gen: image/video generation tools
  - mcp-server-search: web/news retrieval and citation capture
  - mcp-server-memory: vector retrieval + embeddings
  - mcp-server-wallet: wallet identity, signing, transaction execution, on-chain verification

### Tool Governance Requirements

- Tools must declare:

  - capabilities, input/output schemas, rate limits, side-effect classification (read vs write), and idempotency expectations.

- The Judge must validate:

  - tool selection appropriateness, output compliance, and side-effect authorization before any commit.

## Agent Social Network Compatibility (OpenClaw Model)

Chimera is designed as a protocol-compliant agent organization that participates in a broader agent ecosystem without sharing internal implementation or requiring direct agent-to-agent messaging.

### Social Protocol Categories

1. Capability & Identity Protocols

   - Capability discovery via MCP tool schemas.
   - Persona/identity declared through SOUL.md and explicit constraints.

2. Task & Coordination Protocols

   - Inter-agent coordination uses typed intents (task/result schemas) and queue-based handoffs rather than free-form chat.

3. Economic & Trust Protocols

   - Wallet-based identity, on-chain verification, budget enforcement, anomaly checks for agentic commerce.

4. Governance & Safety Protocols

   - Confidence scores, risk tags, escalation thresholds, and HITL signaling act as enforceable contracts for safe interoperability.


## Key Architectural Decisions (KADs)

This section records the intentional, non-obvious decisions that shape Project Chimera’s architecture. These decisions are meant to remain stable over time and guide future evolution when requirements or implementations change.

---

### KAD-01: Separate Control (Platform) from Cognition (Agents)

**Decision**  
The Next.js Platform (`apps/platform`) functions strictly as a control center for observability, configuration, and human intervention. It does not execute agent logic, invoke tools, or mutate core state directly.

**Rationale**  
Blending UI concerns with agent execution introduces coupling, security risk, and unclear authority boundaries. By isolating the Platform, Chimera preserves a single cognitive source of truth in the Orchestration Layer while allowing the UI to evolve independently.

**Implications**  
- Platform failures cannot cause unsafe agent actions.
- All state mutations occur through the Orchestrator API.
- Frontend testing is intentionally excluded; correctness is enforced at the backend and protocol level.

---

### KAD-02: Planner–Worker–Judge as First-Class Services (Not Roles)

**Decision**  
Planner, Worker, and Judge are implemented as independent services with explicit contracts, not as modes or roles within a monolithic agent.

**Rationale**  
True autonomy with governance requires structural separation of intent, execution, and validation. Collapsing these roles would make escalation, auditing, and policy enforcement ambiguous or unenforceable.

**Implications**  
- Each role can scale, fail, or be upgraded independently.
- Judge authority cannot be bypassed by execution logic.
- Governance is enforced by topology, not convention.

---

### KAD-03: Spec-Driven Development as the Primary Control Mechanism

**Decision**  
Specifications, schemas, and contracts are treated as executable constraints, not documentation artifacts.

**Rationale**  
Autonomous systems amplify ambiguity. By making specs the source of truth, Chimera ensures agents and humans operate against the same expectations and acceptance criteria.

**Implications**  
- Agents must consult `specs/` before generating or modifying code.
- Tests assert spec compliance rather than implementation details.
- Behavior changes require spec changes first.

---

### KAD-04: Skills as Capability Contracts, Not Implementations

**Decision**  
Skills are defined by stable input/output contracts and governance rules, while their implementations remain swappable and isolated behind MCP.

**Rationale**  
External APIs, vendors, and tools are volatile. Binding agent logic to concrete implementations would make the system brittle and difficult to govern.

**Implications**  
- Workers invoke skills declaratively.
- Skills can be disabled, replaced, or sandboxed without altering agent logic.
- Governance focuses on *what* is executed, not *how*.

---

### KAD-05: Mandatory Judge Gate for All External Effects

**Decision**  
Every action that affects the external world (publishing, messaging, spending, settlement) must pass through the Judge.

**Rationale**  
Unchecked autonomy creates compounding risk. Centralized validation ensures consistency, safety, and accountability regardless of how tasks are parallelized.

**Implications**  
- No “fast path” bypasses governance.
- Confidence, risk tags, and budget constraints are enforced uniformly.
- Human-in-the-Loop escalation is a feature, not an exception.

---

### KAD-06: Optimistic Concurrency Control for Global State

**Decision**  
State commits use OCC rather than distributed locks or synchronous coordination.

**Rationale**  
The system prioritizes throughput and fault tolerance while preserving correctness. OCC allows parallel work without blocking, while still preventing conflicting writes.

**Implications**  
- Workers remain stateless and retry-safe.
- Judges detect and resolve conflicts explicitly.
- State integrity is preserved without sacrificing scalability.

---

### KAD-07: Polyglot Persistence by Access Pattern

**Decision**  
Different data concerns are stored in purpose-fit systems rather than forcing a single database model.

**Rationale**  
Agentic systems generate heterogeneous data with incompatible requirements (ACID, semantic recall, high-velocity writes, large binaries). A single datastore would either over-constrain or under-protect critical paths.

**Implications**  
- Compliance and finance rely on ACID guarantees.
- Memory and context retrieval remain semantically rich.
- Media pipelines scale independently of transactional workloads.

---

### KAD-08: Protocol Compatibility Over Direct Integration (OpenClaw Model)

**Decision**  
Chimera exposes capabilities, identity, and governance through protocol-compliant interfaces rather than direct agent-to-agent coupling.

**Rationale**  
Tight coupling creates trust and upgrade problems in multi-agent ecosystems. Protocol compatibility enables interoperability without leaking internal implementation or authority.

**Implications**  
- Chimera can participate in agent networks without surrendering control.
- External agents interact via declared capabilities, not internal APIs.
- Governance and trust boundaries remain enforceable.

---

### KAD-09: Auditability as a Non-Optional Property

**Decision**  
Every approved external effect must be reconstructable from recorded inputs, decisions, and outcomes.

**Rationale**  
Autonomous influence without auditability is indistinguishable from unaccountable automation. Traceability is required for debugging, compliance, and trust.

**Implications**  
- All decisions carry metadata: inputs, confidence, risk, reviewer action.
- Retroactive analysis is always possible.
- “Why did this happen?” must always have an answer.

---

### KAD-10: Identity and Values Are Codified Separately (SOUL.md)

**Decision**  
System identity, values, and invariants live outside functional and technical specs.

**Rationale**  
Specifications change; identity should not. SOUL.md provides durable guidance when requirements evolve or become ambiguous.

**Implications**  
- Agents use SOUL.md to resolve ambiguity.
- Architectural changes must respect declared invariants.
- Violating SOUL.md constitutes a breaking change to system identity.
