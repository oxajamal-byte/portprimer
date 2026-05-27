# Design Decisions

PortPrimer is intentionally narrow. The goal is safe beginner education, not offensive capability.

## TCP connect scanning only

PortPrimer uses normal TCP connect scanning because it is easy to understand and does not require raw packet privileges.

## Playground Tour uses localhost-only practice sockets

Playground Tour exists so beginners can learn immediately without installing a vulnerable VM, Docker, VirtualBox, or VMware. It starts simple TCP listeners on high ports and binds only to `127.0.0.1`. The listeners send a short plain-text teaching message and do not implement real SSH, database, HTTP, Redis, or any other real protocol behavior.

## Demo tours do not scan

Metasploitable Demo Tour uses simulated results to teach lab ports without requiring a VM. It does not connect to a target and does not include exploitation steps.

## Full local port scans are private-only

Full-range scanning is opt-in, requires permission, uses TCP connect scanning only, and is refused for public targets. It exists to teach what a full port range means, not to enable broad scanning.

## No stealth scanning

Stealth scanning is outside the educational goal. PortPrimer should teach service exposure clearly, not evasion.

## No exploitation

PortPrimer does not prove vulnerabilities or attempt exploits. It explains what open services usually mean.

## No brute forcing or credential testing

Credential testing can quickly become harmful or unauthorized. PortPrimer avoids it completely.

## No aggressive banner grabbing

PortPrimer does not aggressively query services for banners. The first release focuses on port state and known educational notes.

## No OS fingerprinting

OS fingerprinting can be inaccurate and is not needed to teach common service exposure.

## No mass scanning or CIDR scanning

PortPrimer is for small, intentional, authorized targets. It does not support internet-scale scanning or CIDR ranges.
