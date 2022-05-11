# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class BigdftSpred(AutotoolsPackage):
    """BigDFT-spred: a library for structure prediction tools,
       that is compiled on top of BigDFT routines."""

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

    variant('mpi',       default=True, description='Enable MPI support')
    variant('openmp',    default=True, description='Enable OpenMP support')
    variant('scalapack', default=True, description='Enable SCALAPACK support')

    depends_on('python@:2.8', type=('build', 'run'), when="@:1.8.3")
    depends_on('python@3.0:', type=('build', 'run'), when="@1.9.0:")
    depends_on('python@3.0:', type=('build', 'run'), when="@develop")

    depends_on('blas')
    depends_on('lapack')
    depends_on('py-pyyaml')
    depends_on('mpi',       when='+mpi')
    depends_on('scalapack', when='+scalapack')

    for vers in ['1.8.1', '1.8.2', '1.8.3', '1.9.0', '1.9.1', '1.9.2', 'develop']:
        depends_on('bigdft-futile@{0}'.format(vers),  when='@{0}'.format(vers))
        depends_on('bigdft-psolver@{0}'.format(vers), when='@{0}'.format(vers))
        depends_on('bigdft-core@{0}'.format(vers),    when='@{0}'.format(vers))

    build_directory = "spred"

    def autoreconf(self, spec, prefix):
        autoreconf = which('autoreconf')

        with working_dir(self.build_directory):
            autoreconf('-fi')

    def configure_args(self):
        spec = self.spec
        prefix = self.prefix

        python_version = spec['python'].version.up_to(2)
        pyyaml = join_path(spec['py-pyyaml'].prefix.lib,
                           'python{0}'.format(python_version))

        openmp_flag = []
        if '+openmp' in spec:
            openmp_flag.append(self.compiler.openmp_flag)

        linalg = []
        if '+scalapack' in spec:
            linalg.append(spec['scalapack'].libs.ld_flags)
        linalg.append(spec['lapack'].libs.ld_flags)
        linalg.append(spec['blas'].libs.ld_flags)

        args = [
            "FCFLAGS=%s"             % " ".join(openmp_flag),
            "--with-ext-linalg=%s"   % " ".join(linalg),
            "--with-pyyaml-path=%s"  % pyyaml,
            "--with-futile-libs=%s"  % spec['bigdft-futile'].prefix.lib,
            "--with-futile-incs=%s"  % spec['bigdft-futile'].headers.include_flags,
            "--with-psolver-libs=%s" % spec['bigdft-psolver'].prefix.lib,
            "--with-psolver-incs=%s" % spec['bigdft-psolver'].headers.include_flags,
            "--with-core-libs=%s"    % spec['bigdft-core'].prefix.lib,
            "--with-core-incs=%s"    % spec['bigdft-core'].headers.include_flags,
            "--with-moduledir=%s"    % prefix.include,
            "--prefix=%s"            % prefix,
        ]

        if '+mpi' in spec:
            args.append("CC=%s"  % spec['mpi'].mpicc)
            args.append("CXX=%s" % spec['mpi'].mpicxx)
            args.append("FC=%s"  % spec['mpi'].mpifc)
            args.append("F90=%s" % spec['mpi'].mpifc)
            args.append("F77=%s" % spec['mpi'].mpif77)
        else:
            args.append("--disable-mpi")

        if '+openmp' in spec:
            args.append("--with-openmp")
        else:
            args.append("--without-openmp")

        return args

    @property
    def libs(self):
        shared = "+shared" in self.spec
        return find_libraries(
            'libspred-*', root=self.prefix, shared=shared, recursive=True
        )
