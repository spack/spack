# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libpsl(AutotoolsPackage):
    """libpsl - C library to handle the Public Suffix List."""

    homepage = "https://github.com/rockdaboot/libpsl"
    url      = "https://github.com/rockdaboot/libpsl/releases/download/libpsl-0.17.0/libpsl-0.17.0.tar.gz"

    version('0.17.0', 'fed13f33d0d6dc13ef24de255630bfcb')

    depends_on('icu4c')

    depends_on('gettext', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('python@2.7:', type='build')

    depends_on('valgrind~mpi~boost', type='test')

    def configure_args(self):
        spec = self.spec

        args = [
            'PYTHON={0}'.format(spec['python'].command.path),
        ]

        if self.run_tests:
            args.append('--enable-valgrind-tests')
        else:
            args.append('--disable-valgrind-tests')

        return args
