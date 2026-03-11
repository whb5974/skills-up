#!/bin/bash
# Nmap Scanner Skill Installer
# Usage: ./install.sh

set -e

SKILL_NAME="nmap-scanner"
SKILL_SOURCE="/home/ghost/.openclaw/workspace/skills/$SKILL_NAME"
SKILL_TARGET="$HOME/.npm-global/lib/node_modules/openclaw/skills/$SKILL_NAME"

echo "🔧 Installing Nmap Scanner Skill for OpenClaw"
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "⚠️  Please don't run as root. This script will use sudo when needed."
    exit 1
fi

# Step 1: Check if nmap is installed
echo "📦 Checking nmap installation..."
if command -v nmap &> /dev/null; then
    echo "✅ nmap is already installed"
    nmap --version | head -1
else
    echo "❌ nmap is not installed"
    echo ""
    echo "Installing nmap..."
    
    # Detect OS
    if [ -f /etc/debian_version ]; then
        echo "Detected Debian/Ubuntu"
        sudo apt-get update
        sudo apt-get install -y nmap
    elif [ -f /etc/redhat-release ]; then
        echo "Detected RHEL/CentOS"
        sudo yum install -y nmap
    elif [ "$(uname)" == "Darwin" ]; then
        echo "Detected macOS"
        if command -v brew &> /dev/null; then
            brew install nmap
        else
            echo "❌ Homebrew not found. Please install it first:"
            echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
            exit 1
        fi
    else
        echo "⚠️  Unknown OS. Please install nmap manually:"
        echo "   Ubuntu/Debian: sudo apt-get install nmap"
        echo "   RHEL/CentOS:   sudo yum install nmap"
        echo "   macOS:         brew install nmap"
        echo "   Arch:          sudo pacman -S nmap"
        exit 1
    fi
    
    echo "✅ nmap installed successfully"
fi

# Verify nmap
echo ""
echo "🔍 Verifying nmap installation..."
nmap --version | head -1

# Step 2: Install the skill
echo ""
echo "📚 Installing skill to OpenClaw..."

if [ -d "$SKILL_SOURCE" ]; then
    # Check if skill already exists
    if [ -L "$SKILL_TARGET" ]; then
        echo "✅ Skill is already installed (symlink)"
        read -p "Update symlink? (y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 0
        fi
        rm -f "$SKILL_TARGET"
    elif [ -d "$SKILL_TARGET" ]; then
        echo "⚠️  Skill already exists as directory"
        read -p "Replace with symlink? (y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "Keeping existing directory."
            SKILL_TARGET="$SKILL_TARGET.bak.$(date +%Y%m%d_%H%M%S)"
            echo "Backing up to: $SKILL_TARGET"
            mv "${SKILL_TARGET%.bak.*}" "$SKILL_TARGET"
        else
            rm -rf "$SKILL_TARGET"
        fi
    fi
    
    # Create symlink
    echo "Creating symlink: $SKILL_TARGET -> $SKILL_SOURCE"
    ln -s "$SKILL_SOURCE" "$SKILL_TARGET"
    echo "✅ Skill installed (symlink)"
else
    echo "❌ Skill source not found: $SKILL_SOURCE"
    exit 1
fi

# Step 3: Create output directory
echo ""
echo "📁 Creating scan output directory..."
mkdir -p "$SKILL_SOURCE/nmap-scans"
echo "✅ Output directory created: $SKILL_SOURCE/nmap-scans"

# Step 4: Make scripts executable
echo ""
echo "🔨 Setting permissions..."
chmod +x "$SKILL_SOURCE/nmap-scan.sh"
chmod +x "$SKILL_SOURCE/install.sh"
echo "✅ Scripts are executable"

# Step 5: Restart OpenClaw Gateway
echo ""
echo "🔄 OpenClaw Gateway restart required"
read -p "Restart OpenClaw Gateway now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Restarting OpenClaw Gateway..."
    openclaw gateway restart
    echo "✅ Gateway restarted"
else
    echo "⚠️  Please restart OpenClaw Gateway manually:"
    echo "   openclaw gateway restart"
fi

# Step 6: Test installation
echo ""
echo "🧪 Testing installation..."
if [ -d "$SKILL_TARGET" ]; then
    echo "✅ Skill directory exists"
else
    echo "❌ Skill directory not found"
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Nmap Scanner Skill installed successfully!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Usage:"
echo "  1. Ask OpenClaw: 'Scan my network 192.168.1.0/24'"
echo "  2. Or use CLI: cd $SKILL_SOURCE && ./nmap-scan.sh basic <target>"
echo ""
echo "Documentation: $SKILL_SOURCE/README.md"
echo "Skill file:    $SKILL_SOURCE/SKILL.md"
echo ""
echo "⚠️  Remember: Only scan networks you own or have permission to scan!"
echo ""
