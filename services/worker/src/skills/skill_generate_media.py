"""Skill: generate_media

This feature has not been implemented yet, in accordance with test-driven
development practices. The tests are intentionally failing to signal that
implementation is required.
"""

from __future__ import annotations

from typing import Any, Dict


_REQUIRED_KEYS = {
    "media_type",
    "prompt",
    "character_reference_id",
    "style_lora_id",
    "aspect_ratio",
    "generation_tier",
}


def _validate_payload(payload: Dict[str, Any]) -> None:
    missing = _REQUIRED_KEYS.difference(payload.keys())
    if missing:
        raise ValueError(f"Missing required keys: {sorted(missing)}")


def generate_media(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Generate media for a given prompt.

    Parameters
    ----------
    payload: dict
        Must contain at least the keys in ``_REQUIRED_KEYS``.

    Returns
    -------
    dict
        Implementation-defined response contract.

    Raises
    ------
    NotImplementedError
        This feature has not been implemented yet.
    """
    _validate_payload(payload)
    raise NotImplementedError(
        "generate_media has not been implemented yet. "
        "This test is intentionally failing in accordance with TDD practices."
    )
