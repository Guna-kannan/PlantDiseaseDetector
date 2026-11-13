#!/bin/bash
# ==============================================================================
# Unit 1: Basics of Linux & Essential Administration Utilities
# ==============================================================================
# Demonstrates:
#  1. System and OS inspection (RHEL/Linux kernel)
#  2. Essential tools: grep, tar, gzip, bzip2
#  3. File permissions (ugo / rwx)
#  4. Working with files and directories
#  5. Local storage & partition management (MBR vs GPT)
#  6. Managing users and groups
# ==============================================================================

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Unit 1: Linux Administration & Essential Utilities Demo ===${NC}\n"

# 1. OS & Kernel Details
echo -e "${GREEN}[1] System & OS Identification:${NC}"
uname -a
if [ -f /etc/os-release ]; then
    grep -E '^(NAME|VERSION)=' /etc/os-release
else
    echo "Running on $(uname -s)"
fi
echo ""

# 2. File Searching with grep
echo -e "${GREEN}[2] Text Processing & Pattern Searching with grep:${NC}"
echo "Searching for 'CLASS_NAMES' across src/:"
grep -rn "CLASS_NAMES" src/
echo ""

# 3. Archiving and Compression (tar, gzip, bzip2)
echo -e "${GREEN}[3] Archiving and Compression (tar, gzip, bzip2):${NC}"
DEMO_DIR="/tmp/linux_unit1_demo"
rm -rf "$DEMO_DIR"
mkdir -p "$DEMO_DIR/sample_data"
echo "Creating test files..."
echo "Sample Leaf Health Data" > "$DEMO_DIR/sample_data/leaf1.txt"
echo "Sample Blight Record" > "$DEMO_DIR/sample_data/leaf2.txt"

echo "Creating TAR archive:"
tar -cvf "$DEMO_DIR/sample.tar" -C "$DEMO_DIR" sample_data
ls -lh "$DEMO_DIR/sample.tar"

echo "Compressing with GZIP (.tar.gz):"
gzip -kf "$DEMO_DIR/sample.tar"
ls -lh "$DEMO_DIR/sample.tar.gz"

echo "Compressing with BZIP2 (.tar.bz2):"
if [ -x /usr/bin/bzip2 ]; then
    /usr/bin/bzip2 -kf "$DEMO_DIR/sample.tar"
elif command -v bzip2 &> /dev/null; then
    bzip2 -kf "$DEMO_DIR/sample.tar"
fi
ls -lh "$DEMO_DIR/sample.tar.bz2"
echo ""

# 4. File Permissions (ugo / rwx)
echo -e "${GREEN}[4] File Permissions (User / Group / Others & rwx):${NC}"
touch "$DEMO_DIR/secure_config.conf"
echo "Initial permissions:"
ls -l "$DEMO_DIR/secure_config.conf"

echo "Applying chmod u=rw,go=r (644):"
chmod u=rw,go=r "$DEMO_DIR/secure_config.conf"
ls -l "$DEMO_DIR/secure_config.conf"

echo "Applying chmod u+x (755):"
chmod u+x,go=rx "$DEMO_DIR/secure_config.conf"
ls -l "$DEMO_DIR/secure_config.conf"
echo ""

# 5. Local Storage & Disk Partitions (MBR vs GPT Overview)
echo -e "${GREEN}[5] Local Storage & Partition Architecture:${NC}"
echo "Inspecting mounted filesystems (df -h):"
df -h .
echo ""
echo -e "${YELLOW}Note on MBR vs GPT Partitioning:${NC}"
echo "  - MBR (Master Boot Record): Max 4 primary partitions, 2TB disk size limit, legacy BIOS."
echo "  - GPT (GUID Partition Table): Up to 128 partitions, 9.4 ZB capacity, CRC32 checksums, UEFI."
echo "  - Commands used on RHEL/Linux: 'lsblk', 'fdisk -l /dev/sda', 'parted /dev/sda print'"
echo ""

# 6. Users and Groups
echo -e "${GREEN}[6] User and Group Identification:${NC}"
echo "Current user identity (id):"
id
echo "Current user group memberships (groups):"
groups
echo ""
echo -e "${YELLOW}Commands for RHEL User Management:${NC}"
echo "  - Create user:  sudo useradd -m -s /bin/bash appuser"
echo "  - Create group: sudo groupadd appgroup"
echo "  - Add to group: sudo usermod -aG appgroup appuser"
echo ""

# Cleanup temporary demonstration files
rm -rf "$DEMO_DIR"

echo -e "${BLUE}=== Unit 1 Demonstration Completed Successfully ===${NC}"
