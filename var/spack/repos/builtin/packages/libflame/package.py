# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libflame(AutotoolsPackage):
    """libflame is a portable library for dense matrix computations,
    providing much of the functionality present in LAPACK, developed
    by current and former members of the Science of High-Performance
    Computing (SHPC) group in the Institute for Computational
    Engineering and Sciences at The University of Texas at Austin.
    libflame includes a compatibility layer, lapack2flame, which
    includes a complete LAPACK implementation."""

    homepage = "https://www.cs.utexas.edu/~flame/web/libFLAME.html"
    url      = "https://github.com/flame/libflame/archive/5.1.0.tar.gz"
    git      = "https://github.com/flame/libflame.git"

    version('master', branch='master')
    version('5.2.0', sha256='997c860f351a5c7aaed8deec00f502167599288fd0559c92d5bfd77d0b4d475c')
    version('5.1.0', sha256='e7189b750890bd781fe773f366b374518dd1d89a6513d3d6261bf549826384d1')

    provides('lapack', when='+lapack2flame')

    variant('lapack2flame', default=True,
            description='Map legacy LAPACK routine invocations'
            ' to their corresponding native C implementations'
            ' in libflame.')

    variant('threads', default='no',
            description='Multithreading support',
            values=('pthreads', 'openmp', 'no'),
            multi=False)

    variant('static', default=True,
            description='Build static library')

    variant('shared', default=True,
            description='Build shared library')

    variant('debug', default=False,
            description='Build with debugging support')

    # TODO: Libflame prefers to defer to an external
    # LAPACK library for small problems. Is this to be
    # implemented in spack ?

    # There is a known issue with the makefile :
    # https://groups.google.com/forum/#!topic/libflame-discuss/lQKEfjyudOY
    patch('Makefile_5.1.0.patch', when='@5.1.0')

    def flag_handler(self, name, flags):
        # -std=gnu99 at least required, old versions of GCC default to -std=c90
        if self.spec.satisfies('%gcc@:5.1') and name == 'cflags':
            flags.append('-std=gnu99')
        return (flags, None, None)

    def configure_args(self):
        config_args = []

        if '+lapack2flame' in self.spec:
            config_args.append("--enable-lapack2flame")
        else:
            config_args.append("--disable-lapack2flame")

        if '+static' in self.spec:
            config_args.append("--enable-static-build")
        else:
            config_args.append("--disable-static-build")

        if '+shared' in self.spec:
            config_args.append("--enable-dynamic-build")
        else:
            config_args.append("--disable-dynamic-build")

        if '+debug' in self.spec:
            config_args.append("--enable-debug")
        else:
            config_args.append("--disable-debug")

        config_args.append('--enable-multithreading='
                           + self.spec.variants['threads'].value)

        if 'no' != self.spec.variants['threads'].value:
            config_args.append("--enable-supermatrix")
        else:
            config_args.append("--disable-supermatrix")

        # https://github.com/flame/libflame/issues/21
        config_args.append("--enable-max-arg-list-hack")

        return config_args
