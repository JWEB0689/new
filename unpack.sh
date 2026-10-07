#!/bin/sh
# Restore the firmware package from its base64 parts and unpack it.
# (Stored as parts because GitHub's API uploader mangles raw binaries.)
set -e
cd "$(dirname "$0")"
cat firmware/muse-gadget-cyd-firmware.zip.b64.part-* | base64 -d > muse-gadget-cyd-firmware.zip
unzip -o -q muse-gadget-cyd-firmware.zip
echo "done: muse-gadget-cyd-firmware/"
