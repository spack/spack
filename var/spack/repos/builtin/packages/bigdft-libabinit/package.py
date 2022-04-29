# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class BigdftLibabinit(AutotoolsPackage):
    """BigDFT-libABINIT: this is a subsection of files coming from ABINIT software package,
       to which BigDFT has been coupled since the early days. It handles different parts
       like symmetries, ewald corrections, PAW routines, density and potential mixing
       routines and some MD minimizers."""

    homepage = "https://bigdft.org/"
    url      = "https://gitlab.com/l_sim/bigdft-suite/-/archive/1.9.2/bigdft-suite-1.9.2.tar.gz"
    git      = "https://gitlab.com/l_sim/bigdft-suite.git"

    version('develop', branch='devel')
    version('1.9.2',   sha256='dc9e49b68f122a9886fa0ef09970f62e7ba21bb9ab1b86be9b7d7e22ed8fbe0f')
    version('1.9.1',   sha256='3c334da26d2a201b572579fc1a7f8caad1cbf971e848a3e10d83bc4dc8c82e41')
    version('1.9.0',   sha256='4500e505f5a29d213f678a91d00a10fef9dc00860ea4b3edf9280f33ed0d1ac8')
    version('1.8.3',   sha256='f112bb08833da4d11dd0f14f7ab10d740b62bc924806d77c985eb04ae0629909')
    version('1.8.2',   sha256='042e5a3b478b1a4c050c450a9b1be7bcf8e13eacbce4759b7f2d79268b298d61')
    version('1.8.1',   sha256='e09ff0ba381f6ffbe6a3c0cb71db5b73117874beb41f22a982a7e5ba32d018b3')

    variant('mpi', default=True, description='Enable MPI support')

    depends_on('python@:2.8', type=('build', 'run'), when="@:1.8.3")
    depends_on('python@3.0:', type=('build', 'run'), when="@1.9.0:")
    depends_on('python@3.0:', type=('build', 'run'), when="@develop")

    depends_on('mpi',          when='+mpi')
    depends_on('libxc@:2.2.2', when='@:1.9.1')
    depends_on('libxc@:4.3.4', when='@1.9.1:')
    depends_on('libxc@:4.3.4', when='@develop')

    for vers in ['1.8.1', '1.8.2', '1.8.3', '1.9.0', '1.9.1', '1.9.2', 'develop']:
        depends_on('bigdft-futile@{0}'.format(vers), when='@{0}'.format(vers))

    patch('m_libpaw_mpi.F90.patch', when='@:1.8.2')

    build_directory = "libABINIT"

    def autoreconf(self, spec, prefix):
        autoreconf = which('autoreconf')

        with working_dir(self.build_directory):
            if spec.satisfies('@:1.8.2'):
                autoreconf('-i')
            else:
                autoreconf('-fi')

    def configure_args(self):
        spec = self.spec
        prefix = self.prefix

        args = [
            "--with-libxc-libs=%s %s" % (spec['libxc'].libs.ld_flags,
                                         spec['libxc'].libs.ld_flags + "f90"),
            "--with-libxc-incs=%s"    % spec['libxc'].headers.include_flags,
            "--with-futile-libs=%s"   % spec['bigdft-futile'].prefix.lib,
            "--with-futile-incs=%s"   % spec['bigdft-futile'].headers.include_flags,
            "--with-moduledir=%s"     % prefix.include,
            "--prefix=%s" % prefix,
        ]

        if '+mpi' in spec:
            args.append("CC=%s"  % spec['mpi'].mpicc)
            args.append("CXX=%s" % spec['mpi'].mpicxx)
            args.append("FC=%s"  % spec['mpi'].mpifc)
            args.append("F90=%s" % spec['mpi'].mpifc)
            args.append("F77=%s" % spec['mpi'].mpif77)
        else:
            args.append("--disable-mpi")

        return args

    @property
    def libs(self):
        shared = "+shared" in self.spec
        return find_libraries(
            'libabinit', root=self.prefix, shared=shared, recursive=True
        )
