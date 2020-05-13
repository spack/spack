# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Apbs(AutotoolsPackage):
    """APBS solves the equations of continuum electrostatics
    for large biomolecular assemblages."""

    homepage = "http://www.poissonboltzmann.org/"
    url      = "https://downloads.sourceforge.net/project/apbs/apbs/apbs-1.3.0/apbs-1.3-source.tar.gz"

    # Working around race condition
    parallel = False

    # Version 1.4.2.1 uses cmake. Commented out pending resolution of
    # https://github.com/spack/spack/pull/12941
    # version('1.4.2.1', sha256='aa3de78394ccfdbc29115f07fb005480603a4884628b8f82c9e38d93889dc2be',
    #         url="https://downloads.sourceforge.net/project/apbs/apbs/apbs-1.4.2/apbs-1.4.2.1-source.tar.gz" )
    version('1.3', sha256='5fa5b597f7d5a3d9bb55429ec4fefc69e7d0f918d568c3c4a288088c0fde9ef2')

    variant('python', default=False, description='Build with python wrappers')

    depends_on('python@:2.9999', when='+python')
    depends_on('maloc@:1.4')

    def configure_args(self):
        spec = self.spec
        args = []

        args.append('--disable-maloc-rebuild')

        if '+python' in spec:
            args.append('--enable-python')
        else:
            args.append('--disable-python')

        return args
