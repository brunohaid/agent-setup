---
name: saleae
description: Control and diagnose Saleae Logic analyzers through Logic 2, its Automation API, or MCP. Use for captures, protocol decoding, exports, triggers, and continuous visual monitoring.
---

# Saleae Skill

Use Saleae Logic 2's UI for interactive monitoring and its APIs for bounded, owned automation. Do not try to reproduce oscilloscope-style continuous monitoring by repeatedly creating API captures.

## Choose the correct interface

| Goal | Interface |
|------|-----------|
| Watch signals continuously with stable zoom and decoded history | Logic 2 UI using Looping mode, a built-in analyzer, Data Table, and optionally Trigger View |
| Run one bounded capture, decode it, export it, or save it | Python Automation API or MCP |
| Trigger once on a raw digital edge or pulse | UI Trigger mode, Automation, or MCP |
| Re-center the live view repeatedly on decoded protocol values | UI Trigger View |

Trigger View moves or freezes the viewport on each matching protocol result while the underlying capture continues. Confirm continuation from the Stop control, capture memory/time, or growing Data Table. Identical transactions can make repeated view triggers appear stationary.

## Safety and capture ownership

- **Never implement continuous monitoring as a loop around `start_capture()`.** Every call creates a new Logic 2 session/tab and can exhaust the computer.
- Track every capture ID or `Capture` object created by the current workflow and close it in `finally` or a context manager.
- Stop or close only captures created by the current workflow. Do not stop a UI-owned capture or quit Logic 2 without explicit permission.
- Use bounded timers and memory buffers for unattended automation.
- `start_capture()` ignores the active tab's channels, analyzers, zoom, and other UI settings.
- Automation capture methods other than `wait()` or `stop()` must wait until recording ends. Adding an analyzer while recording can block until timeout.
- A UI-started recording can prevent API session switching with `Cannot switch sessions while recording`; ask the user to stop it.
- Prefer Saleae's built-in protocol analyzers. Add a custom HLA only when it performs requested protocol semantics, not merely different formatting.

## Default local endpoints

Enable both servers in **Logic 2 → Settings → Automation**.

| Service | Default endpoint | Transport |
|---------|------------------|-----------|
| Automation | `127.0.0.1:10430` | gRPC; not HTTP |
| MCP | `http://127.0.0.1:10530` | MCP Streamable HTTP using POST |

An HTTP GET to port 10430 returns binary gRPC bytes rather than a web response. A GET to the MCP endpoint normally returns HTTP 405; use an MCP client or JSON-RPC POST.

## Inspect Logic 2 and connected devices

Use the project's existing Python environment when it already contains `logic2-automation`:

```bash
python - <<'PY'
from saleae import automation

with automation.Manager.connect(port=10430) as manager:
    print(manager.get_app_info())
    for device in manager.get_devices():
        print(device)
PY
```

Do not hardcode the first device when multiple analyzers are connected. Select the intended `device_id` explicitly.

## Bounded Automation capture pattern

```python
from saleae import automation

with automation.Manager.connect(port=10430) as manager:
    device_configuration = automation.LogicDeviceConfiguration(
        enabled_digital_channels=[0, 1],
        digital_sample_rate=10_000_000,
    )
    capture_configuration = automation.CaptureConfiguration(
        buffer_size_megabytes=64,
        capture_mode=automation.TimedCaptureMode(duration_seconds=3.0),
    )

    with manager.start_capture(
        device_id="DEVICE_SERIAL",
        device_configuration=device_configuration,
        capture_configuration=capture_configuration,
    ) as capture:
        capture.wait()
        analyzer = capture.add_analyzer(
            "I2C",
            settings={"SCL": 1, "SDA": 0},
        )
        capture.export_data_table("/absolute/path/i2c.csv", [analyzer])
```

Use `wait()` only for timed or digital-trigger captures. Use `stop()` for manual captures; never call both on one capture.

## MCP access

Prefer a configured MCP client. The endpoint supports `initialize`, `tools/list`, and `tools/call`. For a raw diagnostic request, POST JSON-RPC with both accepted response types and preserve `Mcp-Session-Id` if the server returns one:

```bash
curl -i http://127.0.0.1:10530 \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  --data '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"saleae-client","version":"1"}}}'
```

Inspect `tools/list` instead of assuming tool names or argument schemas. Current Logic 2 releases expose capture lifecycle, analyzer, save/load, and export tools, but not Trigger View or control of an existing configured UI tab.

## Continuous visual monitoring

In one Logic 2 tab:

1. Select **Looping** capture mode and set a bounded memory buffer.
2. Enable only the required channels and choose a suitable sample rate.
3. Add the built-in protocol analyzer and map its signals.
4. Open the analyzer Data Table and keep it at the end for recent decoded frames.
5. Optionally enable Trigger View, choose the analyzer, query, and holdoff.
6. Start and stop this same UI session instead of creating API captures.

Raw digital edge/pulse Trigger mode is one-shot. Trigger View is the continuous decoded-protocol view feature. The APIs do not currently expose Trigger View.

## Official documentation

The documentation site publishes machine-readable Markdown as plain-text `llms-*.txt` files:

- Documentation index: https://docs.saleae.com/
- Machine-readable index: https://docs.saleae.com/llms.txt
- Complete machine-readable docs: https://docs.saleae.com/llms-full.txt
- Automation: https://docs.saleae.com/llms-automation.txt
- MCP: https://docs.saleae.com/llms-mcp.txt
- Extensions: https://docs.saleae.com/llms-extensions.txt
- MSO API: https://docs.saleae.com/llms-mso-api.txt
- Logic 2 support: https://www.saleae.com/support
- Capture modes and Trigger View: https://www.saleae.com/support/logic-software/capturing-data/capture-modes
