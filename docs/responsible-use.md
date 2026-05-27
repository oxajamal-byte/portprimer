# Responsible Use

PortPrimer is for authorized learning. Use it only on systems you own, manage, or have clear permission to test.

## Permission

PortPrimer refuses to scan unless you pass:

```bash
--i-have-permission
```

This is intentional. A scan is network activity against another system, so permission matters.

## Public targets

Website/public-IP scans are supported for targets you own or have written permission to test.

If a target appears public, PortPrimer also requires:

```bash
--allow-public-target
```

Public targets are blocked by default to teach safe scope. Only use that flag when you own the public website, domain, or IP address, or when you have clear written permission from the owner. Do not scan random public IPs or domains.

In the interactive menu, the `Website / Public IP` path asks you to type `AUTHORIZED` before it allows a public-target scan. If you type anything else, PortPrimer cancels that action and returns to the main menu. That confirmation is a scope reminder, not a substitute for real permission.

## Safe targets

Good beginner targets include:

- `127.0.0.1`
- `localhost`
- Private lab IPs such as `192.168.56.101`
- A local VM you own
- A training environment that gives you permission
- A public website or domain you own or have written permission to test

## Full local port scans

Full Local Port Scan checks TCP ports `1-65535` and is allowed only for localhost, private IPs, and home/lab targets. PortPrimer refuses full-range scans against public targets even if `--allow-public-target` is provided.

## Why random public scanning is not okay

Public systems belong to someone. Even simple scanning can be unwanted, logged, disruptive, or against policy. Responsible practice means staying inside clear scope.
