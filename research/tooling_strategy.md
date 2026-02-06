## Developer MCP Tooling Strategy for Cursor

### 1. Purpose and Guiding Principles

The purpose of Developer MCP tooling in Cursor for Project Chimera is to provide **safe, repeatable, and governed access** to external capabilities that support:

- **Development workflows**: editing, searching, refactoring, code review, and repository operations.
- **Repository and environment introspection**: reading files, inspecting Git history, and understanding project structure.
- **Operational support**: running commands and composing multiple tools when working on the codebase.

Guiding principles:

- **Developer tools only**: MCP servers configured in Cursor are for **developer workflows**, not for runtime Planner/Worker/Judge behavior.
- **Governed capabilities**: Each MCP server has an explicit allow/deny list of usage patterns aligned with the Project Chimera constitution.
- **Least privilege**: Tools are configured with the minimum scope needed to accomplish development tasks.
- **Durability over convenience**: Configuration and conventions should remain valid even as specific implementations evolve.
- **Traceability of changes**: Developer MCP usage should support clear mapping from change requests (issues/specs) to code changes, not bypass the SDD workflow.

> Note: The `tenxfeedbackanalytics` entry in `.cursor/mcp.json` is **logging/analytics‑only** and is **out of scope** for this developer tooling strategy.

---

### 2. Developer MCP Servers in Use

The following MCP servers are treated as **developer tooling** inside Cursor for this repository:

- `github` – docker‑based GitHub MCP server (token from `.env`).
- `filesystem` – Node‑based filesystem server rooted at the workspace.
- `git` – Python‑based Git tools via `uvx mcp-server-git`.
- `docker` – Docker MCP gateway for container and process orchestration.

Each server is documented below with purpose, configuration approach, and governance.

---

### 3. Server Details and Governance

#### 3.1 `github` – GitHub MCP Server

- **Purpose**
  - Interact with GitHub issues, pull requests, branches, commits, and repository metadata as part of the development workflow.
  - Support spec‑driven development by tying changes in `specs/` and `services/` to GitHub issues/PRs.

- **Configuration approach (Cursor)**
  - Defined in `.cursor/mcp.json` as:
    - `command: docker`
    - Arguments run the official `ghcr.io/github/github-mcp-server` image.
    - Authentication via `GITHUB_PERSONAL_ACCESS_TOKEN` provided from the workspace `.env` file.
  - Cursor invokes this server when GitHub‑related MCP tools are used in the IDE.

- **Allowed capabilities**
  - Reading repository metadata: branches, commits, files (via GitHub APIs).
  - Listing and inspecting issues, pull requests, and discussions.
  - Creating or updating issues and pull requests **when explicitly requested** in a spec or by the developer.
  - Requesting automated reviews or checks consistent with the project’s CI/CD policy.

- **Disallowed capabilities / governance rules**
  - No destructive operations without explicit human confirmation (e.g. force pushes, branch deletions).
  - No modification of repository or organization‑wide settings (e.g. branch protection rules) via MCP.
  - No use of GitHub MCP as a runtime execution channel for Planner/Worker/Judge; it is strictly a developer helper.
  - All changes initiated via `github` MCP must be traceable to either:
    - A spec change in `specs/`.
    - A documented issue or PR.

---

#### 3.2 `filesystem` – Filesystem MCP Server

- **Purpose**
  - Provide read‑heavy access to the workspace file tree to support navigation, search, and understanding of the codebase from within Cursor.
  - Enable lightweight edits when appropriate while still deferring to the repository’s spec‑first and test policies.

- **Configuration approach (Cursor)**
  - Defined in `.cursor/mcp.json` as:
    - `command: npx`
    - Args: `@modelcontextprotocol/server-filesystem` pointing at `${workspaceFolder}`.
  - Rooted at the repository workspace; it should not be configured to escape that root.

- **Allowed capabilities**
  - Reading files under the workspace (code, specs, docs, configuration) for understanding and refactoring.
  - Searching within the workspace tree.
  - Suggesting or applying edits that are consistent with:
    - The Spec Kit (`specs/`).
    - The Constitution (`constitution.md`).
    - The non‑frontend testing policy.

- **Disallowed capabilities / governance rules**
  - No arbitrary access outside the workspace root.
  - No storage of secrets or credentials in the repository via filesystem edits.
  - No use as a runtime persistence layer for Planner, Worker, or Judge (runtime state belongs in services and their data stores, not in MCP‑initiated ad‑hoc files).

---

#### 3.3 `git` – Git MCP Server

- **Purpose**
  - Interact with the local Git repository to inspect status, diffs, branches, and history in a structured way.
  - Support structured workflows such as “generate a diff for review” or “summarize recent commits” inside Cursor.

- **Configuration approach (Cursor)**
  - Defined in `.cursor/mcp.json` as:
    - `command: uvx`
    - Args: `mcp-server-git`.
  - Runs against the current workspace’s Git repository.

- **Allowed capabilities**
  - Reading Git status, diffs, and logs.
  - Proposing branch names and commit messages aligned with Spec Kit conventions (e.g. feature numbers and short names).
  - Creating commits and branches when explicitly instructed by the developer and consistent with the repository’s branching strategy.

- **Disallowed capabilities / governance rules**
  - No rewriting of shared history (e.g. `git push --force`, interactive rebases on shared branches) via MCP unless a human explicitly directs it and understands the impact.
  - No modification of Git configuration that changes identity, signing, or remote URLs.
  - No use by runtime agents; only human‑driven operations in the IDE.

---

#### 3.4 `docker` – Docker MCP Gateway

- **Purpose**
  - Provide controlled access to Docker‑based operations that support development and local orchestration (e.g. starting services, containers for tests, or auxiliary tooling).

- **Configuration approach (Cursor)**
  - Defined in `.cursor/mcp.json` as:
    - `command: docker`
    - Args: `mcp gateway run` (Docker MCP gateway).
  - The gateway mediates container operations requested through MCP tools.

- **Allowed capabilities**
  - Starting, stopping, and inspecting containers relevant to Project Chimera’s development environment (e.g. database, Redis, vector store, orchestrator, worker, platform containers).
  - Running short‑lived containers for tooling (linters, formatters, spec checkers) when aligned with the repository’s Makefile and infra conventions.

- **Disallowed capabilities / governance rules**
  - No arbitrary container operations that could exfiltrate secrets or access unrelated infrastructure.
  - No long‑running production workloads started from within Cursor; production is managed by the standard deployment pipeline, not MCP.
  - No use of Docker MCP as an alternative runtime control plane for Planner/Worker/Judge; runtime orchestration must follow the infra and services architecture, not IDE‑driven commands.

---

### 4. Separation Rule: Developer MCP vs Runtime Skills

To preserve clear boundaries and follow the Project Chimera constitution:

- **Developer MCP tools are not runtime skills.**
  - `github`, `filesystem`, `git`, and `docker` MCP servers are **for developers in Cursor only**.
  - They MUST NOT be used by runtime Planner, Worker, or Judge services to perform business operations.

- **Runtime agents interact via `skills/` contracts only.**
  - All runtime external actions (social posting, media generation, search, commerce, etc.) MUST be implemented as skills and MCP servers owned by the runtime stack (e.g. under `skills/` or dedicated services), with their own governance rules.
  - Runtime skills MUST NOT depend on the IDE’s developer MCP configuration; they have separate deployment, configuration, and secrets management.

- **No hidden control channels.**
  - Planner, Worker, and Judge MUST NOT rely on Cursor or Developer MCP servers as control planes.
  - Any action that affects production state MUST flow through the orchestrator, queues, skills, Judges, and data stores defined in the architecture and specs, not through ad‑hoc developer tooling.

This separation ensures that developer productivity tooling does not become an implicit part of the production runtime and that governance and safety guarantees remain enforceable and auditable.
