# Chimera Agent Skills

This directory defines the runtime Skills available to Chimera agents.

A **Skill** is a discrete, replaceable capability package that exposes a clear
Input/Output contract. Skills are the *only* way agents interact with the external
world. Agents MUST NOT call external APIs, services, or vendors directly.

Skills are invoked by Workers and validated by Judges.

---

## Skill Design Principles

- Skills are capability-based, not task-based.
- Skills expose stable interfaces even if implementations change.
- Skills must be auditable, interruptible, and replaceable.
- Skills do not store long-term state; persistence is handled elsewhere.
- Skills return structured results with confidence and metadata.

---

## Skill: skill_fetch_trends

### Purpose

Fetches and aggregates trending topics from public sources to support
planning and content ideation. This skill supports *perception*, not decision-making.

### Input Contract

```json
{
  "sources": ["twitter", "news", "rss"],
  "topics_filter": ["string"],
  "time_window_hours": 24,
  "max_results": 50
}
```

### Output Contract

```json
{
  "status": "success | failure",
  "trends": [
    {
      "topic": "string",
      "source": "twitter | news | rss",
      "relevance_score": 0.0,
      "sample_mentions": ["string"],
      "detected_at": "timestamp"
    }
  ],
  "confidence_score": 0.0,
  "error": {
    "code": "string",
    "message": "string"
  }
}
```

### Notes

- This skill performs *no filtering for policy or sensitivity*.
- Trend interpretation is the responsibility of the Planner or Judge.
- Low confidence scores should trigger re-fetch or alternative sources.

---

## Skill: skill_generate_media

### Purpose

Generates images or videos for agent content while enforcing
character consistency and style constraints.

### Input Contract

```json
{
  "media_type": "image | video",
  "prompt": "string",
  "character_reference_id": "string",
  "style_lora_id": "string",
  "aspect_ratio": "1:1 | 9:16 | 16:9",
  "generation_tier": "tier1 | tier2"
}
```

### Output Contract

```json
{
  "status": "success | failure",
  "asset": {
    "asset_type": "image | video",
    "storage_url": "string",
    "duration_seconds": 0,
    "resolution": "string"
  },
  "confidence_score": 0.0,
  "error": {
    "code": "string",
    "message": "string"
  }
}
```

### Notes

- Character consistency is mandatory when `character_reference_id` is provided.
- Tier selection influences cost and latency, not behavior.
- Output must be validated by a Judge before publication.

---

## Skill: skill_publish_social

### Purpose

Publishes approved content to external social platforms in a
platform-agnostic manner.

### Input Contract

```json
{
  "platform": "twitter | instagram | threads",
  "text_content": "string",
  "media_urls": ["string"],
  "disclosure_level": "automated | assisted | none",
  "scheduled_at": "timestamp"
}
```

### Output Contract

```json
{
  "status": "success | failure",
  "external_post_id": "string",
  "platform": "string",
  "published_at": "timestamp",
  "confidence_score": 0.0,
  "error": {
    "code": "string",
    "message": "string"
  }
}
```

### Notes

- This skill must only be invoked after approval.
- Failure does not imply retry; retries are a Planner decision.
- Disclosure level must comply with platform and policy requirements.

---

## Governance Rules (All Skills)

- Every skill MUST return a `confidence_score`.
- Any skill failure must return a structured error object.
- Skills must be safe to disable or swap without breaking agent logic.
- Skills do not make policy decisions; they only execute capabilities.

---

## Future Skills (Non-MVP)

Examples:
- skill_transcribe_audio
- skill_analyze_engagement
- skill_execute_transaction
- skill_moderate_content

These are intentionally excluded from MVP to preserve focus and safety.
