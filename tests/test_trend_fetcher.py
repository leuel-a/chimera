import pytest


def test_trend_fetcher_output_matches_contract():
    """
    Failing test by design.

    The implementation is expected to exist at:
      services/worker/src/skills/skill_fetch_trends.py

    It must expose:
      fetch_trends(payload: dict) -> dict
    and return output matching the contract:
      {
        "status": "success|failure",
        "trends": [...],
        "confidence_score": float,
        "error": {"code": str, "message": str} | None
      }
    """
    from services.worker.src.skills.skill_fetch_trends import fetch_trends  # noqa: F401

    payload = {
        "sources": ["twitter", "news", "rss"],
        "topics_filter": ["ai", "startup"],
        "time_window_hours": 24,
        "max_results": 5,
    }

    result = fetch_trends(payload)

    # Envelope
    assert isinstance(result, dict)
    assert "status" in result
    assert result["status"] in ("success", "failure")

    assert "confidence_score" in result
    assert isinstance(result["confidence_score"], (int, float))
    assert 0.0 <= float(result["confidence_score"]) <= 1.0

    assert "trends" in result
    assert isinstance(result["trends"], list)

    # Item schema
    for item in result["trends"]:
        assert isinstance(item, dict)
        assert "topic" in item and isinstance(item["topic"], str)
        assert "source" in item and item["source"] in ("twitter", "news", "rss")
        assert "relevance_score" in item and isinstance(
            item["relevance_score"], (int, float)
        )
        assert "sample_mentions" in item and isinstance(item["sample_mentions"], list)
        assert "detected_at" in item and isinstance(item["detected_at"], str)

    # Error is optional, but if status=failure it must exist
    if result["status"] == "failure":
        assert "error" in result
        assert isinstance(result["error"], dict)
        assert "code" in result["error"] and isinstance(result["error"]["code"], str)
        assert "message" in result["error"] and isinstance(
            result["error"]["message"], str
        )
