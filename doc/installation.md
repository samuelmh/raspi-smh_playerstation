# SMH_PLAYERSTATION > Installation

## Table of Contents
* [Docker running](#docker)
* [Manual installation (Developers & Raspberry Pi)](#manual)

## Docker running <a name="docker"></a>
This is the preferred method if you just want to run the program. I have built an image (with the latest stable version) so the program will run isolated in a container. You just download the image, run it and enjoy!

*NOTE: it has been tested on Linux, if you use Windows check out  [Docker for Windows](https://docs.docker.com/docker-for-windows/install/). As I am not a Windows user, I cannot guarantee it works on such system.*

### Directories
These is the directory the program will use.
* `smh_playerstation` will be the directory for our project
* `smh_playerstation/songs` is where you put your songs. The program will index all the songs under this path.
* `smh_playerstation/songs/youtube` will have the songs downloaded from Youtube.
* `smh_playerstation/encoded` will have all the encoded songs. For example when a youtube song is encoded into a .mp3 file.

Create the previous directories by hand or just run:
```bash
mkdir ~/smh_playerstation
```

### Run it!
Run a docker container to start the server. This will download the lastest stable version into your system.

```bash
docker run -v ~/smh_playerstation:/data -p 8000:8000 --user `id -u`:`getent group audio | awk -F: '{printf "%d", $3}'` --device /dev/snd -d samuelmh/playerstation
```

Then open a web browser, go to http://localhost:8000 and enjoy.

### Building the image
If you don't trust the previous image I created, you can build your own from the source [Dockerfile](https://github.com/samuelmh/raspi-smh_playerstation/blob/master/docker/PC/Dockerfile).

To build the image:
```bash
docker build https://github.com/samuelmh/raspi-smh_playerstation.git#master:docker/PC -t smh_playerstation
```
And you can run it with.
```bash
docker run -v ~/smh_playerstation/songs:/songs -v ~/smh_playerstation/songs_encoded:/songs_encoded -p 8000:8000 --user `id -u`:`getent group audio | awk -F: '{printf "%d", $3}'` --device /dev/snd -d --rm smh_playerstation
```


## Manual Installation <a name="manual"></a>


### Download the project
```bash
git clone https://github.com/samuelmh/raspi-smh_playerstation.git
```


### Raspberry Pi
*Note: tested on* `2017-11-29-raspbian-stretch-lite.img`

#### How to install raspbian OS
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


#### System packages
```bash
sudo apt-get update
sudo apt-get install python3.6 virtualenv git ffmpeg
```

#### Install the project
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
