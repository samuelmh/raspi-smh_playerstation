FROM alpine:3.7

# Install packages
RUN apk add --no-cache \
  python3=3.6.3-r9 \
	py3-virtualenv \
  make && \
# /data dir will be a volume
  ln -s /home/nouser/raspi-smh_playerstation/data /data && \
# Create a non-root user
  adduser nouser -D && \
  su nouser && \
# Download production project
  cd && \
  wget https://github.com/samuelmh/raspi-smh_playerstation/archive/dev.zip && \
  unzip dev.zip && \
  rm dev.zip && \
  mv raspi-smh_playerstation-dev raspi-smh_playerstation && \
# Install project
  cd "raspi-smh_playerstation" && \
  make install

USER nouser
WORKDIR /home/nouser/raspi-smh_playerstation
VOLUME ["/data"]
ENTRYPOINT ["make", "run-webserver"]
EXPOSE 8000
