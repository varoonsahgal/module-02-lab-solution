# test_demo_tasks.py
from demo_tasks import parse_task, priority_score

# ── Test 1: Happy path ────────────────────────────────────────────────
def test_priority_score_high_returns_three():
    # Arrange
    priority = "high"
    # Act
    result = priority_score(priority)
    # Assert
    assert result == 3

# ── Test 2: Another happy path ───────────────────────────────────────
def test_parse_task_strips_title_whitespace():
    # Arrange
    record = {"title": "   Deploy API   ", "priority": "high"}
    # Act
    result = parse_task(record)
    # Assert
    assert result["title"] == "Deploy API"    # whitespace stripped
    assert result["done"] == False            # always starts not done


import pytest
from demo_tasks import parse_task, InvalidTaskError

# ── Negative test: missing title ─────────────────────────────────────
def test_parse_task_missing_title_raises_invalid_task_error():
    with pytest.raises(InvalidTaskError):
        parse_task({})           # empty dict — no title at all

# ── Edge case: whitespace-only title ─────────────────────────────────
def test_parse_task_whitespace_only_title_raises():
    with pytest.raises(InvalidTaskError):
        parse_task({"title": "     "})   # looks like it has content, but doesn't

# ── Edge case: uppercase priority gets normalized ─────────────────────
def test_parse_task_uppercase_priority_is_normalized():
    result = parse_task({"title": "Ship it", "priority": "HIGH"})
    assert result["priority"] == "high"   # normalized to lowercase
