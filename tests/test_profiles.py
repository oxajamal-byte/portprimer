import pytest

from portprimer.profiles import get_profile_ports, parse_custom_ports


def test_profile_loading():
    assert 22 in get_profile_ports("beginner")
    assert get_profile_ports("web") == [80, 443, 8000, 8080, 8443]


def test_metasploitable2_profile_exists():
    ports = get_profile_ports("metasploitable2")
    assert 1524 in ports
    assert 8180 in ports


def test_playground_profile_exists():
    assert get_profile_ports("playground") == [8022, 8080, 15432, 16379, 18080]


def test_playground_ports_are_high_ports():
    assert all(port >= 1024 for port in get_profile_ports("playground"))


def test_custom_port_parsing():
    assert parse_custom_ports("22,80,443") == [22, 80, 443]


def test_invalid_port_rejection():
    with pytest.raises(ValueError):
        parse_custom_ports("0,22")
    with pytest.raises(ValueError):
        parse_custom_ports("abc")


def test_duplicate_port_handling():
    with pytest.raises(ValueError, match="Duplicate"):
        parse_custom_ports("22,80,22")


def test_custom_port_limit():
    ports = ",".join(str(port) for port in range(1, 102))
    with pytest.raises(ValueError, match="limited"):
        parse_custom_ports(ports)
