# MicroPython RGBWW Smart Bulb
tested on a Tuya [WinnerMicro W600-B800](https://w600.chip.haus/) Smart Bulb

## [VS Code Development guide](https://lemariva.com/blog/2019/08/micropython-vsc-ide-intellisense)

## Hardware flashing preperation
![TY5 W600 Pinout](images/board.jpg)
1. connect serial adapter to GND, VCC, RX0 and TX0
2. erase secboot and old image
   ```bash
   python3 -m w600tool -e -p /dev/ttyUSB0
   ```
3. connect PA0 (BOOT) to GND and reset chip by pulling RST low
4. flash MicroPython firmware
    ```bash
    python3 -m w600tool -p /dev/ttyUSB0 -u W60X_MicroPython_1.10_B1.3_IMG/wm_w600.fls
    ```
    ```
    Opening device: /dev/ttyUSB0
    Erasing secboot
    Switched speed to 2000000
    Uploading W60X_MicroPython_1.10_B1.3_IMG/wm_w600.fls
    0% [##############################] 100% | ETA: 00:00:00
    Total time elapsed: 00:00:15
    Reset board to run user code...
    ```
5. disconnect PA0 (BOOT) and reset the device
6. test Python shell with `screen /dev/ttyUSB0 115200` (press `CTRL-A` + `k` to quit)
    ```

    __            __
    \ \    /\    / /
     \ \  /  \  / /
      \ \/ /\ \/ /
       \  /  \  /
       / /\  / /\
      / /\ \/ /\ \
     / /  \  /  \ \
    /_/    \/    \_\

    WinnerMicro W600

    MicroPython v1.10-284-g2eee4e2-dirty on 2019-11-08; WinnerMicro module with W600
    Type "help()" for more information.
    >>> 
    ```

## Installation
1. In the python shell, connect to wifi and start FTP server:
    ```python
    >>> import easyw600
    >>> easyw600.scan()
    >>> easyw600.connect("<SSID>", "<PASSWORD>")
    conneting...
    connected, ip is 192.168.1.234
    >>> easyw600.ftpserver()
    ftpserver is running.
    ftp server port is 21, username is root, password is root
    ```
2. Copy python files to the board. For example via `ftp://root:root@192.168.1.234`
3. Reset the uC

## How to upload code remotely (WM uPython SDK)

1.  Create `wifi_config.py` with following content:
    ```python
    WIFI_SSID="<SSID>"
    WIFI_PASSWD="<PASSWORD>"
    ```
    This can also be done via the Python shell:
    ```python
    >>> f = open("wifi_config.py")
    >>> f.write('WIFI_SSID="<SSID>"\n')
    >>> f.write('WIFI_PASS="<PASSWORD>"\n')
    >>> f.close()
    ```
2.  Reboot the M600 and connect to bulb via FTP without username and password