from portprimer.safety import PUBLIC_TARGET_AUTHORIZATION_MESSAGE, evaluate_full_range_permission, evaluate_scan_permission, target_appears_public


def test_permission_flag_behavior():
    decision = evaluate_scan_permission("127.0.0.1", has_permission=False, allow_public_target=False)
    assert not decision.allowed
    assert "permission" in decision.reason


def test_localhost_allowed_with_permission():
    decision = evaluate_scan_permission("127.0.0.1", has_permission=True, allow_public_target=False)
    assert decision.allowed


def test_public_target_blocking():
    decision = evaluate_scan_permission("8.8.8.8", has_permission=True, allow_public_target=False)
    assert not decision.allowed
    assert decision.target_is_public
    assert decision.reason == PUBLIC_TARGET_AUTHORIZATION_MESSAGE


def test_public_target_allowed_with_extra_flag():
    decision = evaluate_scan_permission("8.8.8.8", has_permission=True, allow_public_target=True)
    assert decision.allowed


def test_public_full_range_refuses_even_with_public_allowed():
    decision = evaluate_full_range_permission("8.8.8.8", has_permission=True)
    assert not decision.allowed
    assert decision.target_is_public
    assert "local/private targets only" in decision.reason


def test_private_target_detection():
    assert target_appears_public("192.168.56.101") is False
