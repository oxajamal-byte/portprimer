import pytest

from portprimer.labels import validate_action_hint, validate_label


def test_learning_label_lookup():
    assert validate_label("Web Door") == "Web Door"
    assert validate_action_hint("Keep private") == "Keep private"


def test_invalid_learning_label():
    with pytest.raises(ValueError):
        validate_label("High")

