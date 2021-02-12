# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Zziplib(AutotoolsPackage):
    """The zziplib provides read access to zipped files in a zip-archive, using
    compression based solely on free algorithms provided by zlib.  It also
    provides a functionality to overlay the archive filesystem with the
    filesystem of the operating system environment."""

    homepage = "https://github.com/gdraheim/zziplib"
    url      = "https://github.com/gdraheim/zziplib/archive/v0.13.69.tar.gz"

    version('0.13.72', sha256='93ef44bf1f1ea24fc66080426a469df82fa631d13ca3b2e4abaeab89538518dc')
    version('0.13.71', sha256='2ee1e0fbbb78ec7cc46bde5b62857bc51f8d665dd265577cf93584344b8b9de2')
    version('0.13.70', sha256='a1457262d7a237dc50ce1f98ca57242bc714055ff81146f419ee53cdea1bf029')
    version('0.13.69', sha256='846246d7cdeee405d8d21e2922c6e97f55f24ecbe3b6dcf5778073a88f120544')

    patch('python2to3.patch')

    build_directory = 'spack-build'

    depends_on('python', type='build')
    depends_on('zlib')

    def configure_args(self):
        args = ['--with-zlib={0}'.format(self.spec['zlib'].prefix)]
        return args
