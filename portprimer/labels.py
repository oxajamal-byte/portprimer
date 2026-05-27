from __future__ import annotations

LEARNING_LABELS = {
    "Web Door",
    "Admin Door",
    "Data Door",
    "Legacy Door",
    "Private Door",
    "Mail Door",
    "Name Door",
    "Lab Door",
    "System Door",
    "Unknown Door",
}

ACTION_HINTS = {
    "Usually okay if expected",
    "Review if unexpected",
    "Keep private",
    "Replace or disable if unused",
    "Lab only",
    "Learn more before changing",
}


def validate_label(label: str) -> str:
    if label not in LEARNING_LABELS:
        raise ValueError(f"Unknown learning label: {label}")
    return label


def validate_action_hint(hint: str) -> str:
    if hint not in ACTION_HINTS:
        raise ValueError(f"Unknown action hint: {hint}")
    return hint

