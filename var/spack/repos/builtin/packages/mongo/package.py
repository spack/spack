# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install mongo
#
# You can edit this file again by typing:
#
#     spack edit mongo
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Mongo(SConsPackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://github.com/mongodb/mongo"
    url      = "https://github.com/mongodb/mongo/archive/r4.0.6.tar.gz"

    version('4.0.6',      sha256='5db85f06b2a0b2ae393339a4aed1366928aaef2b46c7c32826fa87c3217dc6f7')
    version('3.6.12',     sha256='5d6e99edbea4395c5de18fead0db882cac87ee3c8eb4ad446d91c33ab91cd175')

    variant('languages',
        default='c,c++,fortran',
        values=('ada', 'brig', 'c', 'c++', 'fortran',
                'go', 'java', 'jit', 'lto', 'objc', 'obj-c++'),
        multi=True,
        description='Compilers and runtime libraries to build')

    # FIXME: Add dependencies if required.

    depends_on('gmp@6.1.0', when='@4.0.6')
    depends_on('isl@0.16.1', when='@4.0.6')
    depends_on('mpc@1.0.3', when='@4.0.6')
    depends_on('mpfr@3.1.4', when='@4.0.6')
    depends_on('gcc@7.3.0', when='@4.0.6')

    depends_on('py-pyyaml', when='@4.0.6:', type=('build', 'run'))
    depends_on('py-typing', when='@4.0.6:', type=('build', 'run'))
    depends_on('py-cheetah', when='@4.0.6:', type=('build','run'))

    depends_on('python@2.7.16', when='@4.0.6')

    def build_args(self, spec, prefix):
        # FIXME: Add arguments to pass to build.
        # FIXME: If not needed delete this functiona
        args = [
               'MONGO_VERSION=4.0.6',
               '--disable-warnings-as-errors',
               'CFLAGS="-march=armv8-a+crc -mtune=generic"',
               'CFLAGS="-march=armv8-a+crc"'
               ]
        return args

    def install_args(self, spec, prefix):
        args = [
                '--prefix={0}'.format(prefix),
                'MONGO_VERSION=4.0.6',
                '--disable-warnings-as-errors',
                'CCFLAGS="-march=armv8-a+crc"'
               ]
        return args
