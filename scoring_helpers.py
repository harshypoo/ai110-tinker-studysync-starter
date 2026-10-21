"""
Target file for Tinker 1B, Part 2.

Move `apply_streak_bonus(combined_score, streak_days)` here from scoring.py,
then update the import at the top of scoring.py so `run_demo()` and the
Session Scorer tab still work exactly as before.
"""

# TODO: move apply_streak_bonus(combined_score, streak_days) here from scoring.py

def apply_streak_bonus(combined_score: int, streak_days: int) -> int:
    """Add a bonus for consecutive study days, capped at 100. Works fine -- it's just in the wrong file."""
    boosted = combined_score + streak_days * 2
    return max(0, min(boosted, 100))