# Functional Requirements (User Stories)

## Fleet Operations (Operator)

- As a Network Operator, I need to view a real-time fleet status dashboard showing each agent’s current state (Planning/Working/Judging/Sleeping), wallet balance, and HITL queue depth.
- As a Network Operator, I need to define a campaign goal in natural language and see a generated task tree (DAG) before execution begins.
- As a Network Operator, I need to pause/resume a campaign and ensure in-flight work does not commit stale results.

## HITL Moderation (Reviewer)

- As a Human Reviewer, I need to see a queue of items requiring review, including generated content, confidence_score, and reasoning_trace.
- As a Human Reviewer, I need to approve, reject, or edit content and have the system proceed accordingly.
- As a Human Reviewer, I need sensitive-topic content (politics, health, finance, legal) to ALWAYS route to mandatory review regardless of confidence score.

## Agent Persona & Memory

- As an Agent, I need to load my immutable persona definition from SOUL.md.
- As an Agent, I need hierarchical memory retrieval (short-term cache + long-term semantic retrieval) before generating output.
- As an Agent, I need my successful interactions summarized into long-term memory over time (Judge-triggered).

## Perception & Trends

- As an Agent, I need to poll MCP Resources (mentions/news/market) to ingest changes in the world.
- As an Agent, I need semantic filtering and relevance scoring before turning ingested content into tasks.
- As an Agent, I need a “Trend Spotter” worker to detect topic clusters and generate a Trend Alert for the Planner.

## Content Generation (Creative Engine)

- As a Worker, I need to generate text, images, and video via MCP Tools (never direct vendor APIs).
- As a Worker, I must include a character_reference_id or style LoRA identifier in image generation requests for character consistency.
- As a Judge, I need to validate generated images for character consistency before allowing publication.

## Social Actions (Action System)

- As a Worker, I need platform-agnostic publishing via MCP tools (post/reply/like).
- As a system, I need a bi-directional loop: ingest -> plan -> generate -> act -> verify.

## Agentic Commerce (Optional)

- As an Agent, I need a unique non-custodial wallet.
- As a Planner, I must check get_balance before any cost-incurring workflow.
- As a CFO Judge, I must approve/reject every transaction request and enforce budget limits and anomaly detection.

## Swarm Governance

- As the system, I need Planner/Worker/Judge implemented as decoupled services using queues:
  - Planner pushes tasks to TaskQueue
  - Worker pushes results to ReviewQueue
  - Judge validates and commits or re-queues
- As a Judge, I need optimistic concurrency control to prevent stale commits.
