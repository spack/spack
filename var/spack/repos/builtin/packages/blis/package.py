##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *

# Although this looks like an Autotools package, it's not one. Refer to:
# https://github.com/flame/blis/issues/17
# https://github.com/flame/blis/issues/195
# https://github.com/flame/blis/issues/197


class Blis(Package):
    """BLIS is a portable software framework for instantiating high-performance
    BLAS-like dense linear algebra libraries. The framework was designed to
    isolate essential kernels of computation that, when optimized, immediately
    enable optimized implementations of most of its commonly used and
    computationally intensive operations. BLIS is written in ISO C99 and
    available under a new/modified/3-clause BSD license. While BLIS exports a
    new BLAS-like API, it also includes a BLAS compatibility layer which gives
    application developers access to BLIS implementations via traditional BLAS
    routine calls. An object-based API unique to BLIS is also available."""

    homepage = "https://github.com/flame/blis"
    url      = "https://github.com/flame/blis/archive/0.4.0.tar.gz"
    git      = "https://github.com/flame/blis.git"

    version('develop', branch='master')
    version('0.4.0', sha256='9c7efd75365a833614c01b5adfba93210f869d92e7649e0b5d9edc93fc20ea76')
    version('0.3.2', sha256='b87e42c73a06107d647a890cbf12855925777dc7124b0c7698b90c5effa7f58f')
    version('0.3.1', sha256='957f28d47c5cf71ffc62ce8cc1277e17e44d305b1c2fa8506b0b55617a9f28e4')
    version('0.3.0', sha256='d34d17df7bdc2be8771fe0b7f867109fd10437ac91e2a29000a4a23164c7f0da')
    version('0.2.2', sha256='4a7ecb56034fb20e9d1d8b16e2ef587abbc3d30cb728e70629ca7e795a7998e8')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))

    variant(
        'threads', default='none',
        description='Multithreading support',
        values=('pthreads', 'openmp', 'none'),
        multi=False
    )

    variant(
        'blas', default=True,
        description='BLAS compatibility',
    )

    variant(
        'cblas', default=False,
        description='CBLAS compatibility',
    )

    variant(
        'shared', default=True,
        description='Build shared library',
    )

    variant(
        'static', default=True,
        description='Build static library',
    )

    # TODO: add cpu variants. Currently using auto.
    # If one knl, should the default be memkind ?

    # BLIS has it's own API but can be made compatible with BLAS
    # enabling CBLAS automatically enables BLAS.

    provides('blas', when="+blas")
    provides('blas', when="+cblas")

    phases = ['configure', 'build', 'install']

    def configure(self, spec, prefix):
        config_args = []

        config_args.append("--enable-threading=" +
                           spec.variants['threads'].value)

        if '+cblas' in spec:
            config_args.append("--enable-cblas")
        else:
            config_args.append("--disable-cblas")

        if '+blas' in spec:
            config_args.append("--enable-blas")
        else:
            config_args.append("--disable-blas")

        if '+shared' in spec:
            config_args.append("--enable-shared")
        else:
            config_args.append("--disable-shared")

        if '+static' in spec:
            config_args.append("--enable-static")
        else:
            config_args.append("--disable-static")

        # FIXME: add cpu isa variants.
        config_args.append("auto")

        configure("--prefix=" + prefix,
                  *config_args)

    def build(self, spec, prefix):
        make()

    @run_after('build')
    @on_package_attributes(run_tests=True)
    def check(self):
        make('check')

    def install(self, spec, prefix):
        make('install')
