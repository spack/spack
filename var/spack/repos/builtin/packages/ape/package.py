# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ape(AutotoolsPackage):
    """A tool for generating atomic pseudopotentials within a Density-Functional
    Theory framework"""

    homepage = "http://www.tddft.org/programs/APE/"
    url      = "https://gitlab.com/ape/ape/-/archive/2.3.2/ape-2.3.2.tar.gz"

    version('2.3.2', sha256='ac475d0e60ec75003d88a8221d2ad53dc28604f28ac5f64d11499991526c3aab')
    version('2.3.1', sha256='c319a9c2a95e0f4d7a13f8ce4d148af74d13961a40fb19cc9f339a33fad51e4e')
    version('2.3.0', sha256='d9a03eb21eee11d9f8d9889335f50ea05d39398f2527a2811872765700cb84de')
    version('2.2.1', sha256='3f5125182e308ab49338cad791e175ce158526a56c6ca88ac6582c1e5d7435d4')
    version('1.1.1', sha256='9f3ea37299395dae6988093cd1aeb604c81b2d1ca943435e241d4cb451b086bf')
    version('1.0.1', sha256='a88457b22445ececde3d07c5814004b7bbf2d0bc487b6ffca5d87c534636d47b')

    depends_on('m4',       type='build')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('gsl')
    depends_on('libxc@:4.999', when='@2.3.2:')
    depends_on('libxc@:2.2.2', when='@:2.2.1')

    def configure_args(self):
        spec = self.spec
        config_args = [
            '--with-gsl-prefix=%s'   % spec['gsl'].prefix,
            '--with-libxc-prefix=%s' % spec['libxc'].prefix
        ]

        if (spec.satisfies('%apple-clang') or
                spec.satisfies('%clang') or
                spec.satisfies('%gcc')):
            config_args.extend([
                'FCFLAGS=-O2 -ffree-line-length-none'
            ])

        return config_args
