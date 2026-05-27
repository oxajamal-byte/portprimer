# PortPrimer Report

## Target and scan settings

- Target: `demo-local-lab`
- Profile: `demo`
- Timeout: `1.0` seconds
- Concurrency: `10`
- Generated: `2026-05-26T00:00:00Z`

## Summary

An open port is not automatically a vulnerability. It is a clue. Whether it matters depends on exposure, configuration, authentication, patching, and whether the service is needed.

- Open ports: 3
- Closed ports: 2
- Timed out ports: 0
- Total checked: 5

## Open services table

| Port | Service | Door Type | Action Hint |
| --- | --- | --- | --- |
| 22 | SSH | Admin Door | Keep private |
| 80 | HTTP | Web Door | Usually okay if expected |
| 8080 | HTTP Alternate | Web Door | Review if unexpected |

## Beginner notes for each open service

### 22/tcp SSH

- What it is: SSH is used to remotely manage a machine.
- Why it matters: It is normal on servers, but admin access should be protected carefully.
- Beginner note: If SSH is open, use strong authentication and restrict who can reach it.

### 80/tcp HTTP

- What it is: HTTP serves websites or web applications without built-in encryption.
- Why it matters: Web services are common, but public exposure should be intentional.
- Beginner note: If HTTP is open, learn what site or app is being served.

### 8080/tcp HTTP Alternate

- What it is: Port 8080 commonly hosts alternate web applications or proxies. In Playground Tour, it is only a safe local practice service created by PortPrimer.
- Why it matters: It is easy to forget test or admin web apps on alternate ports. Playground Tour does not implement real HTTP or a vulnerable service.
- Beginner note: For real systems, inspect the service only when you are authorized. In Playground Tour, this exists so you can see how open ports appear in a scan.

## Suggested next steps

- Confirm each open service is expected for this system.
- Keep admin, data, and private services reachable only by trusted users and networks.
- Remove or disable services that are not needed.
- Learn what owns an unknown port before changing it.

## Responsible-use reminder

Use PortPrimer only on systems you own, manage, or have clear permission to test. Do not scan random public targets.

## Limitations

PortPrimer performs normal TCP connect scanning only. It does not exploit services, test credentials, prove vulnerabilities, prove safety, fingerprint operating systems, grab aggressive banners, scan CIDR ranges, or replace Nmap.
