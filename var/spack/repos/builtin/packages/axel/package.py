# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Axel(AutotoolsPackage):
    """Axel is a light command line download accelerator for Linux and Unix"""

    homepage = "https://github.com/axel-download-accelerator/axel"
    url      = 'https://github.com/axel-download-accelerator/axel/releases/download/v2.17.10/axel-2.17.10.tar.bz2'

    version('2.17.10', sha256='c0d26eba6b94945cd98c5b69ca6df2744639d17bfd49047ef51a8a48f067de10')
    version('2.16.1',  sha256='763066efc61e4f7be2eb59afa049bdbc520837e01c95a78f403e542ad82f2719')

    depends_on('pkgconfig', type='build')
    # For systems not providing libintl APU in the system libc (glibc integrated it)
    depends_on('gettext')
    depends_on('openssl')

    def installcheck(self):
        Executable(self.prefix.bin.axel)('--version')
