# Nmap Scanner Skill for OpenClaw

Network scanning and security assessment using nmap.

## ⚠️ Legal Warning

**Only scan networks you own or have explicit written permission to scan.**

Unauthorized network scanning may violate computer crime laws in your jurisdiction.

---

## Installation

### 1. Install Nmap

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y nmap
```

**RHEL/CentOS:**
```bash
sudo yum install -y nmap
```

**macOS (Homebrew):**
```bash
brew install nmap
```

**Arch Linux:**
```bash
sudo pacman -S nmap
```

### 2. Verify Installation

```bash
nmap --version
```

### 3. Install the Skill

Copy or symlink the skill to OpenClaw's skills directory:

```bash
# Option 1: Copy
cp -r /home/ghost/.openclaw/workspace/skills/nmap-scanner \
      ~/.npm-global/lib/node_modules/openclaw/skills/

# Option 2: Symlink (recommended for development)
ln -s /home/ghost/.openclaw/workspace/skills/nmap-scanner \
      ~/.npm-global/lib/node_modules/openclaw/skills/nmap-scanner
```

### 4. Restart OpenClaw

```bash
openclaw gateway restart
```

---

## Usage

### Via OpenClaw Chat

Simply ask:

```
"Scan my home network 192.168.1.0/24"
"Check what ports are open on 192.168.1.1"
"Run a vulnerability scan on my server"
```

The skill will:
1. Confirm authorization
2. Ask for scan type
3. Execute the scan
4. Present results with recommendations

### Via CLI Tool

```bash
cd /home/ghost/.openclaw/workspace/skills/nmap-scanner
chmod +x nmap-scan.sh

# Basic scan
./nmap-scan.sh basic 192.168.1.1

# Full scan with service detection
./nmap-scan.sh comprehensive 192.168.1.1

# Vulnerability scan
./nmap-scan.sh vuln 10.0.0.1

# Host discovery
./nmap-scan.sh discovery 192.168.1.0/24
```

---

## Scan Types

| Type | Command | Description | Time |
|------|---------|-------------|------|
| `discovery` | `nmap -sn` | Find live hosts | Fast |
| `basic` | `nmap` | Top 1000 ports | Medium |
| `fast` | `nmap -F` | Top 100 ports | Fast |
| `full` | `nmap -p-` | All 65535 ports | Slow |
| `service` | `nmap -sV` | Service versions | Medium |
| `os` | `nmap -O` | OS detection | Medium |
| `comprehensive` | `nmap -A` | Full + services + OS | Slow |
| `vuln` | `nmap --script vuln` | Vulnerability scan | Very Slow |
| `stealth` | `nmap -sS` | SYN stealth scan | Medium |
| `udp` | `nmap -sU` | UDP ports | Very Slow |

---

## Output

Scans are saved to:
```
/home/ghost/.openclaw/workspace/skills/nmap-scanner/nmap-scans/
```

Formats:
- `.txt` - Human-readable
- `.xml` - Machine-readable (for tools)

---

## Common Use Cases

### 1. Home Network Audit

```bash
# Find all devices
./nmap-scan.sh discovery 192.168.1.0/24

# Scan router
./nmap-scan.sh comprehensive 192.168.1.1

# Scan your PC
./nmap-scan.sh service 192.168.1.100
```

### 2. Server Security Check

```bash
# Full port + service scan
./nmap-scan.sh full <server-ip>
./nmap-scan.sh service <server-ip>

# Vulnerability assessment
./nmap-scan.sh vuln <server-ip>
```

### 3. Web Server Analysis

```bash
# HTTP/HTTPS ports with scripts
nmap -p 80,443,8080 --script http-* <target>

# SSL/TLS analysis
nmap --script ssl-enum-ciphers -p 443 <target>
```

---

## Security Recommendations

### High-Risk Ports

| Port | Service | Risk | Action |
|------|---------|------|--------|
| 23 | Telnet | 🔴 HIGH | Disable, use SSH |
| 21 | FTP | 🔴 HIGH | Use SFTP instead |
| 3306 | MySQL | 🔴 HIGH | Don't expose publicly |
| 5432 | PostgreSQL | 🔴 HIGH | Don't expose publicly |
| 6379 | Redis | 🔴 HIGH | Bind localhost, add auth |
| 27017 | MongoDB | 🔴 HIGH | Enable auth |
| 11211 | Memcached | 🔴 HIGH | Never expose publicly |

### Medium-Risk Ports

| Port | Service | Risk | Action |
|------|---------|------|--------|
| 22 | SSH | 🟡 MEDIUM | Use key auth, disable root |
| 80 | HTTP | 🟡 MEDIUM | Redirect to HTTPS |
| 3389 | RDP | 🟡 MEDIUM | Use VPN, enable NLA |

### Low-Risk Ports

| Port | Service | Risk | Action |
|------|---------|------|--------|
| 443 | HTTPS | 🟢 LOW | Keep TLS updated |
| 53 | DNS | 🟢 LOW | Standard service |

---

## Safety Guidelines

### ✅ Do's

- Scan only your own networks
- Get written permission for client networks
- Start with gentle scans
- Document everything
- Secure discovered vulnerabilities

### ❌ Don'ts

- Scan without permission
- Scan government/military networks
- Scan your ISP's infrastructure
- Use for malicious purposes
- Share results publicly

---

## Troubleshooting

### "command not found: nmap"
Install nmap (see Installation section)

### "permission denied"
Some scans require sudo:
```bash
sudo nmap -O <target>  # OS detection
sudo nmap -sS <target> # SYN scan
```

### "host seems down"
Add `-Pn` to skip ping check:
```bash
nmap -Pn <target>
```

### "scan too slow"
Use faster options:
```bash
nmap -F <target>      # Top 100 ports
nmap -T4 <target>     # Aggressive timing
```

### "too many false positives"
Use slower, more accurate timing:
```bash
nmap -T3 <target>     # Normal timing (default)
nmap -T2 <target>     # Polite timing
```

---

## Nmap Script Engine (NSE)

### Safe Scripts
```bash
nmap --script "default,safe,discovery" <target>
```

### Vulnerability Scripts (use carefully)
```bash
nmap --script "vuln" <target>
nmap --script "exploit" <target>  # AVOID - actual exploits!
```

### Common Script Categories
- `default` - Safe, useful scripts
- `safe` - Won't crash services
- `discovery` - Information gathering
- `auth` - Authentication checks
- `vuln` - Vulnerability detection ⚠️
- `intrusive` - May crash services ⚠️

---

## License

This skill is provided for educational and authorized security testing purposes only.

---

## Resources

- [Nmap Official Docs](https://nmap.org/docs.html)
- [Nmap Script Engine](https://nmap.org/nsedoc/)
- [Nmap Cheat Sheet](https://hackertarget.com/nmap-cheatsheet-a-quick-reference-guide/)
