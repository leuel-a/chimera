# Project Chimera Specs Meta

## Vision

Project Chimera is an autonomous influencer network that transitions from automated scheduling to persistent, goal-directed influencer agents. The system supports a scalable fleet (hundreds to thousands) of agents managed by a centralized Orchestrator with “management by exception.”

## Primary Users

1. Network Operators: set campaign goals and monitor fleet health.
2. Human Reviewers (HITL): approve/reject/edit flagged content.
3. Developers/System Architects: extend MCP servers, prompts, skills, infra.

## Non-Negotiable Architectural Pillars

1. Swarm execution pattern: Planner, Worker, Judge roles.
2. MCP as the universal external integration layer (Resources/Tools/Prompts).
3. Governance: HITL routing using confidence scoring + sensitive-topic overrides.
4. Agentic commerce (optional): non-custodial wallets and transaction governance.

## Constraints

- Platform volatility: external APIs change frequently. Integrations MUST be isolated behind MCP servers.
- Cost governance: expensive inference and media generation requires budget controls.
- Compliance: agents must support self-disclosure and AI labeling where available.
- Scale: system must support large concurrent agent counts without degrading orchestrator performance.

## Assumptions

- Platform UI is the operator cockpit and talks ONLY to Orchestrator APIs.
- Orchestrator is the canonical state owner (Postgres).
- Redis supports short-term state and queueing.
- Weaviate stores semantic memory/persona/mutable memories.

## Out of Scope (Initial MVP)

- Full production-grade OpenClaw federation (only a status publishing scaffold is defined).
- Full media generation implementation (only MCP tool contracts are defined).
