# Pull Request

## Summary

Explain what this pull request changes.

## Why this matters

Explain how this improves PortPrimer for learners, defenders, or beginner cybersecurity students.

## Type of change

- [ ] Bug fix
- [ ] Documentation update
- [ ] Learning content improvement
- [ ] Quiz improvement
- [ ] Report improvement
- [ ] Safety guardrail improvement
- [ ] Refactor
- [ ] Test improvement
- [ ] Other

## Safety check

- [ ] This change is safe and educational
- [ ] This change does not add exploitation, brute forcing, stealth scanning, evasion, or unauthorized scanning behavior
- [ ] This change keeps permission checks and responsible-use guardrails intact
- [ ] No secrets, tokens, passwords, private files, or personal data are included

## Testing

Describe how you tested this change.

Recommended:

```bash
python -m pytest -q
python -m portprimer playground
python -m portprimer quiz
