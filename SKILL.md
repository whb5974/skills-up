---
name: nmap-scanner
description: Network scanning and security assessment using nmap. Use when user asks for port scanning, network discovery, service detection, vulnerability scanning, or security audits of networked hosts.
---

# Nmap Network Scanner Skill

## Overview

This skill provides network scanning and security assessment capabilities using nmap. It helps users discover hosts, scan ports, detect services, and identify potential security issues on their network.

## ⚠️ Important Legal & Ethical Guidelines

**BEFORE ANY SCAN:**

1. **Authorization Required** - Only scan networks/hosts you own or have explicit written permission to scan
2. **Legal Compliance** - Unauthorized scanning may violate computer crime laws
3. **Scope Definition** - Clearly define what IPs/ranges are in scope
4. **Impact Awareness** - Some scans can disrupt services (especially vulnerability scans)

**Never scan:**
- Public networks without permission
- Your ISP's infrastructure
- Websites/services you don't own
- Government/military networks
- Any system without explicit authorization

## Core Rules

- Require explicit approval before any scan
- Always confirm target IP/range is owned or authorized
- Start with least-intrusive scans first
- Warn about potential service impact
- Redact sensitive data from outputs
- Store results securely

## Workflow

### 1) Establish Authorization & Scope

**Required confirmations before scanning:**

1. "Do you own this network/host or have explicit written permission to scan it?"
2. "What is the target IP address or range?"
3. "What type of scan do you need?" (provide numbered options)

**Authorization checklist:**
- [ ] User confirms ownership or written permission
- [ ] Target IP/range is clearly defined
- [ ] Scan type is appropriate for the goal
- [ ] User understands potential impact

### 2) Scan Type Selection

Offer scan options (numbered):

1. **Quick Host Discovery** - Ping scan, identify live hosts (`nmap -sn`)
2. **Basic Port Scan** - Top 1000 ports (`nmap <target>`)
3. **Full Port Scan** - All 65535 ports (`nmap -p- <target>`)
4. **Service Detection** - Identify running services (`nmap -sV <target>`)
5. **OS Detection** - Guess operating system (`nmap -O <target>`)
6. **Comprehensive Scan** - Services + OS + scripts (`nmap -A <target>`)
7. **Vulnerability Scan** - NSE vulnerability scripts (`nmap --script vuln <target>`)
8. **Stealth Scan** - SYN scan (`nmap -sS <target>`)

**Recommendations:**
- Start with option 1-2 for initial reconnaissance
- Use option 4-6 for detailed assessment
- Option 7 only for security audits (may be intrusive)
- Option 8 for avoiding detection (ethical use only)

### 3) Pre-Scan Safety Check

**Verify:**
- Nmap is installed (`which nmap`)
- Target is valid IP/hostname
- User has network connectivity
- No critical services on target that could be disrupted

**Warn about:**
- Vulnerability scans may crash old services
- Aggressive scans can trigger IDS/IPS alerts
- OS detection requires root/admin privileges
- Some scans may be logged by target systems

### 4) Execute Scan

**Common scan commands:**

```bash
# Host discovery (ping scan)
nmap -sn 192.168.1.0/24

# Basic port scan
nmap 192.168.1.1

# Fast scan (top 100 ports)
nmap -F 192.168.1.1

# Full port scan
nmap -p- 192.168.1.1

# Service version detection
nmap -sV 192.168.1.1

# OS detection (requires root)
sudo nmap -O 192.168.1.1

# Comprehensive scan
nmap -A 192.168.1.1

# Vulnerability scan
nmap --script vuln 192.168.1.1

# All TCP ports + service detection
nmap -p- -sV 192.168.1.1

# UDP scan (slow)
nmap -sU 192.168.1.1

# Aggressive timing (faster, more intrusive)
nmap -T4 192.168.1.1

# Paranoid timing (slowest, stealthiest)
nmap -T1 192.168.1.1
```

**Timing templates:**
- T0 (Paranoid) - IDS evasion
- T1 (Sneaky) - IDS evasion
- T2 (Polite) - Slow, friendly
- T3 (Normal) - Default
- T4 (Aggressive) - Fast, assumes reliable network
- T5 (Insane) - Very fast, may miss things

### 5) Parse & Present Results

**Extract key information:**

1. **Host Status** - Up/Down
2. **Open Ports** - Port number, protocol, state
3. **Services** - Service name, version
4. **OS Guess** - Operating system (if detected)
5. **Vulnerabilities** - CVEs or security issues (if scanned)

**Format output:**
- Use tables for port listings
- Highlight critical findings
- Redact sensitive info if sharing
- Save full output to file

### 6) Security Recommendations

**For each open port/service:**

1. Is this service needed?
2. Is it properly secured?
3. Should it be exposed?
4. Are there known vulnerabilities?

**Common recommendations:**

| Port | Service | Risk | Recommendation |
|------|---------|------|----------------|
| 22 | SSH | Medium | Use key auth, disable root login |
| 23 | Telnet | HIGH | Disable, use SSH |
| 80 | HTTP | Low | Redirect to HTTPS |
| 443 | HTTPS | Low | Keep updated, use strong TLS |
| 3306 | MySQL | HIGH | Don't expose publicly |
| 5432 | PostgreSQL | HIGH | Don't expose publicly |
| 6379 | Redis | HIGH | Bind to localhost, auth required |
| 27017 | MongoDB | HIGH | Enable auth, don't expose |

### 7) Output Management

**Save results:**
```bash
# Normal output
nmap -oN scan_result.txt <target>

# XML output (for tools)
nmap -oX scan_result.xml <target>

# All formats
nmap -oA scan_result <target>
```

**Storage location:** `~/openclaw/workspace/nmap-scans/`

**Retention:** Delete after analysis unless needed for compliance

## Required Confirmations (Always)

Require explicit approval for:

1. **Before any scan** - Confirm authorization
2. **Before vulnerability scans** - Warn about impact
3. **Before OS detection** - May require sudo
4. **Before aggressive scans** - T4/T5 timing
5. **Before scanning multiple hosts** - Confirm range
6. **Before storing results** - Confirm location

## Safety Guidelines

### Do's:
✅ Scan only your own networks
✅ Start with gentle scans
✅ Document authorization
✅ Review results carefully
✅ Secure discovered vulnerabilities

### Don'ts:
❌ Scan without permission
❌ Scan critical infrastructure
❌ Use for malicious purposes
❌ Share results publicly
❌ Ignore legal boundaries

## Common Use Cases

### 1) Home Network Audit
```bash
# Discover all devices
nmap -sn 192.168.1.0/24

# Scan router
nmap -sV 192.168.1.1

# Scan your computers
nmap -A 192.168.1.X
```

### 2) Server Security Check
```bash
# Full port + service scan
nmap -p- -sV <server-ip>

# Vulnerability assessment
nmap --script vuln <server-ip>

# Check for common misconfigurations
nmap --script default,safe <server-ip>
```

### 3) Web Server Assessment
```bash
# HTTP/HTTPS ports
nmap -p 80,443,8080,8443 -sV --script http-* <target>

# SSL/TLS analysis
nmap --script ssl-enum-ciphers -p 443 <target>
```

## Nmap Script Engine (NSE)

**Safe script categories:**
- `default` - Safe, useful scripts
- `safe` - Won't crash services
- `discovery` - Information gathering
- `auth` - Authentication checks

**Use with caution:**
- `intrusive` - May crash services
- `vuln` - Vulnerability detection
- `exploit` - Actual exploits (avoid!)

**Example:**
```bash
# Safe comprehensive scan
nmap --script "default,safe,discovery" <target>

# Vulnerability scan (use carefully)
nmap --script "vuln" <target>
```

## Memory & Logging

**Log scans to:** `memory/nmap-scans/YYYY-MM-DD-<target>.md`

**Record:**
- Scan timestamp
- Target IP/range
- Scan type & command
- Authorization confirmation
- Key findings
- Recommendations

**Redact:**
- Public IPs (unless user's own)
- Service versions with known exploits
- Credentials or sensitive data

## Installation

**If nmap is not installed:**

```bash
# Debian/Ubuntu
sudo apt-get install nmap

# RHEL/CentOS
sudo yum install nmap

# macOS (Homebrew)
brew install nmap

# Arch Linux
sudo pacman -S nmap
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "command not found" | Install nmap |
| "permission denied" | Use sudo for OS detection |
| "host seems down" | Add `-Pn` to skip ping |
| "scan too slow" | Use `-F` or `-T4` |
| "too many false positives" | Use `-T3` or lower |

## Example Session

```
User: Scan my home network for security issues

Assistant: Before I proceed, I need to confirm:
1. Do you own this network or have permission to scan it?
2. What's your network range (e.g., 192.168.1.0/24)?
3. What type of scan would you like?

Options:
1. Quick discovery (find live hosts)
2. Basic port scan (top 1000 ports)
3. Full scan with service detection
4. Vulnerability assessment

User: Yes, it's my home network. 192.168.1.0/24. Option 3 please.

Assistant: Thanks for confirming. I'll run a comprehensive scan on 192.168.1.0/24.

This will:
- Scan top 1000 ports on each host
- Detect running services
- Attempt OS detection (may require sudo)
- Take 5-15 minutes depending on active hosts

Proceed? (yes/no)

User: yes

Assistant: Running scan... [executes nmap -A 192.168.1.0/24]

[Results presented in formatted table with recommendations]
```

---

**Remember:** With great scanning power comes great responsibility. Use this skill ethically and legally.
