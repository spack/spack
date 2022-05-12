# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Atompaw(AutotoolsPackage):
    """atompaw generates projector augmented wave (PAW)
    potentials for electronics structure calculations."""

    homepage = "https://users.wfu.edu/natalie/papers/pwpaw/"
    url      = "https://users.wfu.edu/natalie/papers/pwpaw/atompaw-4.2.0.0.tar.gz"

    version('4.2.0.0', sha256='9ab4f4ab78a720fbcd95bbbc1403e8ff348d15570e7c694932a56be15985e93d')
    version('4.1.1.0', sha256='b1ee2b53720066655d98523ef337e54850cb1e68b3a2da04ff5a1576d3893891')
    version('4.1.0.6', sha256='42a46c0569367c0b971fbc3dcaf5eaec7020bdff111022b6f320de9f11c41c2c')

    variant('libxc', default=False, description='Compile with libxc')
    variant('shared', default=True)

    depends_on('libxc', when='+libxc')
    depends_on('blas')

    def configure_args(self):
        spec = self.spec

        args = ['--with-linalg-prefix=' + spec['blas'].prefix]
        args += ['--with-linalg-libs=' + ' '.join(spec['blas'].libs)]

        if '+libxc' in spec:
            args += ['--enable-libxc']
            args += ['--with-libxc-prefix=' + spec['libxc'].prefix]

        if '+shared' in spec:
            args += ['--enable-shared']
        else:
            args += ['--enable-static']

        return args
