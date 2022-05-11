# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class Neko(AutotoolsPackage, CudaPackage, ROCmPackage):
    """Neko: A modern, portable, and scalable framework
       for high-fidelity computational fluid dynamics
    """

    homepage = "https://github.com/ExtremeFLOW/neko"
    git      = "https://github.com/ExtremeFLOW/neko.git"
    url = "https://github.com/ExtremeFLOW/neko/releases/download/v0.3.2/neko-0.3.2.tar.gz"
    maintainers = ['njansson']

    version('0.3.2', sha256='0628910aa9838a414f2f27d09ea9474d1b3d7dcb5a7715556049a2fdf81a71ae')
    version('0.3.0', sha256='e46bef72f694e59945514ab8b1ad7d74f87ec9dca2ba2b230e2148662baefdc8')
    version('develop', branch='develop')
    variant('parmetis', default=False, description='Build with support for parmetis')
    variant('xsmm', default=False, description='Build with support for libxsmm')

    depends_on('autoconf',  type='build')
    depends_on('automake',  type='build')
    depends_on('libtool',   type='build')
    depends_on('m4',        type='build')
    depends_on('pkgconfig', type='build')
    depends_on('parmetis', when='+parmetis')
    depends_on('libxsmm',  when='+xsmm')
    depends_on('mpi')
    depends_on('blas')
    depends_on('lapack')

    def configure_args(self):
        args = []
        args += self.with_or_without('parmetis')
        args += self.with_or_without('libxsmm', variant='xsmm')
        args += self.with_or_without('cuda', activation_value='prefix')
        rocm_fn = lambda x: spec['hip'].prefix
        args += self.with_or_without('hip', variant='rocm', activation_value=rocm_fn)

        return args
