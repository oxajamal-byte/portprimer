from __future__ import annotations

import ipaddress
import socket
from dataclasses import dataclass


RESPONSIBLE_USE_MESSAGE = (
    "PortPrimer is for authorized learning only. Scan systems you own, manage, "
    "or have clear permission to test. An open port is not automatically a vulnerability."
)

PUBLIC_TARGET_AUTHORIZATION_MESSAGE = (
    "Public target detected.\n"
    "PortPrimer supports website/public-IP scans only when you own the target or have written permission.\n"
    "Run again with --allow-public-target if this scan is authorized."
)


@dataclass(frozen=True)
class SafetyDecision:
    allowed: bool
    reason: str
    target_is_public: bool


def _ip_is_private_or_local(ip: ipaddress._BaseAddress) -> bool:
    return bool(ip.is_private or ip.is_loopback or ip.is_link_local)


def target_appears_public(target: str) -> bool:
    cleaned = target.strip()
    try:
        return not _ip_is_private_or_local(ipaddress.ip_address(cleaned))
    except ValueError:
        pass

    lowered = cleaned.lower()
    if lowered == "localhost" or lowered.endswith(".local"):
        return False
    try:
        infos = socket.getaddrinfo(cleaned, None)
    except OSError:
        return True
    resolved = {info[4][0] for info in infos}
    if not resolved:
        return True
    return any(not _ip_is_private_or_local(ipaddress.ip_address(addr)) for addr in resolved)


def evaluate_scan_permission(target: str, has_permission: bool, allow_public_target: bool) -> SafetyDecision:
    if not has_permission:
        return SafetyDecision(False, "Scanning requires the explicit --i-have-permission flag.", False)

    is_public = target_appears_public(target)
    if is_public and not allow_public_target:
        return SafetyDecision(
            False,
            PUBLIC_TARGET_AUTHORIZATION_MESSAGE,
            True,
        )
    return SafetyDecision(True, "Safety checks passed.", is_public)


def evaluate_full_range_permission(target: str, has_permission: bool) -> SafetyDecision:
    if not has_permission:
        return SafetyDecision(False, "Full local port scan requires permission confirmation.", False)
    is_public = target_appears_public(target)
    if is_public:
        return SafetyDecision(False, "Full-range scans are local/private targets only, even with --allow-public-target.", True)
    return SafetyDecision(True, "Full local port scan safety checks passed.", False)
