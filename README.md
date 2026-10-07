# Muse Gadget firmware for ESP32 CYD (ESP32-2432S028R)

> **GitHub note:** the firmware lives in `muse-gadget-cyd-firmware.zip.b64`
> (base64-encoded, because GitHub's uploader mangles raw binaries). Run
> `./unpack.sh` to restore and unpack the zip, then flash as below.

Built from `facebookincubator/muse-gadget-sdk` (esp32) with a community
board port for the Cheap Yellow Display: status shown on the 2.8" ILI9341
screen, BOOT button for pairing confirmation. Your SDK token is baked into
`muse-gadget.bin` — keep these files private.

## Flash with esptool

Install: `pip install esptool`

Plug in the CYD with a data USB cable, then run (replace PORT):

```sh
python -m esptool --chip esp32 -b 460800 --before default-reset \
  --after hard-reset write-flash --flash-mode dio --flash-freq 80m \
  0x1000 bootloader.bin \
  0x10000 partition-table.bin \
  0x17000 ota_data_initial.bin \
  0x19000 phy_init_data.bin \
  0x20000 muse-gadget.bin
```

Linux port: `/dev/ttyUSB0` (or similar). macOS: `/dev/cu.usbserial-*`
or `/dev/cu.wchusbserial*`. If flashing can't connect: hold BOOT, tap
RESET, release BOOT, and run the command again. If the baud rate fails,
retry with `-b 115200`.

Or use the flash scripts: `flash.sh` (macOS/Linux) / `flash.bat` (Windows).

## Pair with the Muse app

1. Power the CYD — the screen breathes orange when ready for setup.
2. Muse app: **Settings > Devices**, turn on **Developer mode**.
3. **Add Device** (+, top right), pick `MuseGadget-Disp-XXXXXX`.
4. When the screen breathes blue, press the **BOOT** button to confirm.
5. Green = connected.

To start over: hold the button 5 seconds (unpair + forget Wi-Fi).

## Notes

- This is a status-screen build: you get the connection status, agent name,
  and images Muse sends. No full UI/avatar (the CYD's 4 MB flash can't fit
  it) and no home-network tunnel (no PSRAM) — Muse still reaches and
  controls the gadget.
- Flashing custom firmware can brick boards. Proceed at your own risk.
