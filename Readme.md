# Kittenblock Extension for Raspberry Pi

This extension is for Raspberry Pi GPIO control.

## Usage

1. Install Kittenblock Raspberry Pi Extension
```
curl -sSL https://raw.githubusercontent.com/kittenbot/kext-rpi/master/install.sh | bash
```

2. The install script will install the extension to folder `kext-rpi` under your home directory. And it will also create a systemd service listening on port 8601. You can use `systemctl status kext-rpi` to check the status of the service.

3. Open Kittenblock in your browser with URL `http://your_raspberry_pi_ip:8601/`. You can either use the browser on your Raspberry Pi or use a browser on another computer in the same network.

4. Click the `Connect` button on the top left corner of the page to connect to the extension background service.

## Use Rosbot

1. You need to enable the serial port and **disable serial console** on your Raspberry Pi. You can config in the desktop perference or use command line `sudo raspi-config` then go to `Interfacing Options > Serial` to enable the serial port.

2. Set the jumpers next to USB port on the Rosbot to `RPI` mode.

3. Install the communication firmware to your Rosbot. You can find the firmware in this repository and we provide a helper script to install the firmware to your Rosbot. You can run the following command to install the firmware.

```
python arduino_upload.py
```

Press the reset button on the Rosbot and you will see the following message in the terminal.
```
bootloader  0.4 4
cpu name: ATmega328P
flash 0/31213
flash 128/31213
flash 256/31213
flash 384/31213
.....
```

To verify the firmware is installed correctly, you can run the following command to check the serial port.
The `M2` command will turn on/off the LED(Pin13) on the Rosbot.
```
echo "M2 13 0\r\n" > /dev/ttyAMA0
echo "M2 13 1\r\n" > /dev/ttyAMA0
```



| Note: To compile the communication firmware from source please refer to [kext-rosbot](https://github.com/KittenBot/kext-rosbot).
