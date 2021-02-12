# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Rlwrap(AutotoolsPackage):
    """rlwrap is a 'readline wrapper', a small utility that uses the GNU
    readline library to allow the editing of keyboard input for any command."""

    homepage = "https://github.com/hanslub42/rlwrap"
    url      = "https://github.com/hanslub42/rlwrap/releases/download/v0.43/rlwrap-0.43.tar.gz"

    version('0.44', sha256='cd7ff50cde66e443cbea0049b4abf1cca64a74948371fa4f1b5d9a5bbce1e13c')
    version('0.43', sha256='8e86d0b7882d9b8a73d229897a90edc207b1ae7fa0899dca8ee01c31a93feb2f')

    depends_on('readline@4.2:')
