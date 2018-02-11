# SMH_PLAYERSTATION > Installation

## Download project
```bash
git clone https://github.com/samuelmh/raspi-smh_playerstation.git
```


## Raspberry Pi
*Note: tested on* `2017-11-29-raspbian-stretch-lite.img`

### How to install raspbian OS
From: https://www.raspberrypi.org/downloads/raspbian/
1. Download the OS https://downloads.raspberrypi.org/raspbian_lite_latest
1. Build the SD card
```bash
unzip 2017-11-29-raspbian-stretch-lite.zip
dd bs=4M if=2017-11-29-raspbian-stretch-lite.img of=/dev/sdb
```
1. Configure the SD card
  * Host name (main partition) `etc/hostname`
  * SSH server (boot partition) `touch boot/ssh`
  * WiFi (optional, main partition) `etc/wpa_supplicant/wpa_supplicant.conf`
 ```
network={
 ssid="YOUR_NETWORK_NAME"
 psk="YOUR_NETWORK_PASSWORD"
 proto=RSN
 key_mgmt=WPA-PSK
 pairwise=CCMP
 auth_alg=OPEN
}
 ```
1. Run `sync`, wait and and unplug the SD card.
1. Plug the SD card into the raspberry pi and start.


## System packages
```bash
sudo apt-get update
sudo apt-get install python3.6 virtualenv git ffmpeg
```

## Install the project
```bash
cd ~
git clone https://github.com/samuelmh/raspi-smh_playerstation.git
cd raspi-smh_playerstation
make install
```

At this point you should be able to run:
```bash
make run-webserver
```
And have a working server on the port 8000.
