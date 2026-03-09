#!/bin/bash
# Nmap Scanner Tool - OpenClaw Skill Helper
# Usage: ./nmap-scan.sh <scan_type> <target> [output_file]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Scan types
SCAN_TYPES=(
    "discovery"      # Ping scan - host discovery
    "basic"          # Basic port scan (top 1000)
    "fast"           # Fast scan (top 100 ports)
    "full"           # Full port scan (all 65535)
    "service"        # Service version detection
    "os"             # OS detection (requires sudo)
    "comprehensive"  # Full + service + OS
    "vuln"           # Vulnerability scan
    "stealth"        # SYN stealth scan
    "udp"            # UDP scan
)

# Help message
show_help() {
    cat << EOF
${BLUE}Nmap Scanner Tool${NC}

Usage: $0 <scan_type> <target> [output_file]

Scan Types:
  ${GREEN}discovery${NC}     - Ping scan, find live hosts (nmap -sn)
  ${GREEN}basic${NC}         - Basic port scan, top 1000 ports (nmap <target>)
  ${GREEN}fast${NC}          - Fast scan, top 100 ports (nmap -F)
  ${GREEN}full${NC}          - Full port scan, all 65535 ports (nmap -p-)
  ${GREEN}service${NC}       - Service version detection (nmap -sV)
  ${GREEN}os${NC}            - OS detection, requires sudo (nmap -O)
  ${GREEN}comprehensive${NC} - Full scan with service & OS detection (nmap -A)
  ${GREEN}vuln${NC}          - Vulnerability scan (nmap --script vuln)
  ${GREEN}stealth${NC}       - SYN stealth scan (nmap -sS)
  ${GREEN}udp${NC}           - UDP scan (nmap -sU)

Examples:
  $0 discovery 192.168.1.0/24
  $0 basic 192.168.1.1
  $0 comprehensive 192.168.1.1 scan_result.txt
  $0 vuln 10.0.0.1

Output:
  Results saved to ./nmap-scans/ directory
  Formats: .txt (normal), .xml (machine-readable)

EOF
    exit 1
}

# Check if nmap is installed
check_nmap() {
    if ! command -v nmap &> /dev/null; then
        echo -e "${RED}Error: nmap is not installed${NC}"
        echo ""
        echo "Install with:"
        echo "  Ubuntu/Debian: sudo apt-get install nmap"
        echo "  RHEL/CentOS:   sudo yum install nmap"
        echo "  macOS:         brew install nmap"
        echo "  Arch:          sudo pacman -S nmap"
        exit 1
    fi
}

# Validate IP/hostname
validate_target() {
    local target=$1
    
    # Check if it's a valid IP, CIDR, or hostname
    if [[ $target =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}(/[0-9]{1,2})?$ ]]; then
        return 0
    elif [[ $target =~ ^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$ ]]; then
        return 0
    else
        return 1
    fi
}

# Create scan directory
setup_output_dir() {
    local scan_dir="./nmap-scans"
    mkdir -p "$scan_dir"
    echo "$scan_dir"
}

# Run the scan
run_scan() {
    local scan_type=$1
    local target=$2
    local output_file=$3
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local scan_dir=$(setup_output_dir)
    
    # Default output file if not specified
    if [ -z "$output_file" ]; then
        output_file="${scan_dir}/${timestamp}_${scan_type}_${target//[^a-zA-Z0-9]/_}.txt"
    fi
    
    local xml_output="${output_file%.txt}.xml"
    local normal_output="$output_file"
    
    echo -e "${BLUE}Starting nmap scan...${NC}"
    echo -e "Type: ${GREEN}$scan_type${NC}"
    echo -e "Target: ${GREEN}$target${NC}"
    echo -e "Output: ${GREEN}$normal_output${NC}"
    echo ""
    
    case $scan_type in
        discovery)
            echo -e "${YELLOW}Running host discovery scan...${NC}"
            nmap -sn "$target" -oN "$normal_output" -oX "$xml_output"
            ;;
        basic)
            echo -e "${YELLOW}Running basic port scan...${NC}"
            nmap "$target" -oN "$normal_output" -oX "$xml_output"
            ;;
        fast)
            echo -e "${YELLOW}Running fast scan (top 100 ports)...${NC}"
            nmap -F "$target" -oN "$normal_output" -oX "$xml_output"
            ;;
        full)
            echo -e "${YELLOW}Running full port scan (all 65535 ports)...${NC}"
            echo -e "${RED}This may take a while!${NC}"
            nmap -p- "$target" -oN "$normal_output" -oX "$xml_output"
            ;;
        service)
            echo -e "${YELLOW}Running service detection scan...${NC}"
            nmap -sV "$target" -oN "$normal_output" -oX "$xml_output"
            ;;
        os)
            echo -e "${YELLOW}Running OS detection scan...${NC}"
            echo -e "${RED}This requires sudo privileges!${NC}"
            sudo nmap -O "$target" -oN "$normal_output" -oX "$xml_output"
            ;;
        comprehensive)
            echo -e "${YELLOW}Running comprehensive scan...${NC}"
            echo -e "${RED}This may take 5-15 minutes!${NC}"
            nmap -A "$target" -oN "$normal_output" -oX "$xml_output"
            ;;
        vuln)
            echo -e "${YELLOW}Running vulnerability scan...${NC}"
            echo -e "${RED}WARNING: This scan may be intrusive!${NC}"
            nmap --script vuln "$target" -oN "$normal_output" -oX "$xml_output"
            ;;
        stealth)
            echo -e "${YELLOW}Running SYN stealth scan...${NC}"
            echo -e "${RED}This requires sudo privileges!${NC}"
            sudo nmap -sS "$target" -oN "$normal_output" -oX "$xml_output"
            ;;
        udp)
            echo -e "${YELLOW}Running UDP scan...${NC}"
            echo -e "${RED}UDP scans are very slow!${NC}"
            nmap -sU "$target" -oN "$normal_output" -oX "$xml_output"
            ;;
        *)
            echo -e "${RED}Unknown scan type: $scan_type${NC}"
            show_help
            ;;
    esac
    
    echo ""
    echo -e "${GREEN}Scan completed!${NC}"
    echo -e "Results saved to: ${BLUE}$normal_output${NC}"
    echo -e "XML output: ${BLUE}$xml_output${NC}"
    echo ""
    
    # Show summary
    if [ -f "$normal_output" ]; then
        echo -e "${BLUE}--- Quick Summary ---${NC}"
        grep -E "(Nmap scan report|Host is|PORT|STATE|Service|OS)" "$normal_output" | head -20
    fi
}

# Main
main() {
    if [ $# -lt 2 ]; then
        show_help
    fi
    
    local scan_type=$1
    local target=$2
    local output_file=${3:-""}
    
    # Check nmap
    check_nmap
    
    # Validate target
    if ! validate_target "$target"; then
        echo -e "${RED}Error: Invalid target '$target'${NC}"
        echo "Please provide a valid IP address, CIDR range, or hostname."
        exit 1
    fi
    
    # Run scan
    run_scan "$scan_type" "$target" "$output_file"
}

main "$@"
