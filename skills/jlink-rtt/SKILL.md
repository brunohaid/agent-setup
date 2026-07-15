---
name: jlink-rtt
description: Read RTT debug output through an explicitly selected J-Link probe using firmware map metadata.
---

# J-Link RTT Skill

Use this fallback when Ozone is unavailable or SEGGER's RTT Logger/Client cannot discover the control block. It reads channel-zero metadata and ring-buffer bytes directly through J-Link Commander.

**Humans:** Prefer Ozone for interactive RTT. It handles connection state and live streaming more naturally.

## Safety and selection

- Run from the firmware project directory or pass `--project-dir` explicitly.
- **Always pass `--serial` when multiple J-Links are connected.** An exact device profile identifies an MCU type, not the physical probe.
- This helper does not erase, recover, unlock, reset, halt, or write target memory; its J-Link commands are memory reads only.

## Usage

```bash
# Spot through the LM20 DK onboard J-Link.
python3 ~/agent-setup/skills/jlink-rtt/jlink-rtt.py \
  --project-dir lights/spot/main \
  --serial 1051861032 \
  status
python3 ~/agent-setup/skills/jlink-rtt/jlink-rtt.py \
  --project-dir lights/spot/main \
  --serial 1051861032 \
  read

# Shelf Distribution through the external Compact PLUS.
# The exact STM device is discovered from MCU := STM32C562RE in its Makefile.
python3 ~/agent-setup/skills/jlink-rtt/jlink-rtt.py \
  --project-dir cabinet/retail/shelfdistribution \
  --serial 853006444 \
  status
python3 ~/agent-setup/skills/jlink-rtt/jlink-rtt.py \
  --project-dir cabinet/retail/shelfdistribution \
  --serial 853006444 \
  read

# Override metadata only when automatic device discovery is unavailable.
python3 ~/agent-setup/skills/jlink-rtt/jlink-rtt.py \
  --project-dir path/to/project \
  --device nRF54LM20A_M33 \
  --serial 1051861032 \
  read
```

On Windows, use the installed skill path, for example:

```bash
python C:/Users/bruno/.pi/agent/git/github.com/brunohaid/agent-setup/skills/jlink-rtt/jlink-rtt.py \
  --project-dir C:/Users/bruno/meso/firmware/lights/spot/main \
  --device nRF54LM20A_M33 \
  --serial 1051861032 \
  read
```

## Discovery behavior

The helper searches from `--project-dir` upward for:

- Zephyr device profile: `build/*/zephyr/runners.yaml`
- STM exact device profile: project `Makefile` variable `MCU`
- RTT symbol: `build/*/zephyr/zephyr.map` or `build/bin/firmware.map`

`status` prints the resolved project, map, device, physical probe serial, control block, and channel-zero offsets. Use it before `read` when diagnosing discovery.

## Firmware configuration

Zephyr:

```kconfig
CONFIG_USE_SEGGER_RTT=y
CONFIG_RTT_CONSOLE=y
CONFIG_UART_CONSOLE=n
CONFIG_SEGGER_RTT_SECTION_NONE=y
```

FreeRTOS projects need standalone SEGGER RTT linked into the image. In Meso firmware, selecting `MESOLIBS := logging` handles this automatically.

## Failure triage

- **RTT symbol not found:** build first and confirm `--project-dir` points at the controller, not the repository root.
- **Wrong target or attach failure:** verify `--serial` against passive programmer enumeration; do not guess from USB order.
- **Timeout while connecting:** inspect output for a J-Link OB firmware update, wait for the probe to re-enumerate, then retry `status`.
- **Empty output:** inspect `status` write/read offsets and confirm firmware emitted a log after reset.
