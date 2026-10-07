#!/bin/sh
# Restore the firmware package from its base64 encoding and unpack it.
# (The .zip is stored base64-encoded because GitHub's file uploader mangles raw binaries.)
set -e
cd "$(dirname "$0")"
base64 -d muse-gadget-cyd-firmware.zip.b64 > muse-gadget-cyd-firmware.zip
unzip -o -q muse-gadget-cyd-firmware.zip
echo "done: muse-gadget-cyd-firmware/"
