# Security Policy

PortPrimer is an educational TCP connect scanner. It is built for authorized learning on systems you own, manage, or have clear written permission to test.

## Supported scope

PortPrimer is designed to:

- Help learners understand what common open TCP services mean
- Practice scanning safely against localhost and lab targets
- Generate clean reports that explain results in plain language

PortPrimer is not designed for and does not include:

- Exploitation, brute forcing, or credential testing
- SYN, stealth, or fragmented scanning
- IDS or firewall evasion
- OS fingerprinting
- CIDR or mass scanning
- Aggressive banner grabbing

If a feature would push the tool toward offensive security rather than education, it is intentionally left out.

## Responsible use

- Only scan systems you own or have explicit written permission to test.
- Keep intentionally vulnerable lab targets (Metasploitable 2 and similar) isolated on a private network.
- Treat the `AUTHORIZED` confirmation and the `--allow-public-target` flag as a scope check, not a license to scan whatever you want.
- An open port is not automatically a vulnerability. Treat scan results as a starting point, not a conclusion.

## Reporting a security issue in PortPrimer

If you find a security issue in the PortPrimer code itself (for example, a bug that bypasses the permission checks or causes unsafe behavior), please report it privately rather than opening a public issue.

Include:

- The version or commit you tested
- A clear description of the issue
- Steps to reproduce
- Expected and actual behavior

If you are reporting through GitHub, use the private security advisory feature on the repository.

## Out of scope

The following are outside the scope of this security policy:

- Reports about Nmap, Metasploitable 2, or other third-party tools
- Requests for help scanning systems you do not own
- Requests for exploit code or attack techniques

Thanks for helping keep PortPrimer focused and safe.