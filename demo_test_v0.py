# demo_test_v0.py
from demo_tasks import priority_score

def test_priority_score_unknown_returns_zero():
    assert priority_score("urgent") == 0
