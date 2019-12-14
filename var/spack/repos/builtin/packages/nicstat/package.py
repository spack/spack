# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Nicstat(Package):
    """
    Nicstat is a Solaris and Linux command-line that prints out network
    statistics for all network interface cards (NICs), including packets,
    kilobytes per second, average packet sizes and more.
    """

    homepage = "https://github.com/scotte/nicstat"
    url      = "https://jaist.dl.sourceforge.net/project/nicstat/nicstat-1.95.tar.gz"

    version('1.95', sha256='c4cc33f8838f4523f27c3d7584eedbe59f4c587f0821612f5ac2201adc18b367')

    def install(self, spec, prefix):
        os.popen("mv Makefile.Linux makefile && sed -i '23cCMODEL=""' makefile\
        && sed -i 's/sudo/''/g' makefile && mkdir /usr/local/share/man/man1 ")
        make()
        make('install')
        install_tree(".", prefix)
