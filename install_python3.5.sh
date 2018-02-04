#!/usr/bin/env bash

# Install Python 3.5 on raspbian (Raspberry Pi)
# FROM: https://gist.github.com/BMeu/af107b1f3d7cf1a2507c9c6429367a3b

echo '-> UPDATING PACKAGE LIST'
apt-get update

echo '-> INSTALLING PACKAGES'
apt-get \
  install build-essential tk-dev \
  install libncurses5-dev libncursesw5-dev libreadline6-dev \
  install libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev \
  install libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev \

# Download pytho1n 3.5
echo '-> DOWNLOADING AND INSTALLING PYTHON 3.5'
wget https://www.python.org/ftp/python/3.5.2/Python-3.5.2.tgz
tar zxvf Python-3.5.2.tgz
cd Python-3.5.2
./configure --prefix=/usr/local/opt/python-3.5.2
make
make install

#	Make the compiled binaries globally available.
echo '-> LINKING BINARIES'
ln -s /usr/local/opt/python-3.5.2/bin/pydoc3.5 /usr/bin/pydoc3.5
ln -s /usr/local/opt/python-3.5.2/bin/python3.5 /usr/bin/python3.5
ln -s /usr/local/opt/python-3.5.2/bin/python3.5m /usr/bin/python3.5m
ln -s /usr/local/opt/python-3.5.2/bin/pyvenv-3.5 /usr/bin/pyvenv-3.5
ln -s /usr/local/opt/python-3.5.2/bin/pip3.5 /usr/bin/pip3.5

# Clean
echo '-> CLEANING'
rm -r Python-3.5.2
rm Python-3.5.2.tgz
apt-get autoremove
apt-get clean
