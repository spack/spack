# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Form(AutotoolsPackage):
    """FORM is a Symbolic Manipulation System."""

    homepage = "https://www.nikhef.nl/~form/"
    url      = "https://github.com/vermaseren/form/releases/download/v4.2.1/form-4.2.1.tar.gz"
    maintainers = ['iarspider', 'tueda']

    version('4.2.1', sha256='f2722d6d4ccb034e01cf786d55342e1c21ff55b182a4825adf05d50702ab1a28')
    version('4.1-20131025', sha256='fb3470937d66ed5cb1af896b15058836d2c805d767adac1b9073ed2df731cbe9',
            url='https://github.com/vermaseren/form/releases/download/v4.1-20131025/form-4.1.tar.gz')

    depends_on('gmp',      type='link', when='+gmp')
    depends_on('zlib',     type='link', when='+zlib')
    depends_on('mpi',      type='link', when='+parform')

    variant('gmp', default=True, description='Use GMP for long integer arithmetic')
    variant('zlib', default=True, description='Use zlib for compression')
    variant('scalar', default=True, description='Build scalar version (form)')
    variant('threaded', default=True, description='Build threaded version (tform)')
    variant('parform', default=False, description='Build parallel version using MPI (parform)')

    def configure_args(self):
        args = []
        args += self.with_or_without('gmp', 'prefix')
        args += self.with_or_without('zlib', 'prefix')
        args += self.enable_or_disable('scalar')
        args += self.enable_or_disable('threaded')
        args += self.enable_or_disable('parform')

        return args
