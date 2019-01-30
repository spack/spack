# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ndiff(Package):
    """The ndiff tool is a binary utility that compares putatively similar
       files while ignoring small numeric differernces. This utility is
       most often used to compare files containing a lot of
       floating-point numeric data that may be slightly different due to
       numeric error.

    """

    homepage = "http://ftp.math.utah.edu/pub/ndiff/"
    url      = "http://ftp.math.utah.edu/pub/ndiff/ndiff-2.00.tar.gz"

    version('2.00', '885548b4dc26e72c5455bebb5ba6c16d')
    version('1.00', 'f41ffe5d12f36cd36b6311acf46eccdc')

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix)

        mkdirp(prefix.bin)
        mkdirp('%s/lib' % prefix.share)

        make('install-exe', 'install-shrlib')
