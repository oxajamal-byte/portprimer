# PortPrimer

**Ports explained, not exploited.**

PortPrimer is a beginner-friendly port learning tool for authorized cybersecurity practice. It teaches what ports are, what common services use them, why exposure matters, and how to think safely about scan results.

PortPrimer is not a replacement for Nmap, not an exploit tool, and not a vulnerability scanner. It helps beginners learn what common open TCP services mean.

## What is PortPrimer?

PortPrimer performs normal TCP connect scanning against a target you own, manage, or have clear permission to test. For each open port, it shows:

- Port number
- Common service name
- Learning label, such as Web Door or Admin Door
- Action hint
- Short beginner notes

An open port is not automatically a vulnerability. It is a clue. Whether it matters depends on exposure, configuration, authentication, patching, and whether the service is needed.

## Why I built it

Many first port scanner projects stop at `open` or `closed`. PortPrimer adds beginner-focused context so a learner can understand why a port might matter without jumping into exploitation or fear-based language.

## What makes it different from a normal port scanner

- Small, intentional scan profiles
- Friendly explanations for open services
- Responsible-use checks before scanning
- Website/public-IP scans supported with explicit authorization
- Markdown and JSON reports
- A clean field-notebook terminal interface

## Interactive modes

Run:

```bash
py -m portprimer
```

Choose:

```text
 ___           _   ___      _
| _ \___ _ _| |_| _ \_ _(_)_ __  ___ _ _
|  _/ _ \ '_|  _|  _/ '_| | '  \/ -_) '_|
|_| \___/_|  \__|_| |_| |_|_|_|_\___|_|

        ports explained, not exploited

[1] Playground Tour             safe local practice, no VM needed
[2] Metasploitable Demo Tour    learn lab ports without installing a VM
[3] This Computer               scan localhost
[4] Private IP / Home Lab       scan a device you own
[5] Metasploitable 2 VM Scan    scan your isolated local VM
[6] Website / Public IP         supported with authorization
[7] Full Local Port Scan        1-65535 on local/private targets only
[8] Port Knowledge Quiz         20-question learning test
[9] Demo Report                 generate sample output
[0] Exit
```

Interactive mode behaves like a small workspace. After a scan or demo finishes, choose what to do next:

```text
Next:
[L] learn about these ports
[M] main menu
[R] run again
[Q] quit
```

Pressing Enter at the `Next` prompt returns to the main menu. Use `--no-clear` for screenshots or debugging:

```bash
py -m portprimer --no-clear
```

Use `--compact-logo` when you want the short logo even in a wide terminal:

```bash
py -m portprimer --compact-logo
```

Command-line mode exits after each command, which makes it suitable for scripts and repeatable examples.

## Scan paths

- Playground Tour: safe local practice services on `127.0.0.1`; no VM needed.
- Metasploitable Demo Tour: simulated lab-port learning without scanning or installing a VM.
- This Computer: scans localhost with the beginner profile.
- Private IP / Home Lab: scans a device you own or manage on your local network.
- Metasploitable 2 VM Scan: scans your own isolated vulnerable lab VM.
- Website / Public IP: scans a public website or IP when you own it or have written permission. The interactive path requires typing `AUTHORIZED`.
- Full Local Port Scan: scans TCP ports 1-65535 on localhost/private targets only, with explicit permission.
- Port Knowledge Quiz: 20 randomized multiple-choice questions, with Learning Center access from the same learning area.
- Demo Report: generates a sample report without scanning.

## Playground Tour

Playground Tour is for beginners who do not have a lab VM, Docker, VirtualBox, or VMware ready yet. It starts a few harmless practice sockets on `127.0.0.1` using high ports only, scans those exact local ports, writes the normal Markdown and JSON reports, then shuts the sockets down.

```bash
py -m portprimer playground
```

The playground services are not real SSH, database, HTTP, Redis, or vulnerable services. They are simple local TCP listeners that send a short plain-text learning message. They bind only to `127.0.0.1` and exist so you can see how open ports appear in a scan.

Add `--explain` when you want short learning notes in the terminal:

```bash
py -m portprimer playground --explain
```

## Metasploitable 2 Lab Mode

Lab mode uses a profile for common Metasploitable 2 training ports:

```bash
py -m portprimer lab --target 192.168.56.101 --i-have-permission
```

Use this only with your own isolated local lab VM. Metasploitable 2 is intentionally vulnerable and should not be exposed to public networks.

## Metasploitable Demo Tour

This mode does not scan. It uses simulated Metasploitable-style open ports to teach what common lab services are and why they matter.

```bash
py -m portprimer metasploitable-demo
```

It does not include exploitation steps or attack instructions.

## Full Local Port Scan

Full-range scanning is optional and private-only. It checks TCP ports `1-65535` using normal TCP connect scanning and can take longer.

```bash
py -m portprimer scan --target 127.0.0.1 --full-range --i-have-permission
```

Public targets are refused for full-range scans, even when `--allow-public-target` is provided.

## Responsible use

PortPrimer requires `--i-have-permission` before command-line scanning. If a target appears public, PortPrimer also requires `--allow-public-target`.

Website/public-IP scans are supported for targets you own or have written permission to test. Public targets are blocked by default to teach safe scope; add `--allow-public-target` only when the scan is authorized. Do not scan random public targets.

This refuses because the public-target confirmation is missing:

```bash
py -m portprimer scan --target example.com --profile web --i-have-permission
```

This is the supported form for an authorized website or public-IP scan:

```bash
py -m portprimer scan --target example.com --profile web --i-have-permission --allow-public-target
```

## Installation

```bash
pip install -e .
```

For development tests:

```bash
pip install -e ".[dev]"
pytest
```

## Quick start

Direct beginner scan:

```bash
py -m portprimer scan --target 127.0.0.1 --profile beginner --i-have-permission
```

Show compact terminal explanations:

```bash
py -m portprimer scan --target 127.0.0.1 --profile beginner --i-have-permission --explain
```

Custom ports:

```bash
py -m portprimer scan --target 127.0.0.1 --ports 22,80,443,3306 --i-have-permission
```

Demo report without scanning:

```bash
py -m portprimer demo
```

Authorized website or domain scan:

```bash
py -m portprimer scan --target example.com --profile web --i-have-permission --allow-public-target
```

Learning center and quiz:

```bash
py -m portprimer learn
py -m portprimer quiz
```

## Scan profiles

- `beginner`: common learning ports across web, admin, mail, file sharing, and databases
- `web`: common web service ports
- `remote`: remote access ports
- `database`: common database and data service ports
- `playground`: simulated local teaching ports, `8022`, `8080`, `15432`, `16379`, and `18080`
- `metasploitable2`: common ports for a local Metasploitable 2 lab VM

Custom scans accept comma-separated ports, reject duplicates, reject invalid ports, and are limited to 100 ports.

## Example output

Default terminal output is intentionally brief. Full learning notes are always written to the Markdown and JSON reports.

```text
 ___           _   ___      _
| _ \___ _ _| |_| _ \_ _(_)_ __  ___ _ _
|  _/ _ \ '_|  _|  _/ '_| | '  \/ -_) '_|
|_| \___/_|  \__|_| |_| |_|_|_|_\___|_|

        ports explained, not exploited

Scan: Playground Tour
Target: 127.0.0.1
Profile: playground
Checked: 5 ports
Open: 5

Open services
----------------------------------------
8022   Playground SSH        Admin Door  Lab only
8080   HTTP Alternate        Web Door    Review
15432  Playground DB         Data Door   Lab only

Reports saved
  Markdown: reports/portprimer-playground-127-0-0-1-20260526-1815.md
  JSON:     reports/portprimer-playground-127-0-0-1-20260526-1815.json
```

With `--explain`, command-line mode adds short notes after the open-services list. In interactive mode, choose `L` from the `Next` menu:

```text
8022/tcp Playground SSH
  What: Safe local practice service.
  Use:  Shows how an admin-style open port appears.
  Watch: Localhost only. Not a real SSH service.
  Takeaway: Keep admin access restricted.
```

## Example report

Reports are written with the scan path or profile, safe target name, and timestamp:

- `reports/portprimer-playground-127-0-0-1-20260526-1815.md`
- `reports/portprimer-scan-custom-127-0-0-1-20260526-1818.json`
- `reports/portprimer-demo-local-lab-20260526-1819.md`

See [docs/example-report.md](docs/example-report.md) and [examples/sample-report.md](examples/sample-report.md).

## How PortPrimer explains open ports

Reports include full learning notes for each known open port:

- What it is
- Used for
- Why it matters
- What to watch
- Should it be open
- Beginner note

Unknown open ports are still displayed as `Unknown Door` with the action hint `Learn more before changing`.

## Limitations

PortPrimer only performs normal TCP connect scanning. It does not perform SYN scanning, stealth scanning, packet spoofing, decoy scanning, IDS or firewall evasion, exploit checks, brute forcing, credential testing, OS fingerprinting, aggressive banner grabbing, mass internet scanning, or CIDR scanning.

PortPrimer does not prove a machine is secure or insecure.

## Project structure

```text
portprimer/
  portprimer/   Python package
  docs/         Beginner and responsible-use documentation
  examples/     Sample report outputs
  reports/      Generated local reports
  tests/        pytest test suite
```
