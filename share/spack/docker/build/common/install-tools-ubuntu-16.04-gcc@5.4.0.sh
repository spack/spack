#!/bin/bash

set -ex

echo "Installing build tools/packages for Ubuntu 16.04"

apt-get -yqq update
apt-get -yqq install \
  build-essential    \
  ca-certificates    \
  curl               \
  file               \
  g++-5              \
  gcc-5              \
  gfortran           \
  git                \
  gnupg2             \
  python
