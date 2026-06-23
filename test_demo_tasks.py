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
