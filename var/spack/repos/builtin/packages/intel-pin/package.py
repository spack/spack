# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from os import symlink


class IntelPin(Package):
    """Intel Pin is a dynamic binary instrumentation framework for the IA-32,
    x86-64 and MIC instruction-set architectures that enables the creation of
    dynamic program analysis tools."""

    homepage = "http://www.pintool.org"
    maintainers = ['matthiasdiener']

    version('3.11', sha256='aa5abca475a6e106a75e6ed4ba518fb75a57549a59f00681e6bd6e3f221bd23a', url='https://software.intel.com/sites/landingpage/pintool/downloads/pin-3.11-97998-g7ecce2dac-gcc-linux.tar.gz')
    version('3.10', sha256='7c8f14c3a0654bab662b58aba460403138fa44517bd40052501e8e0075b2702a', url='https://software.intel.com/sites/landingpage/pintool/downloads/pin-3.10-97971-gc5e41af74-gcc-linux.tar.gz')
    version('3.7',  sha256='4730328795be61f1addb0e505a3792a4b4ca80b1b9405acf217beec6b5b90fb8', url='https://software.intel.com/sites/landingpage/pintool/downloads/pin-3.7-97619-g0d0c92f4f-gcc-linux.tar.gz')

    def install(self, spec, prefix):
        install_tree('.', prefix)
        mkdir(prefix.bin)
        symlink(join_path(prefix, 'pin'), join_path(prefix.bin, 'pin'))
