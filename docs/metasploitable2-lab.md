# Metasploitable 2 Lab

Metasploitable 2 is an intentionally vulnerable Linux VM used for cybersecurity training. It should only run inside an isolated local lab network.

Do not expose Metasploitable 2 to the internet, a work network, or any network where other people may be affected.

## Safe setup idea

Use a virtualization platform such as VirtualBox or VMware and place the VM on a host-only or isolated lab network. Keep your testing machine and the VM inside that lab network.

## Finding the VM IP

Find the VM IP address from the VM console or from your virtualization platform's network tools. Then provide that IP to PortPrimer:

```bash
python -m portprimer lab --target 192.168.56.101 --i-have-permission
```

## What PortPrimer does in lab mode

PortPrimer scans a small set of common Metasploitable 2 training ports using normal TCP connect scanning. It explains open services in beginner-friendly language.

PortPrimer does not include exploitation steps, credential testing, brute forcing, or vulnerability checks.

## Demo Tour without a VM

If you do not have Metasploitable 2 installed, run:

```bash
py -m portprimer metasploitable-demo
```

This is a simulated learning tour, not a real scan. It uses sample lab-style open ports to teach what the services are and why they matter, without attack steps.
