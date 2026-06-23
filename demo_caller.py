# In demo_tasks.py, change priority_score:
def priority_score(priority: str) -> int:
    weights = {"low": 1, "medium": 2, "high": 3}
    return weights.get(priority, 99)   # bug: unknown priority returns 99, not 0
