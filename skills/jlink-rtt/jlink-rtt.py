#!/usr/bin/env python3
"""
J-Link RTT reader - CLI fallback when Ozone isn't available.
Reads RTT buffer directly via JLinkExe memory commands.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

def find_jlink_device() -> str | None:
    """Find JLINK_DEVICE from nearest Makefile."""
    path = Path.cwd()
    while path != path.parent:
        makefile = path / "Makefile"
        if makefile.exists():
            match = re.search(r'JLINK_DEVICE\s*[:?]?=\s*(\S+)', makefile.read_text())
            if match:
                return match.group(1)
        path = path.parent
    return None

def find_rtt_address() -> int | None:
    """Find RTT control block address from .map file."""
    path = Path.cwd()
    while path != path.parent:
        for pattern in ["build/*/zephyr/zephyr.map", "build/bin/firmware.map"]:
            for mapfile in path.glob(pattern):
                match = re.search(r'(0x[0-9a-fA-F]+)\s+_SEGGER_RTT\b', mapfile.read_text())
                if match:
                    return int(match.group(1), 16)
        path = path.parent
    return None

def run_jlink(device: str, commands: list[str]) -> str:
    """Run JLink commands."""
    script = "\n".join(commands + ["exit"])
    result = subprocess.run(
        ["JLinkExe", "-Device", device, "-If", "SWD", "-Speed", "4000", "-AutoConnect", "1"],
        input=script, capture_output=True, text=True, timeout=10
    )
    return result.stdout

def parse_mem32(output: str) -> list[int]:
    """Parse mem32 output, collecting values from all lines."""
    values = []
    for line in output.split('\n'):
        if re.match(r'^[0-9A-Fa-f]{8}\s*=', line):
            for v in re.findall(r'([0-9A-Fa-f]{8})', line.split('=')[1]):
                values.append(int(v, 16))
    return values

def cmd_read(args):
    """Read and display RTT buffer contents."""
    device = args.device or find_jlink_device()
    if not device:
        sys.exit("Error: No device specified and JLINK_DEVICE not found in Makefile")
    
    rtt_addr = find_rtt_address()
    if not rtt_addr:
        sys.exit("Error: RTT address not found. Build firmware first (need .map file)")
    
    # Read buffer info: skip sName, get pBuffer, size, WrOff
    output = run_jlink(device, [f"mem32 {hex(rtt_addr + 0x18)} 4"])
    values = parse_mem32(output)
    if len(values) < 4:
        sys.exit("Error: Could not read RTT buffer info")
    
    buf_addr = values[1]
    buf_size = values[2]
    
    # Read buffer contents
    output = run_jlink(device, [f"mem {hex(buf_addr)} {buf_size}"])
    
    # Parse hex dump to text
    data = bytearray()
    for line in output.split('\n'):
        match = re.match(r'[0-9A-Fa-f]+\s*=\s*((?:[0-9A-Fa-f]{2}\s*)+)', line)
        if match:
            for b in match.group(1).split():
                if len(b) == 2:
                    try: data.append(int(b, 16))
                    except: pass
    
    # Print readable text
    text = bytes(data).decode('utf-8', errors='replace')
    # Filter to printable + newlines
    print(''.join(c for c in text if c.isprintable() or c in '\n\r\t'))

def cmd_status(args):
    """Show RTT buffer status."""
    device = args.device or find_jlink_device()
    if not device:
        sys.exit("Error: No device specified and JLINK_DEVICE not found in Makefile")
    
    rtt_addr = find_rtt_address()
    if not rtt_addr:
        sys.exit("Error: RTT address not found. Build firmware first.")
    
    output = run_jlink(device, [f"mem32 {hex(rtt_addr + 0x18)} 5"])
    values = parse_mem32(output)
    
    if len(values) >= 5:
        print(f"RTT Control Block: {hex(rtt_addr)}")
        print(f"Buffer: {hex(values[1])}, Size: {values[2]}")
        print(f"Write: {values[3]}, Read: {values[4]}")

def main():
    parser = argparse.ArgumentParser(description="J-Link RTT reader (CLI fallback)")
    parser.add_argument("-d", "--device", help="J-Link device (default: from Makefile)")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("read", help="Read RTT buffer")
    sub.add_parser("status", help="Show RTT status")
    
    args = parser.parse_args()
    {"read": cmd_read, "status": cmd_status}[args.cmd](args)

if __name__ == "__main__":
    main()
