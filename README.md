# Muse Gadget firmware for ESP32 CYD (ESP32-2432S028R)

A community board port that builds Meta's
[`muse-gadget-sdk`](https://github.com/facebookincubator/muse-gadget-sdk)
(ESP32) for the Cheap Yellow Display, so the CYD pairs with the Muse app as a
Muse Gadget.

## What it does

- **Status screen** on the 2.8" ILI9341 display: connection state as coloured
  bars, a pixel-art animation, and the agent's name (your owner name at boot).
- **RGB status LED** — the CYD's onboard RGB LED mirrors the status colour,
  including the breathing animations (orange = setting up, blue = confirm
  pairing, green = connected).
- **Tap to confirm** — tapping the touch screen works like the BOOT button:
  confirm a pending pairing, or reopen the setup window while unpaired.
- **Images and text from Muse** — `display.draw_url` shows an image,
  `display.text` shows a short line of text as the screen title,
  `display.show_animation` restores the animation and agent name.
- Personalized BLE name: `MuseGadget-Jeremy-XXXXXX` (set in
  `board-port/esp32/devices/sdkconfig.cyd`).

Limits: no full UI/avatar (4 MB flash), no home-network tunnel (no PSRAM).
Muse still reaches and controls the gadget over the control session.

## Repository layout

- `board-port/` — the CYD overlay. Copy it over a clone of
  `muse-gadget-sdk` at the pinned commit (see the workflow), then build.
- `flash.sh` / `flash.bat` — flash scripts (auto-detect the serial port).
- `.github/workflows/build-release.yml` — builds the firmware in the
  `espressif/idf:v6.0.1` container and publishes a GitHub Release with
  `muse-gadget-cyd-firmware.zip`.

## Build it yourself

Prerequisites: ESP-IDF **v6.0.1** (other versions are unsupported), Python 3,
and your SDK token (`mgst_…`) from
[gadgets.muse.ai](https://gadgets.muse.ai/settings/sdk-tokens) (Account → SDK
tokens). Every gadget needs a token to pair.

```sh
git clone https://github.com/facebookincubator/muse-gadget-sdk.git sdk
git -C sdk checkout b139b45064b4dcecf7bfe97e75bc7f99c10c28b6
cp -a board-port/. sdk/
printf 'CONFIG_GADGET_SDK_TOKEN="mgst_…"\n' > /tmp/sdkconfig.token
cd sdk/esp32
. ~/esp/esp-idf-v6.0.1/export.sh
idf.py -B build-cyd -DIDF_TARGET=esp32 \
  -DSDKCONFIG="$PWD/build-cyd/sdkconfig" \
  -DSDKCONFIG_DEFAULTS="sdkconfig.defaults;devices/sdkconfig.cyd;/tmp/sdkconfig.token" \
  build
```

Or let GitHub do it: add your token as a repository secret named
`GADGET_SDK_TOKEN` (Settings → Secrets and variables → Actions), then run the
**Build CYD firmware** workflow from the Actions tab (or push a `v*` tag). It
builds, packages, and publishes the release automatically. The token is baked
in at build time and is never committed.

## Flash it

You need the release zip (or the `build-cyd/` outputs): `bootloader.bin`,
`partition-table.bin`, `ota_data_initial.bin`, `phy_init_data.bin`,
`muse-gadget.bin`, plus `flash.sh` / `flash.bat`.

Install esptool (`pip install esptool`), plug the CYD in with a **data** USB
cable, then:

```sh
./flash.sh            # auto-detects the port (macOS/Linux)
```

or with esptool directly (replace PORT):

```sh
python3 -m esptool --chip esp32 -b 460800 --before default-reset \
  --after hard-reset write-flash --flash-mode dio --flash-freq 80m \
  -p PORT \
  0x1000 bootloader.bin \
  0x10000 partition-table.bin \
  0x17000 ota_data_initial.bin \
  0x19000 phy_init_data.bin \
  0x20000 muse-gadget.bin
```

Port names: Linux `/dev/ttyUSB0`, macOS `/dev/cu.usbserial-*` or
`/dev/cu.wchusbserial*` (install the CH340 driver if nothing appears),
Windows `COMx`. If flashing can't connect: hold BOOT, tap RESET, release
BOOT, and run it again. If the high baud rate fails, retry with `-b 115200`.
On macOS 15 you may need to Allow the accessory in
System Settings → Privacy & Security.

Reflashing keeps pairing and Wi-Fi credentials (NVS is left alone).

## Pair it with the Muse app

1. Power the CYD — the screen and RGB LED breathe **orange** when ready.
2. Muse app: **Settings > Devices**, turn on **Developer mode**.
3. **Add Device** (+, top right), pick `MuseGadget-Jeremy-XXXXXX`.
4. When the screen breathes **blue**, **tap the screen** (or press BOOT) to confirm.
5. **Green** = connected.

To start over: hold BOOT for 5 seconds (unpair + forget Wi-Fi).

## Notes

- Flashing custom firmware can brick boards. Proceed at your own risk.
- Back up the stock firmware first if you want it:
  `esptool --chip esp32 -p PORT read-flash 0 0x400000 cyd-stock-backup.bin`
- The firmware is signed with the SDK's dev signing key; Secure Boot stays
  off so the board can be reflashed freely.
