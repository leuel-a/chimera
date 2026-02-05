# Project Chimera Constitution

<!--
Sync Impact Report
==================
Version change: 1.2.0 → 1.3.0
Modified sections:
  - Section 1: Purpose and Scope (expanded from stub to full content)
  - Section 2: Prime Directives (expanded from stub to full content)
  - Section 3: Architecture Constitution (expanded from stub to full content)
  - Section 4: Technology Stack Constitution (expanded from stub to full content)
Added sections: None
Removed sections: None
Templates requiring updates:
  ⚠ pending: .specify/templates/plan-template.md (verify alignment with Prime Directives)
  ⚠ pending: .specify/templates/spec-template.md (verify alignment with Purpose/Scope)
  ⚠ pending: .specify/templates/tasks-template.md (verify alignment with Prime Directives)
Follow-up TODOs: None
-->

## Preface

This constitution serves as the **single source of truth** for Project Chimera's governance, architecture, and development standards. It is derived from the Project Chimera Software Requirements Specification (SRS) and supersedes any inconsistent documentation, practices, or conventions found elsewhere in the repository.

All development work, architectural decisions, and tooling choices must align with the principles and constraints defined herein. Amendments to this constitution require documented rationale and version tracking.

---

## Table of Contents

1. [Purpose and Scope](#1-purpose-and-scope)
2. [Prime Directives (Non-Negotiables)](#2-prime-directives-non-negotiables)
3. [Architecture Constitution](#3-architecture-constitution)
4. [Technology Stack Constitution](#4-technology-stack-constitution)
5. [Repository & Folder Structure Constitution](#5-repository--folder-structure-constitution)
6. [Service Boundaries: Platform vs Orchestrator vs Workers](#6-service-boundaries-platform-vs-orchestrator-vs-workers)
7. [Agent Model Constitution (Planner/Worker/Judge)](#7-agent-model-constitution-plannerworkerjudge)
8. [MCP Integration Constitution (Developer Tools vs Runtime Skills)](#8-mcp-integration-constitution-developer-tools-vs-runtime-skills)
9. [Data & State Constitution](#9-data--state-constitution)
10. [Safety, HITL, and Governance Constitution](#10-safety-hitl-and-governance-constitution)
11. [Agentic Commerce & Wallet Security Constitution](#11-agentic-commerce--wallet-security-constitution)
12. [Performance, Scalability, Reliability Constitution](#12-performance-scalability-reliability-constitution)
13. [Multi-Tenancy & Isolation Constitution](#13-multi-tenancy--isolation-constitution)
14. [Observability & Auditability Constitution](#14-observability--auditability-constitution)
15. [Build, Run, Test & Docker Constitution](#15-build-run-test--docker-constitution)
16. [Spec Kit Blueprint Constitution (specs/ required files)](#16-spec-kit-blueprint-constitution-specs-required-files)
17. [Context Engineering Constitution (.cursor/rules or CLAUDE.md)](#17-context-engineering-constitution-cursorrules-or-claudemd)
18. [Tooling & Skills Strategy Constitution (research/ + skills/)](#18-tooling--skills-strategy-constitution-research--skills)
19. [TDD & Test Policy Constitution (failing tests first)](#19-tdd--test-policy-constitution-failing-tests-first)
20. [CI/CD & AI Review Policy Constitution (.github + CodeRabbit)](#20-cicd--ai-review-policy-constitution-github--coderabbit)
21. [Definition of Done & Acceptance Checks](#21-definition-of-done--acceptance-checks)
22. [Open Questions / Decisions Log](#22-open-questions--decisions-log)

---

## 1. Purpose and Scope

Project Chimera is an **autonomous influencer system** operating at **fleet scale**. The system enables autonomous AI agents to manage influencer operations across multiple accounts, platforms, and campaigns with minimal human intervention.

**Human Management Model**: Humans manage by exception through a centralized Platform. The Platform provides oversight, policy configuration, and intervention capabilities, but day-to-day operations are autonomous.

**System Architecture Overview**:

- **Orchestrator**: Coordinates work across the system, managing task distribution and workflow execution.
- **Workers**: Execute individual tasks in parallel, operating as stateless, shared-nothing executors.
- **Judges**: Govern all outcomes, validating results against acceptance criteria, safety policies, and budget constraints.
- **MCP Tools**: All external platform actions MUST be executed via MCP (Model Context Protocol) tools. Direct third-party SDK or API calls inside core agent logic are prohibited.

## 2. Prime Directives (Non-Negotiables)

The following directives are **non-negotiable** and MUST be followed in all development work:

1. **System Identity**: "This is Project Chimera, an autonomous influencer system."

2. **Spec-First Development**: "NEVER generate code without checking specs/ first." All code MUST be derived from and traceable to specifications in the `specs/` directory.

3. **Plan Before Code**: "Explain your plan before writing code." Developers and AI agents MUST articulate their approach, rationale, and expected outcomes before implementation.

4. **MCP Tool Requirement**: "All external platform actions MUST be executed via MCP tools. Direct third-party SDK/API calls inside core agent logic are prohibited." This ensures isolation, testability, and standardized capability discovery.

5. **Docker Containerization**: "Each project/service MUST have its own Docker container." Services SHALL be containerized independently to enable isolated deployment, scaling, and testing.

6. **Frontend Testing Prohibition**: "The Platform frontend MUST NOT have tests. No unit tests, no integration tests, no E2E tests. Do not create a frontend tests folder. Do not configure frontend test runners." Frontend testing is explicitly excluded from the project scope.

7. **Non-Frontend Testing Requirement**: "All non-frontend components MUST have tests (orchestrator, worker, skills, MCP servers, utilities)." All backend services, utilities, and integration components SHALL have comprehensive test coverage.

## 3. Architecture Constitution

### Hub-and-Spoke Pattern

Project Chimera SHALL follow a **hub-and-spoke architecture**:

- **Hub**: The Orchestrator serves as the central control plane, coordinating all system operations.
- **Spokes**: Worker swarm executes tasks in parallel, operating as stateless executors.
- **Human Cockpit**: The Platform provides human oversight and exception management.

### Component Roles

#### Orchestrator (Hub)

The Orchestrator SHALL serve as:

- **Control Plane API**: Primary interface for system coordination and task distribution.
- **Global State Owner**: Maintains authoritative state for campaigns, budgets, policies, and workflow state.
- **Governance Router**: Routes tasks to Workers, enforces concurrency limits, and manages task lifecycle.

The Orchestrator MUST NOT execute business logic directly; it coordinates and delegates to Workers.

#### Workers (Spokes)

Workers SHALL be:

- **Stateless Executors**: Each Worker processes one task at a time with no local persistent state.
- **Horizontally Scalable**: Workers MUST scale independently based on workload demand.
- **Shared-Nothing**: Workers MUST NOT share state or communicate directly with each other.

Workers receive tasks from the Orchestrator, execute them via MCP tools, and return results for validation.

#### Judges

Judges SHALL enforce:

- **Quality Gates**: Validate all Worker outputs against acceptance criteria and schemas.
- **Approvals**: Authorize side effects (publishing, messaging, commerce) based on safety and policy rules.
- **Concurrency Rules**: Ensure system-wide constraints (budgets, rate limits, quotas) are respected.

Judges MUST approve all external actions before they are executed.

#### Platform (Human Cockpit)

The Platform SHALL provide:

- **Human Interface**: Dashboard and controls for human oversight and intervention.
- **Policy Configuration**: Interface for setting safety rules, budgets, and governance policies.
- **Exception Management**: Capability for humans to review, approve, or reject high-risk actions.

The Platform MUST NOT connect directly to databases or queues; it SHALL communicate only through the Orchestrator API.

### Cloud-Native and Containerization

The system SHALL be:

- **Cloud-Native**: Designed for distributed, scalable deployment in cloud environments.
- **Containerized**: Each project/service MUST have its own Docker container image.
- **Microservices**: Services SHALL be independently deployable and scalable.

### Prohibited Patterns

The following architectural patterns are **prohibited**:

1. **Monolithic Single-Process Design**: The system MUST NOT be implemented as a single monolithic process. Services MUST be separated and independently deployable.

2. **Platform Direct Database/Queue Access**: The Platform MUST NOT connect directly to databases or message queues. All Platform interactions SHALL go through the Orchestrator API.

3. **Direct Social Platform APIs in Core Logic**: Direct third-party SDK or API calls inside core agent logic (Orchestrator, Workers, Judges) are prohibited. All external platform actions MUST be executed via MCP tools.

### Deployment Targets

#### Local Development and CI

- **Docker**: Docker containers SHALL be used for local development and CI/CD pipelines.
- Each service MUST have its own `Dockerfile` and be buildable independently.

#### Production

- **Kubernetes**: Production deployments SHALL use Kubernetes for orchestration and scaling.
- Services SHALL be deployed as Kubernetes deployments with appropriate resource limits, health checks, and scaling policies.

## 4. Technology Stack Constitution

This section defines the **Blessed Stack**—the approved technologies for Project Chimera. All technology choices MUST align with this stack unless explicitly approved through the decision log process.

### Backend (Required)

The backend stack SHALL consist of:

- **Python 3.12**: Primary programming language for all backend services.
- **FastAPI**: Web framework for Orchestrator APIs and service endpoints.
- **Pydantic v2**: Schema validation and data modeling for backend services.
- **PostgreSQL**: Transactional database for persistent state (campaigns, budgets, policies, ledger/audit).
- **Redis**: Message queues, caching, and short-term ephemeral state management.
- **Weaviate**: Vector database for semantic memory and RAG (Retrieval-Augmented Generation).
- **Celery** (or equivalent): Distributed task queue system backed by Redis for worker execution.

### MCP (Required)

- **MCP Host Runtime**: Runtime environment for executing MCP servers.
- **MCP Servers**: Both developer tools and runtime tools MUST be implemented as MCP servers.

All external platform integrations SHALL be exposed via MCP servers, not direct SDK/API calls.

### Agentic Commerce (Required if enabled)

When agentic commerce functionality is enabled:

- **Coinbase AgentKit**: SHALL be used for wallet management and action providers.
- **Secrets Management**: All secrets MUST be managed via a secrets manager service. Secrets MUST NOT be stored in the repository or logged. No secrets in code, no secrets in logs.

### Platform UI (Required)

The Platform frontend SHALL use:

- **Next.js (App Router)**: React framework with App Router architecture.
- **React**: UI library for component-based development.
- **TailwindCSS**: Utility-first CSS framework for styling.
- **shadcn/ui**: Component library built on Radix UI and TailwindCSS.
- **TanStack Query (React Query)**: Server-state management. This is the ONLY state management library permitted for server state.
- **Zod**: Schema validation for frontend forms and API contracts.

### Hard Prohibitions

The following are **explicitly prohibited**:

1. **Client-State Management Libraries**: The Platform MUST NOT add Redux, Zustand, MobX, Recoil, or any other client-state management library. TanStack Query SHALL be used exclusively for server state. Local component state SHALL use React's built-in `useState` and `useReducer` hooks.

2. **Frontend Testing**: The Platform MUST NOT include tests. No unit tests, no integration tests, no E2E tests. Do not create a frontend tests folder. Do not configure frontend test runners. (This prohibition is also stated in Prime Directives but reiterated here for clarity.)

### Technology Addition Process

**Rule**: No new framework, library, or tooling SHALL be added to the project without:

1. **Updating this section** with the new technology and its justification.
2. **Adding a decision log entry** in Section 22 (Open Questions / Decisions Log) documenting:
   - The technology choice
   - Rationale for selection
   - Alternatives considered
   - Impact on existing stack
   - Approval date and approver

This process ensures all technology decisions are documented, justified, and traceable.

## 5. Repository & Folder Structure Constitution

(Draft in Prompt X)

## 6. Service Boundaries: Platform vs Orchestrator vs Workers

(Draft in Prompt X)

## 7. Agent Model Constitution (Planner/Worker/Judge)

(Draft in Prompt X)

## 8. MCP Integration Constitution (Developer Tools vs Runtime Skills)

(Draft in Prompt X)

## 9. Data & State Constitution

(Draft in Prompt X)

## 10. Safety, HITL, and Governance Constitution

(Draft in Prompt X)

## 11. Agentic Commerce & Wallet Security Constitution

(Draft in Prompt X)

## 12. Performance, Scalability, Reliability Constitution

(Draft in Prompt X)

## 13. Multi-Tenancy & Isolation Constitution

(Draft in Prompt X)

## 14. Observability & Auditability Constitution

(Draft in Prompt X)

## 15. Build, Run, Test & Docker Constitution

(Draft in Prompt X)

## 16. Spec Kit Blueprint Constitution (specs/ required files)

(Draft in Prompt X)

## 17. Context Engineering Constitution (.cursor/rules or CLAUDE.md)

(Draft in Prompt X)

## 18. Tooling & Skills Strategy Constitution (research/ + skills/)

(Draft in Prompt X)

## 19. TDD & Test Policy Constitution (failing tests first)

(Draft in Prompt X)

## 20. CI/CD & AI Review Policy Constitution (.github + CodeRabbit)

(Draft in Prompt X)

## 21. Definition of Done & Acceptance Checks

(Draft in Prompt X)

## 22. Open Questions / Decisions Log

(Draft in Prompt X)

---

**Version**: 1.3.0 | **Ratified**: 2026-02-05 | **Last Amended**: 2026-02-05
