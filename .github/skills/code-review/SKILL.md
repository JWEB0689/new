---
name: code-review
description: Comprehensive review guidelines for the ESP32 CYD Muse Gadget firmware and CI/CD release workflows. Use when reviewing pull requests or evaluating code changes in this repository.
---

# Code Review Guidelines for ESP32 CYD Firmware

When reviewing pull requests in this repository, evaluate changes against the following core requirements:

## 1. GitHub Actions & CI/CD (`.github/workflows/`)
- **ESP-IDF Environment Setup**: Any job invoking `idf.py` must use `shell: bash` and explicitly source the ESP-IDF environment export script (`. "$IDF_PATH/export.sh"`) before running build commands.
- **Container Consistency**: Builds run in the `espressif/idf:v6.0.1` container. Ensure toolchain compatibility when adding or modifying dependencies.
- **Board Port Integration**: Verify that board port files copied into the SDK (`board-port/esp32/` -> `sdk/`) preserve the target directory structure and do not overwrite essential SDK components unintentionally.
- **Secret & Token Safety**: Never log, echo, or commit `GADGET_SDK_TOKEN` or other private credentials. The token must only be injected via GitHub Secrets at build time into firmware artifacts.
- **Release Assets**: Verify that release jobs produce and package expected binaries (`bootloader.bin`, `partition-table.bin`, `ota_data_initial.bin`, `phy_init_data.bin`, `muse-gadget.bin`, and the zipped release package).

## 2. Firmware & Hardware Constraints (ESP32-2432S028R)
- **Flash Memory Limits**: The CYD board has 4 MB flash and no external PSRAM. Reject code that introduces excessive static buffers or bloated UI assets that exceed the 4 MB partition table.
- **Display & Peripherals (ILI9341)**: Verify GPIO allocations for the display, SPI bus, and touch/buttons match the CYD hardware pinout. Avoid blocking delays inside main loops or display refresh tasks.
- **Boot Button & Pairing Flow**: Preserve the single-button interaction model (short press for confirmation, 5-second hold for reset/unpair/Wi-Fi clear).
- **Flashing Scripts**: When modifying `flash.sh` or `flash.bat`, confirm flash addresses (`0x1000`, `0x10000`, `0x17000`, `0x19000`, `0x20000`), baud rates (460800 with 115200 fallback), and reset sequences.

## 3. Pull Request Review Output Format
Provide a concise, structured review:
1. **Summary & Recommendation**: Clearly state `Approval recommended` or `Changes requested`.
2. **Workflow & Firmware Impact**: Highlight any effect on CI builds, flash footprint, or board compatibility.
3. **Findings & Action Items**: Categorize by severity (`Critical`, `Warning`, `Suggestion`) with actionable code or YAML snippets.
