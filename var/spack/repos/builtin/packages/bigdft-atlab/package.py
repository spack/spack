# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class BigdftAtlab(AutotoolsPackage):
    """BigDFT: electronic structure calculation based on Daubechies wavelets."""

    homepage = "https://bigdft.org/"
    url      = "https://gitlab.com/l_sim/bigdft-suite/-/archive/1.9.1/bigdft-suite-1.9.1.tar.gz"
    git      = "https://gitlab.com/l_sim/bigdft-suite.git"

    version('1.9.1',   sha256='3c334da26d2a201b572579fc1a7f8caad1cbf971e848a3e10d83bc4dc8c82e41')
    version('1.9.0',   sha256='4500e505f5a29d213f678a91d00a10fef9dc00860ea4b3edf9280f33ed0d1ac8')
    version('1.8.3',   sha256='f112bb08833da4d11dd0f14f7ab10d740b62bc924806d77c985eb04ae0629909')

    variant('openbabel', default=False, description='Enable detection of openbabel compilation')
    variant('openmp',    default=True,  description='Enable OpenMP support')

    depends_on('python@:2.8', type='build', when="@:1.9.0")
    depends_on('python@3.0:', type='build', when="@1.9.1:")

    depends_on('mpi')
    depends_on('bigdft-futile@1.9.1', when='@1.9.1')
    depends_on('bigdft-futile@1.9.0', when='@1.9.0')
    depends_on('bigdft-futile@1.8.3', when='@1.8.3')
    depends_on('bigdft-futile@1.8.2', when='@1.8.2')
    depends_on('bigdft-futile@1.8.1', when='@1.8.1')
    depends_on('openbabel', when='+openbabel')

    phases = ['autoreconf', 'configure', 'build', 'install']

    def autoreconf(self, spec, prefix):
        autoreconf = which('autoreconf')

        with working_dir('atlab'):
            autoreconf('-fi')

    def configure(self, spec, prefix):
        fcflags = [spec['mpi'].libs.ld_flags]
        cflags = [spec['mpi'].libs.ld_flags]

        python_version = spec['python'].version.up_to(2)
        pyyaml = join_path(spec['py-pyyaml'].prefix.lib, 
                                'python{0}'.format(python_version))

        args = [
            "CC=%s" % spec['mpi'].mpicc,
            "CXX=%s" % spec['mpi'].mpicxx,
            "FC=%s" % spec['mpi'].mpifc,
            "F90=%s" % spec['mpi'].mpifc,
            "F77=%s" % spec['mpi'].mpif77,
            "FCFLAGS=%s" % " ".join(fcflags),
            "CFLAGS=%s" % " ".join(cflags),
            "--with-futile-libs=%s" % spec['bigdft-futile'].prefix.lib,
            "--with-futile-incs=%s" % spec['bigdft-futile'].prefix.include,
            "--without-etsf-io",
            "--with-moduledir=%s" % prefix.include,
            "--prefix=%s" % prefix,
        ]

        if '+openbabel' in spec:
            args.append("--enable-openbabel")
            args.append("--with-openbabel-libs=%s" % spec['openbabel'].prefix.lib)
            args.append("--with-openbabel-incs=%s" % spec['openbabel'].prefix.include)

        if '+openmp' in spec:
            args.append("--with-openmp")
        else:
            args.append("--without-openmp")

        with working_dir('atlab'):
            configure(*args)

    def build(self, spec, prefix):
        with working_dir('atlab'):
            make()

    def install(self, spec, prefix):
        with working_dir('atlab'):
            make('install')

    @property
    def libs(self):
        shared = "+shared" in self.spec
        return find_libraries(
            'libatlab-*', root=self.prefix, shared=shared, recursive=True
        )
