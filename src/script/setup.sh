# This script install olympe dependencies
#
# Usage:
# bash postinst
set -e
# Check if we need to sudo things
if [ "$(id -u)" != "0" ]
then
  SUDO="sudo"
  echo "This script might prompt you for your sudo password."
else
  SUDO=""
fi
# install system packages with apt
${SUDO} apt-get update || true # who doesn't have invalid/broken apt sources
# install pyenv dependencies
${SUDO} apt-get install -y make build-essential libssl-dev zlib1g-dev \
        libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev \
        libncursesw5-dev libncurses5 xz-utils tk-dev libffi-dev liblzma-dev \
        python-openssl git libgdbm-dev libgdbm-compat-dev uuid-dev python3-gdbm \
        gawk
# Install python
${SUDO} apt-get -y install python3
# pdraw dependencies
${SUDO} apt-get -y install build-essential yasm cmake libtool libc6 libc6-dev \
  unzip freeglut3-dev libglfw3 libglfw3-dev libsdl2-dev libjson-c-dev \
  libcurl4-gnutls-dev libavahi-client-dev libgles2-mesa-dev
# ffmpeg build dependencies
${SUDO} apt-get -y install rsync
# arsdk build dependencies
${SUDO} apt-get -y install cmake libbluetooth-dev libavahi-client-dev \
    libopencv-dev libswscale-dev libavformat-dev \
    libavcodec-dev libavutil-dev cython python-dev
# Olympe / PySDL2 / pdraw renderer dependencies
${SUDO} apt-get -y install libsdl2-dev libsdl2-2.0-0 libjpeg-dev libwebp-dev \
 libtiff5-dev libsdl2-image-dev libsdl2-image-2.0-0 libfreetype6-dev \
 libsdl2-ttf-dev libsdl2-ttf-2.0-0 libsdl2-gfx-dev