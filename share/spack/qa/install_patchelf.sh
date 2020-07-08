#!/bin/sh
#
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
# Description:
#     Install patchelf for use in buildcache unit tests
#
# Usage:
#     install-patchelf.sh
#
set -ex
if [ "$TRAVIS_OS_NAME" = "linux" ]; then
    olddir=$PWD
    cd /tmp
    wget https://github.com/NixOS/patchelf/archive/0.10.tar.gz
    tar -xvf 0.10.tar.gz
    cd patchelf-0.10 && ./bootstrap.sh && ./configure --prefix=/usr && make && sudo make install && cd $olddir
fi
