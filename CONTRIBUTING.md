# Contributing to PortPrimer

Thank you for your interest in contributing to PortPrimer.

PortPrimer is a beginner friendly cybersecurity learning tool that helps people understand open TCP services, port exposure, scan results, and responsible security testing.

The goal is simple: ports explained, not exploited.

## Good Contributions

Helpful contributions include:

- Improving port explanations
- Adding beginner friendly learning notes
- Improving the Port Knowledge Quiz
- Fixing bugs
- Improving reports
- Improving documentation
- Adding safe tests
- Improving the terminal experience
- Making error messages clearer
- Improving responsible-use guardrails

## Project Principles

PortPrimer is a learning tool first and a scanner second.

Contributions should keep the project:

- Safe
- Educational
- Beginner friendly
- Permission based
- Clear and practical
- Focused on understanding, not exploitation

## Contributions We Do Not Accept

Please do not submit code, documentation, examples, or tests that include:

- Exploitation
- Brute forcing
- Credential testing
- Stealth scanning
- IDS or firewall evasion
- Packet spoofing
- Mass scanning
- Unauthorized scanning
- Instructions for attacking real systems
- Claims that an open port automatically means a system is vulnerable

Open ports are clues, not automatic vulnerabilities. PortPrimer should help users think clearly and responsibly.

## How to Contribute

1. Fork the repository.
2. Create a new branch for your change.
3. Make your update.
4. Add or update tests when needed.
5. Update documentation if your change affects usage.
6. Open a pull request with a clear explanation of what changed.

## Pull Request Checklist

Before opening a pull request, please make sure:

- The change is safe and educational
- Tests pass
- Documentation is updated if needed
- No secrets, tokens, passwords, or private data are included
- The change fits PortPrimer’s purpose
- Any new scanning behavior keeps permission and safety checks in place

## Testing

Run the test suite before submitting changes:

```bash
python -m pytest -q
