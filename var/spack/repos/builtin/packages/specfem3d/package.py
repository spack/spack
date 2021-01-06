# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Specfem3d(AutotoolsPackage):
    """Program specfem3D from SPECFEM3D_GLOBE is
    a 3-D spectral-element solver for the Earth.
    It uses a mesh generated by program meshfem3D."""

    homepage = "https://github.com/geodynamics/specfem3d_globe"
    url      = "https://github.com/geodynamics/specfem3d_globe/archive/v7.0.2.tar.gz"

    version('7.0.2', sha256='78b4cfbe4e5121927ab82a8c2e821b65cdfff3e94d017303bf21af7805186d9b')

    variant("cuda", default=False,
            description="Build with CUDA code generator")
    variant('opencl', default=False,
            description="Build with OpenCL code generator")
    variant('openmp', default=True,
            description="Build with OpenMP code generator")
    variant('double-precision', default=False,
            description="Treat REAL as double precision")

    depends_on('mpi')
    depends_on('cuda', when='+cuda')
    depends_on('opencl', when='+opencl')

    def configure_args(self):
        args = []

        if '+cuda'   in self.spec:
            args.append('--with-cuda')
            args.append('CUDA_LIB={0}'
                        .format(spec['cuda'].libs.directories[0]))
            args.append('CUDA_INC={0}'
                        .format(spec['cuda'].prefix.include))
            args.append('MPI_INC={0}'
                        .format(spec['mpi'].prefix.include))
        if '+opencl' in self.spec:
            args.append('--with-opencl')
            args.append('OCL_LIB={0}'
                        .format(spec['opencl'].libs.directories[0]))
            args.append('OCL_INC={0}'
                        .format(spec['opencl'].prefix.include))

        args.extend(self.enable_or_disable('openmp'))
        args.extend(self.enable_or_disable('double-precision'))

        return args

    def install(self, spec, prefix):
        install_tree('.', prefix)
