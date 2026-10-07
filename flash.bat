@echo off
REM Flash the Muse Gadget CYD firmware. Usage: flash.bat [COM port, e.g. COM5]
set PORT=%1
if "%PORT%"=="" (
  echo error: pass the COM port, e.g. flash.bat COM5
  exit /b 1
)
python -m esptool --chip esp32 -b 460800 --before default-reset ^
  --after hard-reset write-flash --flash-mode dio --flash-freq 80m ^
  -p %PORT% ^
  0x1000 bootloader.bin ^
  0x10000 partition-table.bin ^
  0x17000 ota_data_initial.bin ^
  0x19000 phy_init_data.bin ^
  0x20000 muse-gadget.bin
