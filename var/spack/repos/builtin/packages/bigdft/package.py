# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Bigdft(Package):
    """BigDFT: electronic structure calculation based on Daubechies wavelets."""

    homepage = "https://bigdft.org/"
    url      = "https://gitlab.com/l_sim/bigdft-suite/-/archive/1.9.1/bigdft-suite-1.9.1.tar.gz"
    git      = "https://gitlab.com/l_sim/bigdft-suite.git"

    version('develop', branch='develop')
    version('1.9.1',   sha256='3c334da26d2a201b572579fc1a7f8caad1cbf971e848a3e10d83bc4dc8c82e41')
    version('1.9.0',   sha256='4500e505f5a29d213f678a91d00a10fef9dc00860ea4b3edf9280f33ed0d1ac8')
    version('1.8.3',   sha256='f112bb08833da4d11dd0f14f7ab10d740b62bc924806d77c985eb04ae0629909')
    version('1.8.2',   sha256='042e5a3b478b1a4c050c450a9b1be7bcf8e13eacbce4759b7f2d79268b298d61')
    version('1.8.1',   sha256='e09ff0ba381f6ffbe6a3c0cb71db5b73117874beb41f22a982a7e5ba32d018b3')

    variant('scalapack', default=True,  description='Enable SCALAPACK support')
    variant('cuda',      default=False, description='Enable CUDA support')

    depends_on('python@:2.8', type='build', when="@:1.9.0")
    depends_on('python@3.1:', type='build', when="@1.9.1:")
    depends_on('py-six',      type='build')
    depends_on('autoconf',    type='build')
    depends_on('automake',    type='build')
    depends_on('libtool',     type='build')
    depends_on('m4',          type='build')

    depends_on('mpi@3:')
    depends_on('blas')
    depends_on('lapack')
    depends_on('scalapack', when='+scalapack')
    depends_on('cuda',      when='+cuda')

    conflicts('%gcc@8.4.0:', when='@:1.8.3',
              msg='Compatibility issues when Bigdft < v1.9.0'
                  ' is compiled with GCC > v8.3.0')

    phases = ['build', 'install']

    def build(self, spec, prefix):
        ext_blas = [spec['blas'].libs.ld_flags]
        ext_linalg = [spec['lapack'].libs.ld_flags]
        fcflags = [
            spec['mpi'].libs.ld_flags,
            spec['mpi'].headers.include_flags,
        ]
        cflags = [
            spec['mpi'].libs.ld_flags,
            spec['mpi'].headers.include_flags,
        ]

        if spec.satisfies('%gcc') or spec.satisfies('%clang'):
            fcflags += ["-ffree-form", "-ffree-line-length-none"]

        if '+scalapack' in spec:
            fcflags.append(spec['scalapack'].libs.ld_flags)
            cflags.append(spec['scalapack'].libs.ld_flags)

        autogen_options = [
            "../Installer.py",
            "autogen",
            "-y",
            "-c",
        ]

        conf_options = [
            "../Installer.py",
            "build",
            "-y",
            "-c",
            "CC=%s" % spec['mpi'].mpicc,
            "CXX=%s" % spec['mpi'].mpicxx,
            "FC=%s" % spec['mpi'].mpifc,
            "F90=%s" % spec['mpi'].mpifc,
            "F77=%s" % spec['mpi'].mpif77,
            "--with-mpi3",
        ]

        if spec.satisfies('@:1.9.0'):
            conf_options += [
                "FCFLAGS=%s" % " ".join(fcflags),
                "CFLAGS=%s" % " ".join(cflags),
                "--with-ext-blas=%s" % " ".join(ext_blas),
                "--with-ext-linalg=%s" % " ".join(ext_linalg),
            ]
        else:
            conf_options += [
                "FCFLAGS=\'%s\'" % " ".join(fcflags),
                "CFLAGS=\'%s\'" % " ".join(cflags),
                "--with-ext-blas=\'%s\'" % " ".join(ext_blas),
                "--with-ext-linalg=\'%s\'" % " ".join(ext_linalg),
            ]

        if '+scalapack' in spec:
            conf_options.append("--with-scalapack")

        if '+cuda' in spec:
            conf_options.append("--enable-opencl")
            conf_options.append("--with-ocl-path=%s" % spec['cuda'].prefix)
            conf_options.append("--enable-cuda-gpu")
            conf_options.append("--with-cuda-path=%s" % spec['cuda'].prefix)

        python = which('python')
        with working_dir('build', create=True):
            if spec.satisfies('@:1.9.0'):
                python(*autogen_options)
            python(*conf_options)

    def install(self, spec, prefix):
        install_tree(join_path('build', 'install'), prefix)
