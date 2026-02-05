# Project Chimera Constitution

<!--
Sync Impact Report
==================
Version change: 2.4.0 → 2.5.0
Modified sections:
  - Section 1: Purpose and Scope (expanded from stub to full content)
  - Section 2: Prime Directives (expanded from stub to full content)
  - Section 3: Architecture Constitution (expanded from stub to full content)
  - Section 4: Technology Stack Constitution (expanded from stub to full content)
  - Section 5: Repository & Folder Structure Constitution (expanded from stub to full content)
  - Section 6: Service Boundaries: Platform vs Orchestrator vs Workers (expanded from stub to full content)
  - Section 7: Agent Model Constitution (Planner/Worker/Judge) (expanded from stub to full content)
  - Section 8: MCP Integration Constitution (Developer Tools vs Runtime Skills) (expanded from stub to full content)
  - Section 9: Data & State Constitution (expanded from stub to full content)
  - Section 10: Safety, HITL, and Governance Constitution (expanded from stub to full content)
  - Section 11: Agentic Commerce & Wallet Security Constitution (expanded from stub to full content)
  - Section 12: Performance, Scalability, Reliability Constitution (expanded from stub to full content)
  - Section 13: Multi-Tenancy & Isolation Constitution (expanded from stub to full content)
  - Section 14: Observability & Auditability Constitution (expanded from stub to full content)
  - Section 15: Build, Run, Test & Docker Constitution (expanded from stub to full content)
  - Section 16: Spec Kit Blueprint Constitution (specs/ required files) (expanded from stub to full content)
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

Project Chimera SHALL follow a **canonical monorepo structure** with clearly defined top-level directories. This structure ensures consistency, discoverability, and proper separation of concerns.

### Canonical Structure

The repository MUST include the following top-level directories and files:

- **`apps/platform`**: Platform UI lives here. This path is **mandatory** and MUST NOT be changed.
- **`services/orchestrator`**: Orchestrator service implementation.
- **`services/worker`**: Worker service implementation.
- **`skills`**: MCP skills and agent capabilities.
- **`specs`**: Specification documents (SDD artifacts).
- **`tests`**: Non-frontend tests only. Platform tests are prohibited.
- **`research`**: Research documents, architecture strategies, and design decisions.
- **`infra`**: Infrastructure as code, deployment configurations, and DevOps tooling.
- **`.github`**: GitHub Actions workflows, issue templates, and repository configuration.
- **`constitution.md`**: Project constitution (this document). Located at repository root.
- **`Makefile`**: Build, test, and deployment automation scripts.

### Directory Tree

```text
project-chimera/
├── apps/
│   └── platform/          # Platform UI (Next.js + React)
├── services/
│   ├── orchestrator/      # Orchestrator service
│   └── worker/            # Worker service
├── skills/                 # MCP skills and agent capabilities
├── specs/                  # Specification documents
├── tests/                  # Non-frontend tests only
├── research/               # Research and architecture docs
├── infra/                  # Infrastructure as code
├── .github/                # GitHub workflows and configs
├── Makefile                # Build automation
├── constitution.md         # Project constitution
└── README.md               # Project documentation
```

### Structural Rules

1. **No New Top-Level Folders**: No new top-level directories SHALL be created without:
   - Updating this section with the new directory and its purpose.
   - Adding a decision log entry in Section 22 (Open Questions / Decisions Log) documenting the rationale.

2. **Platform Path is Fixed**: The Platform UI MUST be located at `apps/platform`. This path MUST NOT be changed, moved, or renamed.

3. **Platform Testing Prohibition**: The Platform (`apps/platform`) MUST NOT contain:
   - Test folders (no `__tests__`, `tests`, `test`, `.test`, `.spec` directories).
   - Test configuration files (no Jest, Vitest, Playwright, or other test runner configs).
   - Test utilities or test helpers.

This prohibition aligns with Prime Directive #6 and Section 4 (Technology Stack Constitution).

4. **Service Structure**: Each service under `services/` SHALL have its own:
   - `Dockerfile` for containerization.
   - `pyproject.toml` or equivalent dependency management file.
   - Test directory structure (if applicable per service requirements).

5. **Specs Location**: All specification documents SHALL be organized under `specs/` following the SDD (Spec-Driven Development) workflow defined in the Spec Kit Blueprint Constitution (Section 16).

## 6. Service Boundaries: Platform vs Orchestrator vs Workers

This section defines **strict service boundaries** and responsibilities for each major component. These boundaries MUST NOT be violated. Violations compromise system architecture, testability, and scalability.

### Platform (`apps/platform`)

**Responsibilities**:

- **Human-Facing UI Only**: The Platform SHALL provide the user interface for human oversight, policy configuration, and exception management.
- **API Communication**: The Platform SHALL use TanStack Query (React Query) to call Orchestrator APIs. All server state MUST be managed through TanStack Query.
- **Input Validation**: The Platform MUST validate all user inputs with Zod before sending requests to the Orchestrator.

**Strict Boundaries**:

- The Platform MUST NOT connect directly to PostgreSQL, Redis, or Weaviate.
- The Platform MUST NOT execute business logic or make decisions about task routing, approvals, or state management.
- The Platform MUST NOT communicate directly with Workers or Judges.
- The Platform MUST NOT access message queues or task queues.

### Orchestrator (`services/orchestrator`)

**Responsibilities**:

- **Canonical Global State Owner**: The Orchestrator SHALL own and maintain the authoritative state for campaigns, budgets, policies, and workflow state.
- **Governance Logic**: The Orchestrator SHALL implement all governance logic, including task routing, concurrency limits, and policy enforcement.
- **API Provider**: The Orchestrator SHALL expose APIs consumed by the Platform and internal services.
- **Task Management**: The Orchestrator SHALL create tasks, route them to Workers, manage approvals, and coordinate the task lifecycle.
- **Database Operations**: The Orchestrator SHALL write to the database (PostgreSQL) for persistent state and read from it for state recovery and queries.

**Strict Boundaries**:

- The Orchestrator MUST NOT execute business logic that belongs in Workers (e.g., content generation, MCP tool calls).
- The Orchestrator MUST NOT directly execute Skills or make MCP tool calls.
- The Orchestrator MUST NOT bypass Workers to perform task execution.

### Worker (`services/worker`)

**Responsibilities**:

- **Stateless Executor**: Workers SHALL execute individual tasks with no local persistent state.
- **Skill Execution**: Workers SHALL execute Skills and make MCP tool calls as directed by task specifications.
- **Result Return**: Workers SHALL return results for Judge review and commit. Workers MUST NOT commit results directly to the database.

**Strict Boundaries**:

- Workers MUST NOT access the database (PostgreSQL) directly. All state reads and writes SHALL go through the Orchestrator.
- Workers MUST NOT create new tasks or modify task routing.
- Workers MUST NOT make approval decisions or bypass Judges.
- Workers MUST NOT communicate directly with the Platform.
- Workers MUST NOT share state or communicate directly with other Workers.

### No Boundary Violations

The following violations are **prohibited** and MUST NOT occur:

1. **Platform Direct Database Access**: Platform MUST NOT connect to PostgreSQL, Redis, or Weaviate. All data access MUST go through Orchestrator APIs.

2. **Platform Direct Worker Communication**: Platform MUST NOT communicate directly with Workers. All communication MUST go through the Orchestrator.

3. **Orchestrator Direct Execution**: Orchestrator MUST NOT execute Skills or make MCP tool calls directly. Execution MUST be delegated to Workers.

4. **Worker State Management**: Workers MUST NOT write directly to the database or manage global state. All state operations MUST go through the Orchestrator.

5. **Worker-to-Worker Communication**: Workers MUST NOT communicate directly with each other. All coordination MUST go through the Orchestrator.

6. **Platform Business Logic**: Platform MUST NOT contain business logic, governance rules, or decision-making logic. These MUST reside in the Orchestrator.

7. **Orchestrator Bypass**: Services MUST NOT bypass the Orchestrator to access databases, queues, or other services directly.

These boundaries ensure proper separation of concerns, enable independent scaling, and maintain system testability and maintainability.

## 7. Agent Model Constitution (Planner/Worker/Judge)

Project Chimera implements a **Planner/Worker/Judge** agent model that separates planning, execution, and governance concerns. This model enables scalable, safe, and auditable autonomous operations.

### Planner

The Planner SHALL:

- **Decompose Goals**: Break down high-level goals and objectives into concrete, actionable tasks.
- **Create Task DAG**: Generate a Directed Acyclic Graph (DAG) of tasks with dependencies, priorities, and resource requirements.
- **Replan**: Monitor execution progress and dynamically adjust the task DAG when conditions change, dependencies fail, or new information becomes available.

The Planner operates within the Orchestrator service and maintains the canonical view of the task graph and execution state.

### Worker

The Worker SHALL:

- **Execute Atomic Tasks**: Process one task at a time, ensuring atomicity and idempotency.
- **Stateless Operation**: Maintain no local persistent state between task executions. All state MUST be managed by the Orchestrator.
- **Use MCP Tools**: Execute tasks by invoking MCP (Model Context Protocol) tools as specified in the task definition.
- **Produce Artifacts**: Generate outputs (content, data, results) as specified by the task requirements.

Workers are horizontally scalable, stateless executors that receive tasks from the Orchestrator and return results for validation.

### Judge

The Judge SHALL:

- **Validate**: Verify that Worker outputs meet acceptance criteria, schema requirements, and quality standards.
- **Approve/Reject**: Make binary decisions on whether results should be committed or rejected based on safety policies, brand guidelines, and governance rules.
- **Enforce Governance**: Apply budget constraints, rate limits, concurrency rules, and policy compliance checks.
- **Control Commits**: Authorize all state commits and external actions. Only approved results SHALL be persisted or executed.

Judges operate within the Orchestrator service and serve as the gatekeeper for all side effects and state changes.

### Concurrency & State Commit Rules

**Optimistic Concurrency Control (OCC)**: The system SHALL enforce Optimistic Concurrency Control using `state_version` or equivalent versioning mechanism. All state reads MUST include the current version, and all state writes MUST verify the version has not changed.

**Conflict Resolution**: On conflict (version mismatch):

1. **Re-read State**: Fetch the current state and version from the authoritative source.
2. **Replan**: Re-evaluate the task DAG and execution plan based on the updated state.
3. **Retry with Backoff**: Retry the operation with exponential backoff to avoid thundering herd problems.

**Prohibited Behavior**: The system MUST NEVER overwrite state silently or ignore version conflicts. All state modifications MUST be version-aware and conflict-aware.

### Required Message Envelopes

The system SHALL use the following message envelope types for inter-service communication:

#### Task

The Task envelope SHALL contain:

- Task identifier and metadata
- Task specification (type, parameters, requirements)
- Dependencies and execution context
- Resource requirements and constraints
- Version information for state consistency

#### Result

The Result envelope SHALL contain:

- Task identifier (linking back to the originating task)
- Execution status (success, failure, partial)
- Output artifacts and data
- Error information (if applicable)
- Execution metadata (duration, resource usage, etc.)

#### ReviewDecision

The ReviewDecision envelope SHALL contain:

- Result identifier (linking to the Worker result)
- Decision (approved, rejected, requires_human_review)
- Validation details and rationale
- Governance checks performed
- Commit authorization (if approved)

These message envelopes ensure traceability, auditability, and proper coordination between Planner, Worker, and Judge components.

## 8. MCP Integration Constitution (Developer Tools vs Runtime Skills)

MCP (Model Context Protocol) SHALL serve as the **ONLY gateway** for external actions in Project Chimera. All interactions with external systems, platforms, and services MUST be mediated through MCP servers. This ensures isolation, testability, standardized capability discovery, and centralized governance.

### MCP as the Exclusive Gateway

**Hard Rule**: Core logic (Orchestrator, Workers, Judges) MUST NOT embed vendor-specific platform SDKs or make direct API calls to external services. All external actions SHALL be executed via MCP tool calls.

This rule applies to:

- Social media platform APIs (Twitter/X, Instagram, TikTok, etc.)
- Content generation services (image generators, video editors, etc.)
- Analytics and monitoring services
- Payment and commerce platforms
- Any third-party service or API

### Two Categories of MCP Tools

MCP tools are organized into two distinct categories based on their purpose and usage context:

#### A) Developer Tools (MCP)

Developer Tools are MCP servers that assist developers in building, testing, and maintaining the Project Chimera system. These tools operate in the development environment and are NOT used by the runtime agent system.

**Examples**:

- `git-mcp`: Git operations for version control
- `filesystem-mcp`: File system operations for development workflows
- `docker-mcp`: Container management for local development
- `database-mcp`: Database schema migrations and management tools

**Characteristics**:

- Used during development, testing, and CI/CD pipelines
- Not accessible to runtime Workers or agents
- May have elevated permissions for development tasks
- Typically run in development environments only

#### B) Runtime Tools (Agent Skills)

Runtime Tools (also called Agent Skills) are MCP servers used by the agent system during autonomous operation. These tools enable Workers to perform their assigned tasks and interact with external platforms.

**Examples**:

- Trend fetchers: Retrieve trending topics, hashtags, and content from social platforms
- Publishers: Post content to social media platforms
- Media generators: Create images, videos, and other media assets
- Analytics collectors: Gather performance metrics and engagement data
- Commerce tools: Handle payments, transactions, and wallet operations

**Characteristics**:

- Used by Workers during task execution
- Subject to governance, rate limiting, and approval workflows
- Must implement safety and audit hooks
- Run in production environments with restricted permissions

### MCP Layer Expectations

The MCP layer SHALL provide the following cross-cutting concerns:

#### Rate Limiting

MCP servers MUST implement rate limiting to prevent API quota exhaustion and ensure fair resource usage. Rate limits SHALL be:

- Configurable per tool and per platform
- Enforced at the MCP server level
- Logged and monitored for compliance

#### Logging

All MCP tool invocations MUST be logged with:

- Tool identifier and parameters
- Execution timestamp and duration
- Success/failure status
- Error details (if applicable)
- Request/response metadata

#### Audit

MCP servers SHALL provide audit trails for:

- All external actions attempted
- Approval/rejection decisions
- State changes and side effects
- Policy violations or exceptions

#### Dry-Run Hooks

MCP servers MUST support dry-run mode for:

- Testing and validation workflows
- Previewing actions without side effects
- Validating parameters before execution
- Training and development scenarios

These hooks enable safe testing and validation without executing real external actions.

### Integration Requirements

- **MCP Host Runtime**: The system SHALL use an MCP host runtime to execute MCP servers and manage tool invocations.
- **Tool Discovery**: Workers SHALL discover available tools through MCP's standardized capability discovery mechanism.
- **Error Handling**: MCP tool failures SHALL be handled gracefully with retry logic, fallback strategies, and error reporting.
- **Versioning**: MCP servers SHALL support versioning to enable backward compatibility and gradual migration.

This architecture ensures that external integrations are isolated, testable, and governed, while maintaining flexibility to add new capabilities through standardized MCP servers.

## 9. Data & State Constitution

Project Chimera SHALL use a multi-database architecture with clear separation of concerns for different types of data and state. This section defines what data lives where, state ownership rules, and tenant isolation requirements.

### Data Storage: What Lives Where

#### PostgreSQL: Transactional Truth

PostgreSQL SHALL store all **transactional truth**—the authoritative, persistent state that requires ACID guarantees and long-term retention. This includes:

- **Campaigns**: Campaign definitions, configurations, goals, and metadata.
- **Posts**: Published content, drafts, and content metadata.
- **Approvals**: Approval records, HITL decisions, and review history.
- **Audit Logs**: Comprehensive audit trails for all system actions, state changes, and governance decisions.
- **Budgets**: Budget allocations, spending records, and financial state.
- **Agent State**: Agent configurations, personas, and persistent agent state.
- **Policy Configurations**: Safety policies, governance rules, and HITL thresholds.
- **Transaction Records**: Financial transaction records and wallet state (as defined in Section 11).

PostgreSQL serves as the **single source of truth** for all persistent, transactional data.

#### Redis: Queues + Ephemeral/Short-Term State

Redis SHALL store:

- **Message Queues**: Task queues, review queues, and inter-service communication queues.
- **Ephemeral State**: Short-lived state that does not require persistence:
  - Task execution state (in-progress tasks)
  - Rate limiting counters
  - Cache entries for frequently accessed data
  - Session state and temporary locks
- **Distributed Locks**: OCC locks, concurrency control locks, and coordination primitives.

Redis data SHALL be considered ephemeral and may be lost during restarts. Critical state MUST NOT rely solely on Redis.

#### Weaviate: Semantic Memory and Retrieval

Weaviate SHALL store:

- **Semantic Memory**: Long-term memory embeddings for RAG (Retrieval-Augmented Generation) workflows.
- **Content Embeddings**: Vector embeddings of published content, drafts, and media assets.
- **Knowledge Base**: Semantic knowledge base for agent reasoning and context retrieval.
- **Similarity Search**: Enables semantic similarity search and retrieval for content discovery and context building.

Weaviate enables semantic understanding and retrieval but does not serve as transactional truth.

### State Ownership

#### Orchestrator Owns Canonical State

The Orchestrator SHALL be the **sole owner** of canonical state and the only service authorized to write to PostgreSQL. The Orchestrator:

- **Maintains Authoritative State**: Holds the canonical view of campaigns, budgets, policies, and workflow state.
- **Writes to PostgreSQL**: All persistent state writes SHALL go through the Orchestrator.
- **Coordinates State Changes**: Manages state transitions, versioning, and concurrency control.
- **Enforces State Consistency**: Ensures state consistency across the system through centralized coordination.

#### Workers Do Not Write Directly

Workers SHALL NOT write to PostgreSQL directly. Workers:

- **Submit Results**: Return execution results to the Orchestrator for review and commit.
- **No Direct Database Access**: MUST NOT have direct database connections or write permissions.
- **Stateless Operation**: Maintain no persistent state; all state operations go through the Orchestrator.

This ensures that all state changes go through proper governance routing (Worker → Judge → Orchestrator → Database) as defined in Section 10.

#### Platform Reads via Orchestrator APIs Only

The Platform SHALL read data exclusively through Orchestrator APIs. The Platform:

- **No Direct Database Access**: MUST NOT connect directly to PostgreSQL, Redis, or Weaviate.
- **API-Only Access**: All data access SHALL go through Orchestrator REST APIs or GraphQL endpoints.
- **Filtered Views**: Receives filtered, permission-aware views of data appropriate for human oversight.

This boundary ensures that the Platform cannot bypass governance or access data outside of approved workflows.

### Tenant Isolation Requirements

**Multi-Tenancy Support**: Project Chimera SHALL support multi-tenant operation where multiple agents, campaigns, or organizations operate within the same system instance.

**Data Layer Isolation**: Tenant isolation SHALL be enforced at the data layer:

#### Database-Level Isolation

- **Tenant Identifier**: All database records SHALL include a tenant identifier (tenant_id) as a mandatory field.
- **Row-Level Security**: Database queries SHALL filter by tenant_id to ensure data isolation.
- **Foreign Key Constraints**: Foreign key relationships SHALL respect tenant boundaries (no cross-tenant references).

#### Application-Level Isolation

- **Tenant Context**: All service requests SHALL include tenant context, and services SHALL validate tenant context before processing.
- **Query Filtering**: All database queries SHALL automatically include tenant_id filtering to prevent cross-tenant data access.
- **API Isolation**: Orchestrator APIs SHALL enforce tenant isolation, ensuring tenants can only access their own data.

#### Redis Isolation

- **Key Namespacing**: Redis keys SHALL be namespaced by tenant_id (e.g., `tenant:{tenant_id}:queue:task`).
- **Queue Isolation**: Task queues and message queues SHALL be isolated per tenant.

#### Weaviate Isolation

- **Collection Per Tenant**: Weaviate collections SHALL be scoped per tenant, or tenant_id SHALL be included in vector metadata for filtering.
- **Query Filtering**: All Weaviate queries SHALL include tenant filtering to prevent cross-tenant semantic search.

**Isolation Violations**: Any attempt to access data across tenant boundaries SHALL be:

- Detected and blocked
- Logged as a security event
- Reported to the Platform for investigation

This multi-layered isolation ensures that tenants operate in complete isolation, preventing data leakage and ensuring compliance with multi-tenancy requirements.

## 10. Safety, HITL, and Governance Constitution

Project Chimera SHALL implement comprehensive safety controls, Human-in-the-Loop (HITL) mechanisms, and governance policies to ensure responsible autonomous operation. This section defines the requirements for confidence scoring, HITL triggers, governance routing, and transparency rules.

### Confidence Scoring Requirement

**Worker Output Confidence**: All Worker outputs SHALL include a confidence score that indicates the Worker's assessment of output quality, accuracy, and compliance. Confidence scores SHALL:

- **Range**: Be expressed as a normalized value (e.g., 0.0 to 1.0, or 0% to 100%).
- **Basis**: Reflect the Worker's assessment of:
  - Output quality and completeness
  - Alignment with task requirements
  - Compliance with safety and policy guidelines
  - Risk assessment for potential side effects

- **Usage**: Be used by Judges to determine approval thresholds and HITL escalation requirements.

**Low Confidence Handling**: Outputs with confidence scores below configured thresholds SHALL automatically trigger additional review or HITL escalation, regardless of other validation criteria.

### Policy-Driven HITL Triggers

**Human-in-the-Loop Requirements**: The system SHALL implement policy-driven HITL triggers that require human review before execution. HITL triggers SHALL be activated for:

- **Sensitive Actions**: Publishing content, sending messages, executing transactions, or any action with potential brand, legal, or financial impact.
- **High-Risk Categories**: Content or actions related to politics, legal/financial claims, health/medical advice, or brand safety concerns.
- **Low Confidence Outputs**: Worker outputs with confidence scores below policy-defined thresholds.
- **Policy Violations**: Any output that violates safety policies, brand guidelines, or governance rules.
- **Budget Thresholds**: Transactions or spending operations that exceed configured approval thresholds.

**Sensitive-Action Overrides**: Certain sensitive actions SHALL always require HITL approval, regardless of confidence scores or other factors. These include:

- Publishing content to public-facing platforms
- Sending direct messages to users
- Executing financial transactions (as defined in Section 11)
- Making legal or regulatory claims
- Representing the brand in official communications

**HITL Workflow**: When HITL is triggered:

1. **Escalation**: The action is escalated to the Platform for human review.
2. **Human Review**: A human reviewer evaluates the proposed action, context, and rationale.
3. **Decision**: The human reviewer approves, rejects, or requests modifications.
4. **Execution**: Only approved actions proceed to execution; rejected actions are logged and reported.

### Governance Routing

**Standard Governance Flow**: All actions SHALL follow the governance routing pattern:

1. **Worker Proposes**: Workers generate outputs and propose actions based on task specifications.
2. **Judge Reviews**: Judges validate outputs against acceptance criteria, safety policies, and governance rules.
3. **Orchestrator Commits**: The Orchestrator commits approved results to persistent state (database).
4. **MCP Executes**: Where relevant, MCP tools execute external actions (publishing, messaging, transactions) based on committed state.

**Prohibited Shortcuts**: Actions MUST NOT bypass any step in this routing pattern. Workers MUST NOT execute external actions directly, and Judges MUST NOT commit state without Orchestrator coordination.

**Exception Handling**: Rejected actions SHALL be:

- Logged with rejection rationale
- Reported to the Platform for visibility
- Optionally returned to Workers for revision (if applicable)

### Transparency Rules for AI-Generated Content

**AI Content Disclosure**: When AI-generated content is published or shared, the system SHALL comply with transparency requirements:

- **Disclosure Requirements**: Content that is substantially AI-generated SHALL be disclosed as such, where required by platform policies or legal regulations.
- **Attribution**: AI-generated content SHALL include appropriate attribution or disclosure markers as specified by platform requirements and legal obligations.
- **Traceability**: The system SHALL maintain records of AI-generated content, including:
  - Generation timestamp and method
  - Original prompts and context
  - Modifications made during review or editing
  - Publication details and platforms

**Platform-Specific Rules**: Different platforms may have different disclosure requirements. The system SHALL:

- Track platform-specific disclosure policies
- Apply appropriate disclosure rules per platform
- Maintain compliance with evolving platform requirements

### Safety Cannot Be Bypassed

**Non-Negotiable Rule**: Safety and governance rules MUST NOT be bypassed, overridden, or compromised for any reason, including:

- **Persona Goals**: Agent personas, brand voice, or creative objectives MUST NOT override safety policies or governance rules.
- **Optimization Goals**: Performance optimization, engagement metrics, or business objectives MUST NOT compromise safety controls.
- **Efficiency Concerns**: Speed, throughput, or resource efficiency MUST NOT justify bypassing safety checks or HITL requirements.
- **User Requests**: User requests or preferences MUST NOT override safety policies or governance rules.

**Enforcement**: The system SHALL enforce safety and governance rules at multiple layers:

- **Worker Layer**: Workers SHALL apply safety checks during output generation.
- **Judge Layer**: Judges SHALL validate all outputs against safety and governance policies.
- **Orchestrator Layer**: The Orchestrator SHALL enforce governance routing and prevent bypass attempts.
- **MCP Layer**: MCP tools SHALL implement safety hooks and validation before executing external actions.

**Violation Handling**: Any attempt to bypass safety or governance rules SHALL be:

- Detected and blocked
- Logged as a security event
- Reported to the Platform for investigation
- Escalated for human review if necessary

This multi-layered enforcement ensures that safety and governance cannot be compromised, regardless of system goals or operational pressures.

## 11. Agentic Commerce & Wallet Security Constitution

When agentic commerce functionality is enabled, Project Chimera SHALL implement strict security and governance controls for wallet operations and financial transactions. This section defines the requirements for wallet management, transaction approval, and security practices.

### Non-Custodial Wallets

**Per-Agent Wallet Model**: When agentic commerce is enabled, each agent SHALL have its own non-custodial wallet. Wallets SHALL be:

- **Non-Custodial**: Private keys are controlled by the agent system, not held by third-party custodians.
- **Isolated**: Each agent's wallet is independent and isolated from other agents' wallets.
- **Managed via Coinbase AgentKit**: Wallet operations SHALL use Coinbase AgentKit as specified in Section 4 (Technology Stack Constitution).

This model ensures that each agent has independent financial control and accountability.

### CFO Judge Gate

**Transaction Approval Requirement**: Every transaction request MUST be reviewed and approved by a CFO Judge before execution. The CFO Judge SHALL:

- **Review Transaction Details**: Validate transaction amount, recipient, purpose, and context.
- **Check Budget Constraints**: Verify that the transaction does not exceed available budget or violate spending policies.
- **Apply Governance Rules**: Enforce commerce policies, rate limits, and approval workflows.
- **Make Approval Decision**: Approve, reject, or escalate to human review based on risk assessment.

**Prohibited Behavior**: Transactions MUST NEVER be executed without CFO Judge approval. Workers MUST NOT bypass the Judge gate or execute transactions directly.

### Balance Check Requirement

**Pre-Transaction Balance Check**: The `get_balance` operation MUST precede any cost-incurring workflow. Before initiating any transaction or spending operation:

1. **Check Balance**: Call `get_balance` to retrieve the current wallet balance.
2. **Validate Sufficiency**: Verify that the balance is sufficient for the intended transaction.
3. **Proceed or Abort**: Only proceed with the transaction if balance is sufficient; otherwise abort or escalate.

This requirement prevents insufficient funds errors and ensures proper financial planning before committing to transactions.

### Secrets Management

**Hard Security Rules**: Wallet private keys and other sensitive credentials SHALL be managed according to the following rules:

1. **Never Stored in Repository**: Private keys, API keys, and other secrets MUST NOT be stored in the repository (no hardcoded secrets in code, config files, or documentation).

2. **Never Logged**: Secrets MUST NOT be logged in any form (no secrets in application logs, debug output, error messages, or audit trails). Logging systems SHALL mask or redact any secret values that might be accidentally included.

3. **Injected at Runtime**: Secrets SHALL be injected at runtime through:
   - Secrets manager service (e.g., AWS Secrets Manager, HashiCorp Vault, Kubernetes secrets)
   - Environment variables (for local development only, never committed)
   - Secure configuration services

4. **Access Control**: Secrets SHALL be accessible only to authorized services and components that require them for legitimate operations.

These rules ensure that sensitive credentials are protected throughout the system lifecycle and reduce the risk of credential exposure.

### Required Audit Trails

**Transaction Audit Requirements**: All transactions SHALL maintain comprehensive audit trails with the following components:

#### Internal Audit Trail

The internal audit trail SHALL record:

- **Transaction Request**: Timestamp, agent identifier, transaction type, amount, recipient, purpose, and context.
- **Balance Check**: Pre-transaction balance retrieved via `get_balance` operation.
- **CFO Judge Review**: Review timestamp, judge identifier, decision (approved/rejected/escalated), and rationale.
- **Execution Status**: Transaction execution timestamp, success/failure status, error details (if applicable).
- **Post-Transaction State**: Updated balance and wallet state after transaction completion.

#### On-Chain Reference

The audit trail SHALL include:

- **Transaction Hash**: Blockchain transaction hash or on-chain transaction identifier.
- **Block Information**: Block number, block timestamp, and confirmation status.
- **On-Chain Verification**: Link to blockchain explorer or on-chain verification endpoint for transaction validation.

#### Audit Trail Storage

- **Persistent Storage**: Audit trails SHALL be stored in PostgreSQL for long-term retention and queryability.
- **Immutable Records**: Audit trail records MUST NOT be modified or deleted after creation (append-only).
- **Queryability**: Audit trails SHALL support queries by agent, transaction type, time range, and on-chain reference.

These audit trails enable financial accountability, compliance verification, and forensic analysis of all commerce operations.

## 12. Performance, Scalability, Reliability Constitution

Project Chimera SHALL meet defined performance, scalability, and reliability requirements to support autonomous operation at fleet scale. This section defines horizontal scaling of Workers, Orchestrator responsiveness, queue backpressure rules, reliability targets, and graceful degradation expectations.

### Horizontal Autoscaling of Workers

**Worker Scaling**: Workers SHALL scale horizontally based on workload demand. The system SHALL:

- **Autoscaling**: Automatically scale the number of Worker instances up or down based on:
  - Queue depth (task queue length)
  - Processing latency and throughput metrics
  - Resource utilization (CPU, memory) within defined bounds
- **Scale-Out**: Add Worker instances when queue depth exceeds configured thresholds or latency degrades.
- **Scale-In**: Reduce Worker instances when load decreases, while preserving minimum capacity for baseline responsiveness.
- **Bounded Scaling**: Enforce minimum and maximum Worker counts to prevent runaway scaling and control cost.

**Orchestration**: Autoscaling SHALL be orchestrated via Kubernetes Horizontal Pod Autoscaler (HPA) or equivalent, as specified in Section 3 (Architecture Constitution).

### Orchestrator Responsiveness

**High-Concurrency Requirement**: The Orchestrator MUST remain responsive under high concurrency. The Orchestrator SHALL:

- **Latency Targets**: Meet defined latency targets for API requests (e.g., p95 latency within acceptable bounds) even under elevated load.
- **Non-Blocking Design**: Use non-blocking I/O and asynchronous processing where appropriate to avoid head-of-line blocking.
- **Resource Management**: Limit in-flight work (connection pools, request concurrency) to prevent overload and maintain stability.
- **Health and Readiness**: Expose health and readiness endpoints that reflect actual ability to serve traffic; load balancers SHALL use these for routing decisions.

**Degradation**: Under extreme load, the Orchestrator MAY degrade by rejecting or rate-limiting non-critical requests before compromising core API availability. Critical operations (e.g., task submission, state commits, HITL escalation) SHALL retain priority.

### Backpressure Rules for Queues

**Queue Management**: Message queues (Redis-backed task queues, review queues) SHALL implement backpressure to prevent unbounded growth and cascading failure. The system SHALL:

- **Queue Depth Limits**: Define maximum queue depth per queue type. When limits are approached or exceeded:
  - New task submissions MAY be rejected or deferred with a clear error or retry-after signal.
  - Producers (e.g., Orchestrator) SHALL apply backpressure rather than continuing to enqueue without bound.
- **Consumer Backpressure**: Workers SHALL consume at a sustainable rate; the system SHALL not require Workers to drain queues faster than they can process.
- **Dead Letter Handling**: Failed or poison messages SHALL be moved to dead-letter queues or equivalent after configurable retries, so they do not block the main queue.
- **Monitoring**: Queue depth, consumer lag, and backpressure events SHALL be monitored and alerted to support operational response.

**Prohibited**: Queues MUST NOT grow unbounded. Unbounded queue growth is a reliability anti-pattern and SHALL be prevented by backpressure and limits.

### Reliability Targets and Graceful Degradation

**Reliability Targets**: The system SHALL target:

- **Availability**: Orchestrator and Platform APIs SHALL target high availability (e.g., 99.5% or better uptime for critical paths, excluding planned maintenance).
- **Durability**: Data committed to PostgreSQL SHALL be durable; no silent data loss.
- **Task Processing**: Task processing SHALL be at-least-once or exactly-once (with idempotency) as specified per task type; no silent task loss under normal operation.

**Graceful Degradation**: When components fail or are overloaded, the system SHALL degrade gracefully:

- **Orchestrator Unavailable**: Platform SHALL display clear status and avoid silent failures; task submission SHALL fail with a retriable or user-actionable error.
- **Worker Unavailable**: Pending tasks remain in the queue; no task loss. When Workers recover, processing resumes.
- **Database or Redis Unavailable**: The system SHALL fail closed (reject writes) rather than fail open (lose data or consistency). Reads MAY be served from cache where safe and explicitly designed.

**Recovery**: After outages, the system SHALL recover without manual data repair where possible (e.g., replay from queues, idempotent retries).

### Platform Usability During Worker Backlogs

**Requirement**: The Platform MUST remain usable even during Worker backlogs. When task queues are deep or Workers are overloaded:

- **Platform Responsiveness**: Platform UI and Orchestrator APIs consumed by the Platform SHALL remain responsive. Human users SHALL be able to:
  - View dashboard and current state
  - Submit configuration changes, policy updates, and HITL decisions
  - Monitor queue depth and system health
  - Cancel or reprioritize work where supported
- **No Coupling to Queue Depth**: Platform request latency and availability SHALL NOT degrade proportionally to task queue depth. Orchestrator SHALL isolate Platform-serving paths from heavy task-processing load where possible.
- **User Feedback**: When backlogs exist, the Platform SHALL surface clear indicators (e.g., "High task backlog; processing may be delayed") so users understand system state without assuming failure.

This ensures that human oversight and intervention remain possible when the system is under load, supporting the "manage by exception" model defined in Section 1.

## 13. Multi-Tenancy & Isolation Constitution

Project Chimera SHALL enforce strict multi-tenancy and isolation so that tenants (agents, campaigns, or organizations) operate in complete isolation with no data leakage or cross-tenant access. This section defines tenant isolation boundaries, Weaviate retrieval rules, secrets isolation, and Platform tenant scoping.

### Tenant Isolation Boundaries

**Isolation Domains**: Tenant isolation SHALL be enforced across the following boundaries:

#### Data

- **PostgreSQL**: All transactional data SHALL be scoped by tenant_id. Every table that holds tenant-scoped data MUST include tenant_id; all queries MUST filter by tenant_id. Cross-tenant queries are prohibited. (See Section 9 for data-layer isolation details.)
- **Redis**: All queue and ephemeral state SHALL be namespaced by tenant_id (e.g., `tenant:{tenant_id}:queue:task`). No shared queues or keys across tenants.
- **Data Access**: Services SHALL resolve tenant context (e.g., from auth token or request header) before any data access and MUST NOT return or expose data belonging to another tenant.

#### Memory (Semantic / Weaviate)

- **Tenant-Scoped Memory**: Semantic memory and vector embeddings in Weaviate SHALL be stored and retrieved only within a single tenant's scope.
- **No Cross-Tenant Retrieval**: Weaviate MUST NOT return results from another tenant. All semantic search and retrieval operations SHALL include tenant filtering (e.g., tenant_id in metadata or tenant-scoped collections). Cross-tenant retrieval is prohibited.
- **Isolation Mechanism**: Implement either per-tenant Weaviate collections or mandatory tenant_id filters on every query so that results are strictly limited to the requesting tenant.

#### Wallets

- **Per-Tenant Wallets**: When agentic commerce is enabled, wallets SHALL be scoped per tenant (or per agent within a tenant). One tenant's wallet MUST NOT be used for another tenant's transactions.
- **Wallet Access**: Wallet credentials and operations SHALL be accessible only within the tenant context. No shared wallet access across tenants.

#### Configs

- **Tenant-Scoped Configuration**: Campaign configs, safety policies, governance rules, and agent configurations SHALL be stored and retrieved per tenant. Configurations MUST NOT be shared or visible across tenants.
- **Default and Overrides**: Tenant-specific overrides SHALL not affect other tenants; global defaults (if any) apply only where explicitly designed and SHALL not leak tenant-specific data.

### No Cross-Tenant Retrieval in Weaviate

**Rule**: There SHALL be no cross-tenant retrieval in Weaviate. Specifically:

- **Queries**: Every Weaviate query (vector search, hybrid search, or filter) SHALL include a tenant constraint so that only documents/vectors belonging to the current tenant can be returned.
- **Indexing**: When writing to Weaviate, tenant_id SHALL be stored (e.g., as a property or in metadata) and used for filtering. Documents MUST NOT be queryable across tenants.
- **Validation**: Query builders and API layers SHALL validate that tenant context is present and apply tenant filters; missing or invalid tenant context SHALL result in request rejection.

This prevents one tenant from accessing another tenant's semantic memory or content embeddings.

### No Shared Secrets Across Tenants

**Rule**: Secrets SHALL NOT be shared across tenants. Specifically:

- **Per-Tenant Secrets**: API keys, wallet keys, OAuth tokens, and other secrets SHALL be stored and retrieved per tenant (e.g., in a secrets manager with tenant-scoped paths or keys).
- **Injection**: At runtime, secrets SHALL be injected only into the tenant context that owns them. A Worker or Orchestrator handling Tenant A MUST NOT receive or use Tenant B's secrets.
- **Access Control**: Secrets manager and configuration services SHALL enforce tenant-scoped access so that one tenant cannot read another tenant's secrets.

Violations (e.g., using one tenant's API key for another tenant's operations) are security incidents and SHALL be logged, blocked, and reported.

### Platform Tenant Scopes via Orchestrator APIs and Auth

**Requirement**: The Platform MUST respect tenant scopes. All Platform data access and actions SHALL be tenant-scoped via Orchestrator APIs and authentication:

- **Authentication**: Platform users SHALL authenticate in a tenant context (e.g., user belongs to one or more tenants; session or token carries tenant scope). Multi-tenant users (e.g., admins) SHALL explicitly select or be restricted to a tenant when performing actions.
- **Orchestrator APIs**: The Platform SHALL call only Orchestrator APIs. The Orchestrator SHALL derive tenant from the authenticated request (token, header, or session) and enforce tenant isolation on every API call. The Platform MUST NOT send tenant identifiers that the user is not authorized to access.
- **Scoped Responses**: Orchestrator responses to the Platform SHALL contain only data for the requesting tenant(s) the user is authorized to see. No cross-tenant data in responses.
- **UI Scoping**: Platform UI SHALL display data and actions only for the current tenant context. Tenant switcher (if any) SHALL switch context and refetch data via Orchestrator; no client-side mixing of tenant data.

This ensures that human operators see and act only within their authorized tenant scope, with enforcement at the API and auth layer rather than solely in the UI.

## 14. Observability & Auditability Constitution

Project Chimera SHALL implement required telemetry, structured logging, metrics, and audit trails to support operations, debugging, compliance, and traceability. This section defines required telemetry, audit logs, traceability rules, and Platform observability constraints.

### Required Telemetry

#### Structured Logs with Correlation IDs

All backend services (Orchestrator, Workers, Judges, MCP servers) SHALL emit **structured logs** (e.g., JSON) that include **correlation IDs** so that related events can be traced across services. At minimum, logs SHALL include:

- **task_id**: Identifier of the task being processed (when applicable).
- **campaign_id**: Identifier of the campaign context (when applicable).
- **agent_id**: Identifier of the agent context (when applicable).
- **tenant_id**: Tenant context for multi-tenant isolation and filtering.
- **request_id** or **trace_id**: Unique identifier for the request or trace span, propagated across service boundaries.

Additional context (e.g., user_id, judge_decision, tool_name) SHALL be included where relevant. Logs MUST NOT contain secrets (see Section 11).

#### Metrics

The system SHALL expose and collect the following metrics (or equivalent) to support operations and cost control:

- **Queue Depth**: Current depth of task queues, review queues, and other critical queues (per tenant where applicable).
- **Tool Latency**: Latency of MCP tool invocations (e.g., p50, p95, p99) per tool and per tenant.
- **Errors**: Error counts by type, service, and tenant (e.g., task failures, validation failures, timeout errors).
- **Costs**: Cost-related metrics (e.g., token usage, API call costs, transaction amounts) where applicable and without exposing secrets.
- **HITL Events**: Counts and latency of HITL escalations, approvals, and rejections.

Metrics SHALL be queryable and aggregatable (e.g., via Prometheus, OpenTelemetry, or equivalent) and SHALL support alerting on thresholds.

#### Audit Logs

**Audit logs** SHALL be maintained for governance-sensitive and financial actions. At minimum, audit logs SHALL cover:

- **Approvals**: Every Judge approval or rejection (what was approved/rejected, by whom or which component, when, rationale).
- **Publishes**: Every content publish or post (what was published, where, when, campaign/agent context).
- **Financial Actions**: Every transaction request, CFO Judge decision, and execution (as defined in Section 11), including internal and on-chain references.

Audit log entries SHALL be immutable (append-only), include timestamp and actor (user or system component), and be stored in PostgreSQL for long-term retention and queryability.

#### Traceability: UI Action to Orchestrator Request ID

**Requirement**: Every UI action that triggers an Orchestrator API call SHALL be traceable to a single Orchestrator request ID. Specifically:

- **Request ID**: The Orchestrator SHALL assign a unique request_id to each API request and return it in the response (e.g., header or body).
- **Platform Propagation**: The Platform SHALL capture and store (e.g., in UI state or logs) the request_id for each user-initiated action that resulted in an Orchestrator call.
- **Correlation**: Support and debugging workflows SHALL be able to map "user did X in the UI at time T" to the corresponding Orchestrator request_id and thus to backend logs, metrics, and audit entries.

This enables end-to-end traceability from user action to backend processing.

### Platform Observability

**Minimal Client Logs Allowed**: The Platform (client/frontend) MAY emit minimal client-side logs (e.g., errors, navigation, or request IDs) for debugging and support, provided that:

- Logs MUST NOT contain secrets or PII beyond what is necessary for support (e.g., request_id, error codes).
- Log volume SHALL be kept minimal; no verbose or debug logging in production by default.

**No Test Tooling**: The Platform MUST NOT include test tooling in production builds. Specifically:

- No test runners, test utilities, or test-only code paths in production.
- No E2E or integration test frameworks bundled with the Platform (consistent with Prime Directive #6 and Section 4: Platform has no tests).
- Observability in the Platform is limited to minimal logs and any instrumentation that reports to backend or analytics; no separate test infrastructure or test harnesses in the client.

This keeps the Platform surface small and avoids confusion between observability and testing, while preserving the prohibition on frontend tests.

## 15. Build, Run, Test & Docker Constitution

Project Chimera SHALL use Docker for containerization and a root-level Makefile for build, run, and test automation. This section defines the hard requirement for per-service containers, infrastructure via Docker Compose, the Make targets contract, and the CRITICAL test policy.

### Hard Requirement: Per-Service Docker Containers

**Each project/service MUST have its own Docker container/image.** The following services SHALL have dedicated Dockerfiles and images:

- **apps/platform**: Next.js application. SHALL have its own Dockerfile and image (e.g., `apps/platform/Dockerfile`).
- **services/orchestrator**: FastAPI application. SHALL have its own Dockerfile and image (e.g., `services/orchestrator/Dockerfile`).
- **services/worker**: Celery worker. SHALL have its own Dockerfile and image (e.g., `services/worker/Dockerfile`).
- **MCP servers**: Any MCP server that is used outside local stdio (e.g., run as a separate process in development or production) SHALL run in its own container. MCP servers invoked only via local stdio in a single process MAY share a container with the invoking service where explicitly designed; otherwise they SHALL have separate containers.

No service SHALL be deployed without a corresponding container image. This aligns with Section 3 (Architecture Constitution) and Section 5 (Repository & Folder Structure Constitution).

### Infrastructure: Docker Compose

**Infrastructure services (PostgreSQL, Redis, Weaviate) MUST be runnable via Docker Compose.** The repository SHALL provide a Docker Compose configuration (e.g., `docker-compose.yml` or `compose.yaml`) that:

- Starts PostgreSQL, Redis, and Weaviate with versions and configurations suitable for local development and CI.
- Exposes ports and volumes as needed for Orchestrator, Workers, and Platform to connect.
- MAY include optional services (e.g., Celery beat, MCP servers) where appropriate.

Developers and CI SHALL be able to run `make up` (or equivalent) to bring up infrastructure and optionally application services, and `make down` to tear them down.

### Make Targets Contract

The repository root SHALL contain a **Makefile** that implements the following targets. Targets marked **MUST exist** are required; others are optional or recommended as indicated.

#### Required (MUST exist)

- **make setup**: One-time or idempotent setup (e.g., install dependencies, create env files from templates, pre-commit hooks). SHALL be documented so new contributors can run it to get ready to develop.
- **make up**: Start infrastructure and/or application services (e.g., via Docker Compose). SHALL bring up at least PostgreSQL, Redis, and Weaviate when used for full local stack.
- **make down**: Stop and remove containers/volumes started by `make up`. SHALL cleanly tear down the same resources.
- **make run-platform**: Run the Platform (Next.js) in a mode suitable for local development (e.g., dev server or container). SHALL be invocable after setup.
- **make run-orchestrator**: Run the Orchestrator (FastAPI) in a mode suitable for local development. SHALL be invocable after setup.
- **make run-worker**: Run the Worker (Celery worker) in a mode suitable for local development. SHALL be invocable after setup.
- **make test**: Run the **non-frontend** test suite (orchestrator, worker, skills, MCP servers, utilities). SHALL NOT run or install frontend test runners. See CRITICAL test policy below.

#### Optional

- **make test-local**: Optional target for running tests in a local or sandbox environment (e.g., with local services). If present, it SHALL NOT run frontend tests.
- **make spec-check**: Optional target for validating specs or constitution (e.g., linting spec files, checking required files). If present, it SHALL be documented.

#### Recommended

- **make lint**: Recommended. Run linters for non-frontend code (orchestrator, worker, skills, etc.). SHALL NOT run frontend linters that depend on frontend test tooling.
- **make format**: Recommended. Run formatters for non-frontend code. SHALL NOT install or depend on frontend test tooling.

Implementations MAY add more targets (e.g., `make build`, `make push`, `make migrate`) as long as the required ones exist and the test policy is respected.

### CRITICAL Test Policy

**make test** is the canonical entrypoint for running tests in the repository. The following rules are **non-negotiable**:

1. **make test MUST run non-frontend tests.** It SHALL execute tests for:
   - services/orchestrator
   - services/worker
   - skills
   - MCP servers (if they have tests)
   - Any other non-frontend components that have tests (utilities, shared libraries, etc.)

2. **make test MUST NOT run or install frontend test runners.** It SHALL NOT:
   - Invoke Jest, Vitest, Playwright, Cypress, or any other frontend test runner.
   - Install dependencies or scripts whose primary purpose is frontend testing.
   - Run tests under `apps/platform` (the Platform has no tests per Prime Directive #6 and Section 4).

3. **Frontend exclusion is explicit.** The Makefile and any test orchestration SHALL exclude `apps/platform` (and any other frontend app directories) from the test discovery and execution path. Accidentally running frontend tests via `make test` is a violation of this constitution.

This policy ensures that the repository has a single, consistent way to run the allowed test suite (non-frontend only) and that the Platform remains free of test tooling as required elsewhere in this constitution.

## 16. Spec Kit Blueprint Constitution (specs/ required files)

Project Chimera SHALL maintain a **Spec Kit** under the `specs/` directory as the source of truth for implementation details. This section defines the required files under `specs/`, the relationship between specs and code, and the rule that every Platform API endpoint MUST be defined in the technical spec.

### Required Files Under specs/

The following files SHALL exist under `specs/` (see Section 5 for repository structure):

#### Mandatory

- **specs/\_meta.md**: Metadata and index for the spec kit (e.g., version of the spec kit, last updated, list of spec documents, conventions used). SHALL be the entry point for navigating specs.

- **specs/functional.md**: Functional specifications—user-facing capabilities, user stories, acceptance criteria, and feature requirements. SHALL describe _what_ the system does from a product and user perspective.

- **specs/technical.md**: Technical specifications. SHALL include:
  - **API contracts**: Request/response shapes, HTTP methods, paths, and status codes for Orchestrator APIs (and other service APIs where relevant).
  - **DB schema / ERD**: Database schema, entity-relationship description, and key tables/columns. SHALL align with Section 9 (Data & State Constitution) and the actual PostgreSQL usage.

#### Optional

- **specs/openclaw_integration.md**: Optional. When OpenClaw or similar integrations exist, this file MAY describe integration points, contracts, and constraints. If present, it SHALL be referenced from \_meta.md.

Additional files (e.g., per-feature specs under `specs/features/`) MAY exist as long as the mandatory files exist and are kept in sync.

### Specs Are the Source of Truth

**Specs are the source of truth for implementation details.** Implementation (code, APIs, schema) SHALL be derived from and traceable to the specs. When specs and code diverge, the specs define the intended design; code SHALL be updated to match, or the specs SHALL be updated through the normal change process (and reflected in \_meta.md / versioning as appropriate).

### No Code Changes Without Spec Alignment

**No code changes SHALL be made without spec alignment.** Specifically:

- **New behavior**: New features, API endpoints, or schema changes SHALL be specified in the appropriate spec (functional.md for behavior, technical.md for API and DB) before or as part of implementation.
- **Changes**: Changes to existing behavior or contracts SHALL be reflected in the specs. Code changes that alter observable behavior or contracts without a corresponding spec update are not permitted.
- **Refactors**: Purely internal refactors that do not change APIs, schema, or user-visible behavior MAY be implemented without spec changes, but any change to contracts or behavior SHALL have spec coverage.

This reinforces Prime Directive #2: "NEVER generate code without checking specs/ first."

### Every Platform API Endpoint in specs/technical.md

**Rule**: Every API endpoint used by the Platform MUST be defined in **specs/technical.md**.

- **Coverage**: The Orchestrator (and any other service) APIs that the Platform calls SHALL be fully documented in technical.md—path, method, request/response shape, auth, and semantics.
- **Single source**: The Platform SHALL not call endpoints that are not documented in technical.md. Adding a new endpoint used by the Platform SHALL require updating technical.md first (or in the same change).
- **Consistency**: technical.md SHALL be the authoritative reference for API consumers (including the Platform). Discrepancies between technical.md and implementation SHALL be treated as defects (either in code or in the spec) and resolved.

## This ensures that the Platform’s integration with the Orchestrator is fully specified and auditable in one place.

---

**Version**: 2.5.0 | **Ratified**: 2026-02-05 | **Last Amended**: 2026-02-05
