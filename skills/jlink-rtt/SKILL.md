---
name: jlink-rtt
description: Read RTT debug output from firmware on boards with onboard J-Link programmers (Nordic DKs) where Segger CLI tools fail.
---

# J-Link RTT Skill

RTT console output for boards with onboard J-Link programmers (like Nordic DKs) where Segger's CLI tools (`JLinkRTTLogger`, `JLinkRTTClient`) fail to find the RTT control block.

**Humans:** Use Ozone instead - it handles RTT properly.

## Usage

```bash
# From a project directory (uses JLINK_DEVICE from Makefile)
python3 tools/jlink-rtt/jlink-rtt.py read     # dump RTT buffer
python3 tools/jlink-rtt/jlink-rtt.py status   # show buffer info
```

## How It Works

Reads RTT buffer directly via `JLinkExe` memory commands, bypassing the broken RTT discovery in Segger's CLI tools. Finds RTT address from the project's `.map` file.

## Firmware Config

```kconfig
CONFIG_USE_SEGGER_RTT=y
CONFIG_RTT_CONSOLE=y
CONFIG_UART_CONSOLE=n
CONFIG_SEGGER_RTT_SECTION_NONE=y
CONFIG_TRACING=n  # rtt-tracing snippet causes HardFault on nRF54
```
