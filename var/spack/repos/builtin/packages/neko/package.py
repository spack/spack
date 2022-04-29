# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Neko(AutotoolsPackage, CudaPackage, ROCmPackage):
    """Neko: A modern, portable, and scalable framework
       for high-fidelity computational fluid dynamics
    """

    homepage = "https://github.com/ExtremeFLOW/neko"
    git      = "https://github.com/ExtremeFLOW/neko.git"
    maintainers = ['njansson']

    version('0.3.0', commit='a82097a10ae3c965fb873da909a6324c7a7742fb')
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
