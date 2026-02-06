## Project Chimera – OpenClaw‑Style Integration Specification

This document describes how Project Chimera behaves as a **protocol participant** in an external agent network (e.g. OpenClaw). It focuses on:

- Capability advertisement
- Identity declaration
- Governance and safety signaling
- Task delegation and result reporting

Where upstream protocol details are not yet fixed, assumptions are explicitly marked.

---

### 1. Role in the External Network

Chimera appears to the network as an **influencer‑oriented agent organization** rather than a single agent. Its responsibilities in the network are:

- Accepting influencer‑related tasks that it can map into its internal Planner–Worker–Judge model.
- Advertising governance posture, safety constraints, and supported capabilities.
- Reporting availability and health so that peers can make informed routing decisions.
- Returning structured results and explanations for delegated work.

Chimera **does not**:

- Expose its internal Planner, Worker, or Judge services directly.
- Accept requests that require bypassing its internal governance (e.g. “post immediately, no review”).
- Act as a general‑purpose execution substrate for arbitrary code or non‑influencer workloads.

---

### 2. Identity Declaration

Chimera MUST declare a stable, inspectable identity to the external network.

#### 2.1 Identity Profile

At minimum, the identity profile SHOULD include:

- `node_id`: Stable identifier for this Chimera deployment.
- `display_name`: Human‑readable name.
- `description`: Short description, e.g. “Governed autonomous influencer swarm (Planner–Worker–Judge)”.
- `operator_contact`: Contact channel for human operators (e.g. email alias, URL).
- `governance_profile_ref`: Reference to a machine‑readable governance description (see Section 4).
- `version`: Semantic version of the Chimera node’s spec alignment.

> **[ASSUMPTION]**: The precise field names and serialization format for identity (e.g. JSON vs. other) will be aligned with the chosen external protocol; this spec defines required _content_, not exact wire format.

#### 2.2 Authenticity and Attestation

- Chimera SHOULD support network‑level authentication (e.g. signed identity documents, key‑based trust) so that peers can verify they are communicating with the intended node.
- Any attestation or endorsement system provided by the network (e.g. “verified organization” flags) SHOULD be connected to this identity profile, not to transient internal agents.

---

### 3. Capability Advertisement

Chimera MUST publish a structured capability description so that external nodes can determine what kinds of tasks it can accept.

#### 3.1 Capability Catalog

The capability catalog SHOULD describe:

- **Supported domains**

  - Examples: `trend_research`, `content_generation`, `engagement`, `media_production`, `agentic_commerce`.

- **Supported channels**

  - Examples: social platforms, content formats, and media types for which Chimera is configured.

- **Governance sensitivity**

  - For each capability, whether actions:
    - Can be auto‑approved under certain conditions.
    - Always require Judge approval.
    - Always require HITL approval.

- **Resource characteristics**
  - Qualitative statements about throughput, typical latency range, and cost characteristics (where known).

#### 3.2 Capability Descriptor Shape (Conceptual)

Conceptually, a capability descriptor for a single capability might contain:

- `capability_id`: Stable identifier.
- `name`: Human‑readable label.
- `domain`: Domain keyword (e.g. `content_generation`).
- `supported_channels`: List of channel identifiers.
- `requires_human_review`: `always | policy_based | rare`.
- `max_parallelism_hint`: Non‑binding hint about safe concurrent usage.
- `governance_tags`: Tags like `high_risk`, `financial`, `political_sensitive`, etc.

> **[ASSUMPTION]**: Exact schema and enumeration values depend on the external network’s capability taxonomy and will need reconciliation once that taxonomy is known.

---

### 4. Governance and Safety Signaling

Chimera MUST make its **governance posture** explicit so that external nodes cannot inadvertently ask it to operate outside its constraints.

#### 4.1 Governance Profile

The governance profile SHOULD cover:

- **Review model**

  - Description of Planner–Worker–Judge separation.
  - High‑level rules for when outputs are auto‑approved vs. escalated vs. rejected.

- **Safety categories**

  - Categories that are always considered sensitive (e.g. politics, financial advice, health, legal claims, brand‑critical statements).
  - Categories for which actions MUST be HITL‑approved.

- **Commerce and wallets**

  - Whether agentic commerce is enabled.
  - If enabled, the existence of a dedicated financial Judge gate and per‑transaction approval requirements.

- **Transparency practices**
  - How AI‑generated content is disclosed where required.
  - How audit trails are retained and surfaced upon request.

#### 4.2 Policy Mismatch Handling

- If an external node requests behavior that conflicts with Chimera’s governance profile (e.g. “post without review” for a sensitive category), Chimera MUST:
  - Either reject the request with an explicit policy violation reason; or
  - Accept the request only after mapping it into an internal flow that preserves all governance invariants, and signal any changes in behavior semantics back to the caller.

---

### 5. Availability and Status

Chimera MUST surface its availability and status in a way that external nodes can consume without inspecting internal implementations.

#### 5.1 Status Dimensions

Status SHOULD include:

- `operational_state`: e.g. `online`, `degraded`, `draining`, `offline`.
- `accepting_new_work`: boolean.
- `approx_queue_depth`: qualitative indicator (e.g. `low`, `medium`, `high`) or bounded numeric ranges.
- `expected_latency_hint`: qualitative or bounded numeric ranges for key capability classes.

#### 5.2 Heartbeats and Subscriptions

- Chimera SHOULD regularly publish heartbeats or be queryable via a status endpoint in the external protocol.
- Consumers SHOULD NOT rely on internal metrics; they MUST use these protocol‑level signals to decide whether to route work to Chimera.

---

### 6. Task Delegation Semantics

This section describes how external tasks are mapped into internal flows.

#### 6.1 Accepted Task Types

Chimera MUST clearly state which **task types** it is willing to accept from the network, such as:

- `influencer_trend_research`
- `content_brief_generation`
- `post_draft_generation`
- `reply_draft_generation`
- `media_asset_generation`
- `campaign_level_experiment`
- `agentic_commerce_action` (if enabled)

Each external task type MUST map to one or more internal `task_type` values understood by the Planner and Workers.

#### 6.2 External Task Envelope (Conceptual)

An external task addressed to Chimera SHOULD include at least:

- `external_task_id`
- `origin_node_id`
- `tenant_or_org_context` (how the external network identifies the requester)
- `task_type`
- `goal_description`
- `constraints` (including any policy or budget constraints the origin wishes to impose)
- `success_criteria` (expressed at a level Chimera can map to internal acceptance criteria)

Chimera MUST:

- Validate that it can honor the requested constraints without violating its own constitution and governance profile.
- Reject tasks that cannot be safely mapped, with explicit reasons.

#### 6.3 Mapping to Internal Planner

- For accepted tasks, Chimera’s Planner MUST:

  - Create or associate an internal `GOAL` and a set of `TASK` records.
  - Preserve `external_task_id` and `origin_node_id` as lineage fields in the internal representation.

- Internal retries, replans, and parallelizations MUST NOT be visible to the external node as separate tasks; they are internal implementation details.

---

### 7. Result and Explanation Reporting

Chimera MUST return sufficiently rich results for external nodes to act on, while preserving internal privacy and abstraction.

#### 7.1 Result Envelope (Conceptual)

For each accepted external task, Chimera SHOULD return:

- `external_task_id`
- `node_id` (Chimera)
- `status`: `complete | failed | partial | cancelled`
- `artifacts`: high‑level descriptions and references (e.g. post drafts, media asset references, suggested experiment configurations).
- `governance_summary`:
  - Whether output was auto‑approved, judged, and/or HITL‑approved.
  - High‑level reasons for any rejections or modifications.
- `trace_ref`: an opaque reference that Chimera can later use to reconstruct internal lineage if required for audits.

#### 7.2 Failure and Escalation Reporting

- If Chimera cannot complete a task due to internal safety rules, policy mismatches, or external dependencies, it MUST:
  - Return a structured failure status and a reason code (e.g. `POLICY_VIOLATION`, `INSUFFICIENT_BUDGET`, `UNSUPPORTED_CHANNEL`).
  - Avoid leaking sensitive internal implementation details.

---

### 8. Governance and Safety Across Network Boundaries

#### 8.1 Non‑Delegable Responsibilities

Chimera MUST NOT accept network‑level requests that:

- Ask Chimera to ignore or weaken its internal safety, governance, or audit requirements.
- Require Chimera to perform irreversible actions without the possibility of HITL intervention when its own rules would demand it.

In such cases, Chimera MUST reject the request or negotiate a safer behavior explicitly.

#### 8.2 Data and Tenant Isolation

- External tasks targeting Chimera MUST be assigned to a tenant context within Chimera’s own multi‑tenant model.
- Chimera MUST ensure that no cross‑tenant data access occurs when fulfilling cross‑network tasks:
  - External requests may be mapped to specific tenants or to a dedicated network‑integration tenant, but MUST NOT be allowed to mingle data across tenants.

---

### 9. Open Questions and Alignment Needs

The following items are intentionally left partially specified pending alignment with a concrete external protocol:

- **Wire format and discovery mechanisms**

  - Whether capabilities, identity, and status are discovered via registry, direct queries, or other means.
  - Exact message schemas and authentication handshakes.

- **Standard governance vocabulary**

  - A shared set of risk and governance tags for cross‑network understanding (e.g. what qualifies as “high‑risk politics”).

- **Cross‑network audit integration**
  - How Chimera’s internal audit records can be surfaced or summarized in forms consumable by the broader network without leaking sensitive internal state.

Once an external protocol (e.g. a specific OpenClaw version) is selected, this specification MUST be updated to bind these behavioral requirements to concrete message types and fields, without weakening Chimera’s internal governance and safety invariants.
