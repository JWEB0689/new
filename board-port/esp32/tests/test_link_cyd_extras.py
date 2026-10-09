# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Host tests for the ESP32 CYD extras: display.text, touch-as-button, RGB LED."""

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class LinkCydExtrasTest(unittest.TestCase):
    def test_display_text_is_advertised(self):
        noise = (ROOT / "main/noise_control.cpp").read_text()
        self.assertIn('"display.text"', noise)
        # Registered next to the other display commands, with a text parameter.
        start = noise.index('"display.text"')
        block = noise[max(0, start - 600):start]
        self.assertIn("text_required", block)
        self.assertIn("CONFIG_HOMEHUB_DISPLAY", block)

    def test_display_text_is_handled(self):
        app = (ROOT / "main/app.c").read_text()
        start = app.index('"display.text"')
        block = app[start:start + 700]
        self.assertIn("led_status_set_title", block)
        self.assertIn("led_status_show_animation", block)
        self.assertIn("missing_param", block)

    def test_touch_tap_bridges_to_button(self):
        button_c = (ROOT / "main/button.c").read_text()
        self.assertIn("void button_touch_tap(void)", button_c)
        self.assertIn("s_short_press_cb", button_c)
        button_h = (ROOT / "main/button.h").read_text()
        self.assertIn("void button_touch_tap(void);", button_h)
        led = (ROOT / "main/led_status.c").read_text()
        self.assertIn("button_touch_tap()", led)

    def test_cyd_rgb_led_pins_and_polarity(self):
        led = (ROOT / "main/led_status.c").read_text()
        # Common-anode RGB LED: R=4, G=16, B=17, active low.
        self.assertIn("#define CYD_LED_R_GPIO   4", led)
        self.assertIn("#define CYD_LED_G_GPIO   16", led)
        self.assertIn("#define CYD_LED_B_GPIO   17", led)
        self.assertIn("255 - c.r * 255", led)

    def test_cyd_touch_pins(self):
        led = (ROOT / "main/led_status.c").read_text()
        # XPT2046 on its own SPI bus: SCLK=25, MOSI=32, MISO=39, CS=33.
        self.assertIn("#define CYD_TOUCH_SCLK_GPIO 25", led)
        self.assertIn("#define CYD_TOUCH_MOSI_GPIO 32", led)
        self.assertIn("#define CYD_TOUCH_MISO_GPIO 39", led)
        self.assertIn("#define CYD_TOUCH_CS_GPIO   33", led)
        self.assertIn("SPI3_HOST", led)

    def test_owner_name_personalization(self):
        kconfig = (ROOT / "main/Kconfig.projbuild").read_text()
        self.assertIn("config GADGET_OWNER_NAME", kconfig)
        overlay = (ROOT / "devices/sdkconfig.cyd").read_text()
        self.assertIn('CONFIG_HOMEHUB_BLE_NAME_SUFFIX="-Jeremy"', overlay)
        self.assertIn('CONFIG_GADGET_OWNER_NAME="Jeremy"', overlay)


if __name__ == "__main__":
    unittest.main()
