#!/usr/bin/env bash
# Flash the Muse Gadget CYD firmware. Usage: ./flash.sh [PORT]
set -euo pipefail
PORT="${1:-}"
if [ -z "$PORT" ]; then
  CANDIDATES=(/dev/ttyUSB* /dev/cu.usbserial-* /dev/cu.wchusbserial*)
  FOUND=()
  for g in "${CANDIDATES[@]}"; do
    for p in $g; do [ -e "$p" ] && FOUND+=("$p"); done
  done
  if [ "${#FOUND[@]}" -ne 1 ]; then
    echo "error: pass the serial port, e.g. ./flash.sh /dev/ttyUSB0 (found: ${FOUND[*]:-none})" >&2
    exit 1
  fi
  PORT="${FOUND[0]}"
fi
cd "$(dirname "$0")"
python3 -m esptool --chip esp32 -b 460800 --before default-reset \
  --after hard-reset write-flash --flash-mode dio --flash-freq 80m \
  -p "$PORT" \
  0x1000 bootloader.bin \
  0x10000 partition-table.bin \
  0x17000 ota_data_initial.bin \
  0x19000 phy_init_data.bin \
  0x20000 muse-gadget.bin
