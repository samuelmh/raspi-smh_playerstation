# PLAYERSTATION > Installation

## Download project
```bash
git clone https://github.com/samuelmh/raspi-smh_playerstation.git
```


## Raspberry Pi
*Note: tested on '2017-11-29-raspbian-stretch-lite.img'*

### How to install raspbian OS
From: https://www.raspberrypi.org/downloads/raspbian/
1. Download https://downloads.raspberrypi.org/raspbian_lite_latest
1. Build SD card
```bash
unzip 2017-11-29-raspbian-stretch-lite.zip
dd bs=4M if=2017-11-29-raspbian-stretch-lite.img of=/dev/sdb
```
1. Config SD card
 1. Host name (main partition) `etc/hostname`
 1. SSH server (boot partition) `touch boot/ssh`
 1. WiFi (optional, main partition) `etc/wpa_supplicant/wpa_supplicant.conf`
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
1. Run `sync` and unplug SD card.
1. Plug SD card in the raspberry pi and start.


## System packages
```bash
apt-get update
apt-get install python3.5 virtualenv git ffmpeg
```


## Install project
```bash
cd ~
git clone https://github.com/samuelmh/raspi-smh_playerstation.git
cd raspi-smh_playerstation
make install
```
