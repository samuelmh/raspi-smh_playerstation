FROM alpine:3.7

RUN \
  # Install packages
  apk add --no-cache \
    python3=3.6.3-r9 \
    py3-virtualenv=15.1.0-r0 \
    make=4.2.1-r0 \
    alsa-lib=1.1.4.1-r2 \
    ffmpeg=3.4-r1 && \
  # Project directory
  mkdir /opt  && \
  cd /opt  && \
  # Download
  wget https://github.com/samuelmh/raspi-smh_playerstation/archive/dev.zip && \
  unzip dev.zip && \
  rm dev.zip && \
  mv raspi-smh_playerstation-dev raspi-smh_playerstation && \
  # Install project
  cd "raspi-smh_playerstation" && \
  make install

RUN \
  # Output project directories
  cd "/opt/raspi-smh_playerstation" && \
  mkdir data/songs && \
  mkdir data/encoded && \
  # easy-name volumes
  ln -s /opt/raspi-smh_playerstation/data/songs /songs && \
  ln -s /opt/raspi-smh_playerstation/data/encoded /songs_encoded && \
  # Permissions
  chmod -R 755 /opt && \
  chmod -R 777 /opt/raspi-smh_playerstation/data


WORKDIR /opt/raspi-smh_playerstation
VOLUME ["/songs"]
VOLUME ["/songs_encoded"]
CMD make run-webserver
EXPOSE 8000

# SAMPLE RUN:
# docker run -v ~/smh_playerstation/songs:/songs -v ~/smh_playerstation/songs_encoded:/songs_encoded -p 8000:8000 --user `id -u`:`getent group audio | awk -F: '{printf "%d", $3}'` --device /dev/snd -d smh_playerstation
