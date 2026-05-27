from __future__ import annotations

MAX_CUSTOM_PORTS = 100
FULL_RANGE_PORTS = list(range(1, 65536))

PROFILES: dict[str, list[int]] = {
    "beginner": [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 3389, 5432, 6379, 8080, 9200, 27017],
    "web": [80, 443, 8000, 8080, 8443],
    "remote": [22, 23, 3389, 5900],
    "database": [1433, 1521, 3306, 5432, 6379, 9200, 27017],
    "playground": [8022, 8080, 15432, 16379, 18080],
    "metasploitable2": [21, 22, 23, 25, 53, 80, 111, 139, 445, 512, 513, 514, 1099, 1524, 2049, 2121, 3306, 5432, 5900, 6000, 6667, 8009, 8180],
}


def list_profiles() -> list[str]:
    return sorted(PROFILES)


def get_profile_ports(profile: str) -> list[int]:
    try:
        return list(PROFILES[profile])
    except KeyError as exc:
        names = ", ".join(list_profiles())
        raise ValueError(f"Unknown profile '{profile}'. Choose one of: {names}.") from exc


def parse_custom_ports(raw_ports: str) -> list[int]:
    if not raw_ports.strip():
        raise ValueError("Custom ports cannot be empty.")

    ports: list[int] = []
    seen: set[int] = set()
    duplicates: list[int] = []

    for item in raw_ports.split(","):
        text = item.strip()
        if not text:
            raise ValueError("Custom ports must be comma-separated numbers.")
        if not text.isdigit():
            raise ValueError(f"Invalid port '{text}'. Ports must be numbers from 1 to 65535.")
        port = int(text)
        if port < 1 or port > 65535:
            raise ValueError(f"Invalid port '{port}'. Ports must be between 1 and 65535.")
        if port in seen:
            duplicates.append(port)
        seen.add(port)
        ports.append(port)

    if duplicates:
        duplicate_text = ", ".join(str(port) for port in sorted(set(duplicates)))
        raise ValueError(f"Duplicate custom port(s): {duplicate_text}. Remove duplicates and try again.")
    if len(ports) > MAX_CUSTOM_PORTS:
        raise ValueError(f"Custom scans are limited to {MAX_CUSTOM_PORTS} ports.")
    return ports


def choose_ports(profile: str | None, custom_ports: str | None) -> tuple[str, list[int]]:
    if profile and custom_ports:
        raise ValueError("Choose either --profile or --ports, not both.")
    if custom_ports:
        return "custom", parse_custom_ports(custom_ports)
    profile_name = profile or "beginner"
    return profile_name, get_profile_ports(profile_name)
