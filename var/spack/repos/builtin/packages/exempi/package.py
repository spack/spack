# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Exempi(AutotoolsPackage):
    """exempi is a port of Adobe XMP SDK to work on UNIX and to be build with
    GNU automake.

    It includes XMPCore and XMPFiles, libexempi, a C-based API and exempi
    a command line tool.
    """

    homepage = "https://libopenraw.freedesktop.org/wiki/Exempi"
    url      = "https://libopenraw.freedesktop.org/download/exempi-2.5.2.tar.bz2"

    version('2.5.2', sha256='52f54314aefd45945d47a6ecf4bd21f362e6467fa5d0538b0d45a06bc6eaaed5')

    depends_on('zlib')
    depends_on('iconv')
    depends_on('boost@1.48.0:')
    depends_on('pkgconfig')

    conflicts('%gcc@:4.5')

    def configure_args(self):
        args = ['--with-boost={0}'.format(self.spec['boost'].prefix)]

        if self.spec.satisfies('polatform=darwin'):
            args += ['--with-darwinports', '--with-fink']

        return args
