#!/bin/bash

set -ex

echo "Installing build tools/packages for Ubuntu 16.06"

apt-get -yqq update
apt-get -yqq install \
  build-essential    \
  ca-certificates    \
  curl               \
  g++-5              \
  gcc-5              \
  gfortran           \
  git                \
  gnupg2             \
  python
