# OpenClaw Integration Specification

## Purpose

This document defines how Project Chimera exposes availability, capability, and health
signals to the OpenClaw network. The integration is designed to be non-invasive,
privacy-preserving, and optional, while enabling Chimera to participate in federated
agent coordination ecosystems.

This specification focuses on _publishing status_, not accepting external task execution
in the initial MVP.

---

## Integration Goals

- Advertise Chimera fleet availability and high-level capacity
- Expose agent capabilities in a machine-readable format
- Allow OpenClaw-compatible systems to reason about Chimera readiness
- Preserve tenant isolation and internal operational privacy
- Avoid tight coupling between Chimera and OpenClaw internals

---

## Scope (MVP)

Included:

- Fleet-level status publication
- Agent-level availability and capability metadata
- Read-only exposure via MCP Resource or Tool

Excluded:

- External task intake from OpenClaw
- Cross-network task arbitration
- Shared memory or wallet access
- Cross-tenant execution

---

## Architectural Placement

- OpenClaw integration is owned by the Orchestrator service
- Platform UI does not communicate with OpenClaw directly
- Status data is derived from:
  - Redis queue metrics
  - Orchestrator global state
  - Agent runtime heartbeats

---

## Publishing Models

### Model A: MCP Resource (Pull-Based)

Chimera exposes read-only MCP Resources that OpenClaw can poll.

Resource URIs:

- chimera://status/fleet
- chimera://status/agent/{agent_id}

Characteristics:

- Stateless
- Cacheable
- No authentication beyond MCP transport
- Recommended for MVP

---

### Model B: MCP Tool (Push-Based)

Chimera actively publishes status updates to OpenClaw endpoints.

Characteristics:

- Event-driven
- Higher implementation complexity
- Requires delivery guarantees and retry logic

---

## Fleet Status Resource

Resource URI:
chimera://status/fleet

Response Schema:

```json
{
  "network_id": "chimera",
  "timestamp": "iso-8601",
  "fleet": {
    "active_agents": 0,
    "idle_agents": 0,
    "queue_depth": {
      "task_queue": 0,
      "review_queue": 0,
      "hitl_queue": 0
    },
    "health": {
      "status": "healthy | degraded | critical",
      "last_updated": "iso-8601"
    }
  }
}
```

---

## Agent Status Resource

Resource URI:
chimera://status/agent/{agent_id}

Response Schema:

```json
{
  "agent_id": "uuid",
  "handle": "string",
  "status": "planning | working | judging | sleeping",
  "availability": {
    "accepting_tasks": true,
    "max_parallel_tasks": 0
  },
  "capabilities": [
    "fetch_trends",
    "generate_content",
    "reply_comments",
    "publish_social",
    "commerce_enabled"
  ],
  "constraints": {
    "hitl_required": false,
    "budget_limited": false
  },
  "last_heartbeat": "iso-8601"
}
```

---

## Capability Vocabulary

Capabilities are advertised as stable string identifiers.

Standard Capability Set:

- fetch_trends
- generate_content
- generate_image
- generate_video
- reply_comments
- publish_social
- moderate_content
- commerce_enabled

Capabilities MUST NOT expose internal implementation details.

---

## Privacy and Redaction Rules

- No campaign goals or prompts are exposed
- No memory contents are exposed
- No wallet balances or transaction history are exposed
- Agent identifiers may be anonymized if tenant isolation is enabled
- Capability exposure may be restricted by operator policy

---

## Failure Modes

- If status cannot be computed, resource returns:
  - health.status = degraded
- If agent heartbeat exceeds timeout threshold:
  - agent is marked unavailable
- OpenClaw polling failures do not impact Chimera execution

---

## Security Considerations

- Resources are read-only
- No side effects permitted
- No authentication secrets embedded in payloads
- All payloads must be safe for public or semi-public exposure

---

## Future Extensions (Non-MVP)

- Bidirectional task negotiation
- Capability pricing and cost signaling
- SLA-based availability windows
- Cross-network HITL escalation
- Federated governance policies

---

## MVP Deliverable

- One MCP Resource exposing fleet status
- One MCP Resource exposing agent status
- Configuration flag to enable or disable OpenClaw publishing
- No dependency on OpenClaw uptime for Chimera operation
