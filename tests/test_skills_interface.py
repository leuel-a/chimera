import inspect

import pytest


@pytest.mark.parametrize(
    "module_path,function_name,required_keys",
    [
        (
            "services.worker.src.skills.skill_fetch_trends",
            "fetch_trends",
            {"sources", "topics_filter", "time_window_hours", "max_results"},
        ),
        (
            "services.worker.src.skills.skill_generate_media",
            "generate_media",
            {
                "media_type",
                "prompt",
                "character_reference_id",
                "style_lora_id",
                "aspect_ratio",
                "generation_tier",
            },
        ),
        (
            "services.worker.src.skills.skill_publish_social",
            "publish_social",
            {
                "platform",
                "text_content",
                "media_urls",
                "disclosure_level",
                "scheduled_at",
            },
        ),
    ],
)
def test_skill_modules_exist_and_have_expected_signature(
    module_path, function_name, required_keys
):
    """
    Failing test by design.

    Each skill must exist in:
      services/worker/src/skills/

    And expose a function with signature:
      fn(payload: dict) -> dict

    The payload must contain at least required_keys.
    """
    module = __import__(module_path, fromlist=[function_name])
    fn = getattr(module, function_name)

    sig = inspect.signature(fn)
    params = list(sig.parameters.values())

    # Must be exactly one positional parameter: payload (dict)
    assert len(params) == 1
    assert params[0].name in ("payload", "input", "data")

    # Basic runtime check of required keys enforcement (should raise on missing keys)
    with pytest.raises(Exception):
        fn({})  # must reject missing required keys

    # Should accept at least required keys
    payload = {k: None for k in required_keys}
    # Not asserting success yet; only interface acceptance.
    fn(payload)
