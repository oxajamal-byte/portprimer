# Beginner Guide

## What are ports?

A port is like a numbered door for network traffic. A computer can run many services at the same time, and ports help traffic reach the right service.

For example, web traffic often uses port 80 for HTTP or port 443 for HTTPS. Remote administration often uses port 22 for SSH.

## Start without a lab VM

If you do not have Metasploitable 2, VirtualBox, VMware, Docker, or another lab ready, use Playground Tour:

```bash
py -m portprimer playground
```

Playground Tour starts safe local practice services on `127.0.0.1` only, scans the playground port list, writes the same Markdown and JSON reports, and then shuts the services down. These are not real vulnerable services and do not implement real SSH, database, HTTP, Redis, or other protocol behavior. They exist so you can see how open ports appear in a scan.

## Choosing a scan path

The interactive menu gives you beginner-friendly paths:

- Playground Tour for immediate local practice.
- Metasploitable Demo Tour for simulated lab-port learning without a VM.
- This Computer for localhost.
- Private IP / Home Lab for devices you own on your local network.
- Metasploitable 2 VM Scan for your own isolated vulnerable lab VM.
- Website / Public IP for public targets you own or have written permission to scan.
- Full Local Port Scan for TCP ports 1-65535 on local/private targets only.
- Port Knowledge Quiz for a 20-question practice test, with Learning Center access nearby.
- Demo Report when you want to see report format without scanning.

Interactive mode behaves like a small workspace. After you choose one scan path, PortPrimer runs that action and shows a `Next` menu. Press Enter or choose `M` for the main menu, `R` to run the same action again, or `Q` to quit.

Website/public-IP scans are supported with explicit authorization. Public targets are blocked by default to teach safe scope, and interactive Website / Public IP mode asks you to type `AUTHORIZED` before it runs the web profile.

## Short output and explanations

PortPrimer keeps terminal output brief by default so beginners can focus on the scan result first. Use `--explain` when you want short notes in the terminal:

```bash
py -m portprimer scan --target 127.0.0.1 --profile beginner --i-have-permission --explain
```

Interactive mode does not show notes automatically. Choose `L` from the `Next` menu to show short learning notes. Markdown and JSON reports always include the full learning notes.

The Metasploitable Demo Tour does not scan anything. It shows simulated lab-style open ports so you can learn before installing a VM.

Use `--no-clear` with interactive mode when you want the menu to avoid clearing the terminal, such as when taking screenshots. Use `--compact-logo` when you want the short logo.

## What does open mean?

An open port usually means a service answered the connection attempt. That does not automatically mean something is vulnerable. It means there is something worth understanding.

Good beginner questions are:

- Is this service expected?
- Who should be able to reach it?
- Does it need authentication?
- Is the software maintained?
- Can it be kept private?

## What does closed mean?

A closed port means the target responded but nothing accepted a connection on that port. PortPrimer summarizes closed ports so the report stays readable.

## What does timeout mean?

A timeout means PortPrimer did not get a clear answer before the timeout ended. Firewalls, routing, filtering, or a quiet host can cause timeouts.

## What should I do with results?

Use results as a learning map. Identify expected services, look up unknown services, and avoid changing systems you do not understand or do not have permission to manage.
