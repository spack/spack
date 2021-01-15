# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Openexr(AutotoolsPackage):
    """OpenEXR Graphics Tools (high dynamic-range image file format)"""

    homepage = "http://www.openexr.com/"
    url      = "https://github.com/AcademySoftwareFoundation/openexr/archive/v2.5.3.tar.gz"

    version('2.5.3', sha256='6a6525e6e3907715c6a55887716d7e42d09b54d2457323fcee35a0376960bebf')
    version('2.3.0', sha256='fd6cb3a87f8c1a233be17b94c74799e6241d50fc5efd4df75c7a4b9cf4e25ea6')
    version('2.4.2', sha256='8e5bfd89f4ae1221f84216a163003edddf0d37b8aac4ee42b46edb55544599b9')
    version('2.3.0', sha256='9c898bb16e7bc916c82bebdf32c343c0f2878fc3eacbafa49937e78f2079a425')

    variant('debug', default=False,
            description='Builds a debug version of the libraries')

    #Added version constraint to cmake in accordance with:
    #https://github.com/AcademySoftwareFoundation/openexr/blob/master/INSTALL.md
    depends_on('cmake@3.12.0:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('ilmbase')
    depends_on('zlib', type=('build', 'link'))

    def configure_args(self):
        configure_options = []

        configure_options += self.enable_or_disable('debug')

        return configure_options
