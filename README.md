# MicroPython RGBWW Smart Bulb
tested on a Tuya WinnerMicro W600 Smart Bulb

## [VS Code Development guide](https://lemariva.com/blog/2019/08/micropython-vsc-ide-intellisense)

## Installation
1. Copy python files to board.
2. Reset the uC

## How to upload code remotely (WM uPython SDK)

1.  Create `wifi_config.py` with following content:
    ```python
    WIFI_SSID="<SSID>"
    WIFI_PASSWD="<PASSWORD>"
    ```
2.  Reboot the M600 and connect to bulb via FTP without username and password