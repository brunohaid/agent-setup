#!/usr/bin/env python3
"""Read SEGGER RTT buffers directly through a serial-pinned J-Link Commander."""

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


# Keep map patterns aligned with Zephyr/sysbuild and STM32 bare-metal outputs.
RTT_MAP_PATTERNS = ("build/*/zephyr/zephyr.map", "build/bin/firmware.map")
# Bound malformed control-block sizes before asking J-Link to dump target memory.
MAX_RTT_BUFFER_SIZE = 1024 * 1024


def find_jlink_exe() -> str:
    """Find J-Link Commander across Unix and Windows installs."""
    for name in ("JLinkExe", "JLink.exe"):
        path = shutil.which(name)
        if path:
            return path

    windows_default = Path(r"C:\Program Files\SEGGER\JLink\JLink.exe")
    if os.name == "nt" and windows_default.exists():
        return str(windows_default)

    return "JLinkExe"


def walk_to_root(start: Path):
    """Yield one directory and each parent so project-local metadata wins."""
    path = start.resolve()
    while True:
        yield path
        if path == path.parent:
            return
        path = path.parent


def find_jlink_device(start: Path) -> str | None:
    """Find an exact device from Zephyr runners or an STM project Makefile."""
    for path in walk_to_root(start):
        # Prefer generated runner metadata because it records the built Zephyr core.
        for runner_file in path.glob("build/*/zephyr/runners.yaml"):
            match = re.search(r"--device=([^\s]+)", runner_file.read_text())
            if match:
                return match.group(1)

        makefile = path / "Makefile"
        if not makefile.is_file():
            continue
        text = makefile.read_text()
        # Preserve compatibility with projects that still declare an explicit profile.
        match = re.search(r"^\s*JLINK_DEVICE\s*(?::|\?|\+)?=\s*(\S+)", text, re.MULTILINE)
        if match:
            return match.group(1)
        # STM projects already record the exact J-Link-compatible part in MCU.
        match = re.search(r"^\s*MCU\s*(?::|\?|\+)?=\s*(STM\S+)", text, re.MULTILINE)
        if match:
            return match.group(1)

    return None


def find_rtt_address(start: Path) -> tuple[int, Path] | None:
    """Find the RTT control-block address and source map file."""
    for path in walk_to_root(start):
        for pattern in RTT_MAP_PATTERNS:
            for mapfile in path.glob(pattern):
                match = re.search(r"(0x[0-9a-fA-F]+)\s+_SEGGER_RTT\b", mapfile.read_text())
                if match:
                    return int(match.group(1), 16), mapfile
    return None


def run_jlink(device: str, serial: str | None, commands: list[str]) -> str:
    """Run read commands through one explicitly selected probe when provided."""
    command = [find_jlink_exe()]
    if serial:
        command.extend(["-SelectEmuBySN", serial])
    command.extend(
        [
            "-NoGui",
            "1",
            "-ExitOnError",
            "1",
            "-Device",
            device,
            "-If",
            "SWD",
            "-Speed",
            "4000",
            "-AutoConnect",
            "1",
        ]
    )
    script = "\n".join(commands + ["q", ""])

    try:
        result = subprocess.run(
            command,
            input=script,
            capture_output=True,
            text=True,
            timeout=60,
        )
    except subprocess.TimeoutExpired as error:
        output = (error.stdout or "") + (error.stderr or "")
        raise RuntimeError(
            "J-Link timed out. It may be updating onboard probe firmware; "
            "wait for USB re-enumeration, verify the probe, and retry.\n" + output[-2000:]
        ) from error

    output = result.stdout + result.stderr
    if result.returncode != 0:
        raise RuntimeError(f"J-Link exited with {result.returncode}:\n{output[-4000:]}")
    return output


def parse_mem32(output: str) -> list[int]:
    """Parse 32-bit values from macOS/Linux and Windows Commander output."""
    values = []
    for line in output.splitlines():
        match = re.search(r"(?:^|J-Link>)([0-9A-Fa-f]{8})\s*=\s*(.*)", line)
        if not match:
            continue
        values.extend(int(value, 16) for value in re.findall(r"\b[0-9A-Fa-f]{8}\b", match.group(2)))
    return values


def parse_mem_bytes(output: str) -> bytearray:
    """Parse byte dumps without mistaking Commander's ASCII column for data."""
    data = bytearray()
    for line in output.splitlines():
        match = re.search(
            r"(?:^|J-Link>)[0-9A-Fa-f]{8}\s*=\s*((?:[0-9A-Fa-f]{2}\s+){1,16})",
            line,
        )
        if match:
            data.extend(int(value, 16) for value in match.group(1).split())
    return data


def resolve_context(args) -> tuple[Path, str, int, Path]:
    """Resolve project, target device, and map metadata with actionable errors."""
    project_dir = Path(args.project_dir).expanduser().resolve()
    if not project_dir.is_dir():
        raise RuntimeError(f"Project directory not found: {project_dir}")

    device = args.device or find_jlink_device(project_dir)
    if not device:
        raise RuntimeError(
            f"No J-Link device found from {project_dir}. "
            "Pass --device or build the project first."
        )

    rtt = find_rtt_address(project_dir)
    if not rtt:
        patterns = ", ".join(RTT_MAP_PATTERNS)
        raise RuntimeError(
            f"RTT symbol not found from {project_dir}. Build first; expected {patterns}."
        )
    rtt_addr, mapfile = rtt
    return project_dir, device, rtt_addr, mapfile


def read_buffer_info(device: str, serial: str | None, rtt_addr: int) -> tuple[int, int, int, int]:
    """Read channel-zero buffer pointer, size, write offset, and read offset."""
    output = run_jlink(device, serial, [f"mem32 {hex(rtt_addr + 0x18)} 5"])
    values = parse_mem32(output)
    if len(values) < 5:
        raise RuntimeError("Could not parse RTT channel-zero control block")

    buffer_addr, buffer_size, write_offset, read_offset = values[1:5]
    if buffer_addr == 0 or not 0 < buffer_size <= MAX_RTT_BUFFER_SIZE:
        raise RuntimeError(
            f"Invalid RTT buffer metadata: address={hex(buffer_addr)} size={buffer_size}"
        )
    if write_offset >= buffer_size or read_offset >= buffer_size:
        raise RuntimeError(
            f"Invalid RTT offsets: write={write_offset} read={read_offset} size={buffer_size}"
        )
    return buffer_addr, buffer_size, write_offset, read_offset


def cmd_read(args):
    """Read and display currently unread channel-zero RTT text."""
    _, device, rtt_addr, _ = resolve_context(args)
    buffer_addr, buffer_size, write_offset, read_offset = read_buffer_info(
        device, args.serial, rtt_addr
    )

    output = run_jlink(device, args.serial, [f"mem {hex(buffer_addr)} {buffer_size}"])
    data = parse_mem_bytes(output)
    if len(data) < buffer_size:
        raise RuntimeError(f"Read only {len(data)} of {buffer_size} RTT buffer bytes")
    data = data[:buffer_size]

    # RTT uses a ring, so concatenate wrapped unread data in chronological order.
    if write_offset >= read_offset:
        unread = data[read_offset:write_offset]
    else:
        unread = data[read_offset:] + data[:write_offset]

    text = bytes(unread).decode("utf-8", errors="replace")
    clean = "".join(char for char in text if char.isprintable() or char in "\n\r\t")
    if os.name == "nt":
        encoding = sys.stdout.encoding or "utf-8"
        clean = clean.encode(encoding, errors="ignore").decode(encoding, errors="ignore")
    print(clean, end="" if clean.endswith("\n") else "\n")


def cmd_status(args):
    """Show resolved target and RTT channel-zero metadata."""
    project_dir, device, rtt_addr, mapfile = resolve_context(args)
    buffer_addr, buffer_size, write_offset, read_offset = read_buffer_info(
        device, args.serial, rtt_addr
    )
    print(f"Project: {project_dir}")
    print(f"Map: {mapfile}")
    print(f"Device: {device}")
    print(f"Probe serial: {args.serial or 'automatic'}")
    print(f"RTT control block: {hex(rtt_addr)}")
    print(f"Buffer: {hex(buffer_addr)}, size: {buffer_size}")
    print(f"Write: {write_offset}, read: {read_offset}")


def parse_args():
    """Parse explicit project, device, and physical-probe selection."""
    parser = argparse.ArgumentParser(description="Serial-pinned direct J-Link RTT reader")
    parser.add_argument(
        "--project-dir",
        default=".",
        help="firmware project directory used for build metadata discovery (default: current directory)",
    )
    parser.add_argument("-d", "--device", help="exact J-Link device profile")
    parser.add_argument(
        "-s",
        "--serial",
        help="physical J-Link serial; always supply this when multiple probes are connected",
    )
    subparsers = parser.add_subparsers(dest="cmd", required=True)
    subparsers.add_parser("read", help="read current RTT channel-zero text")
    subparsers.add_parser("status", help="show resolved target and RTT buffer metadata")
    return parser.parse_args()


def main():
    """Dispatch the requested RTT operation with concise errors."""
    args = parse_args()
    try:
        {"read": cmd_read, "status": cmd_status}[args.cmd](args)
    except RuntimeError as error:
        raise SystemExit(f"Error: {error}") from error


if __name__ == "__main__":
    main()
