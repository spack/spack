# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *


class Bigdft(Package):
    """BigDFT: electronic structure calculation based on Daubechies wavelets."""

    homepage = "https://bigdft.org/"
    url      = "https://gitlab.com/l_sim/bigdft-suite/-/archive/1.9.1/bigdft-suite-1.9.1.tar.gz"
    git      = "https://gitlab.com/l_sim/bigdft-suite.git"

    version('1.9.1', sha256='3c334da26d2a201b572579fc1a7f8caad1cbf971e848a3e10d83bc4dc8c82e41')
    version('1.9.0', sha256='4500e505f5a29d213f678a91d00a10fef9dc00860ea4b3edf9280f33ed0d1ac8')
    version('1.8.3', sha256='f112bb08833da4d11dd0f14f7ab10d740b62bc924806d77c985eb04ae0629909')

    variant('cuda',      default=False, description='Enable CUDA support')
    variant('scalapack', default=True,  description='Enable SCALAPACK support')
    variant('openmp',    default=True,  description='Enable OpenMP support')

    depends_on('python',   type='build')
    depends_on('py-six',   type='build')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')

    depends_on('mpi')
    depends_on('lapack')
    depends_on('scalapack', when='+scalapack')
    depends_on('cuda',      when='+cuda')

    phases = ['build', 'install']

    def build(self, spec, prefix):
        ext_linalg = [spec['lapack'].libs.ld_flags]
        fcflags = []
        cflags = []
        
        if spec.satisfies('%gcc') or spec.satisfies('%clang'):
            fcflags.append("-ffree-form")
            fcflags.append("-ffree-line-length-none")

        if '+openmp' in spec:
            fcflags.append(self.compiler.openmp_flag)
            cflags.append(self.compiler.openmp_flag)

        if '+scalapack' in spec:
            ext_linalg.append(spec['scalapack'].libs.ld_flags)

        conf_options = [
            "../Installer.py",
            "build",
            "-y",
            "-c",
            "CC=%s" % spec['mpi'].mpicc,
            "CXX=%s" % spec['mpi'].mpicxx,
            "FC=%s" % spec['mpi'].mpifc,
            "F77=%s" % spec['mpi'].mpif77,
            "FCFLAGS='%s'" % " ".join(fcflags),
            "CFLAGS='%s'" % " ".join(cflags),
            "--with-gobject=yes",
            "--with-ext-linalg=\'%s\'" % " ".join(ext_linalg),
        ]

        if '+cuda' in spec:
            conf_options.append("--enable-opencl")
            conf_options.append("--with-ocl-path=%s" % spec['cuda'].prefix)
            conf_options.append("--enable-cuda-gpu")
            conf_options.append("--with-cuda-path=%s" % spec['cuda'].prefix)

        sh = which('python')
        with working_dir('build', create=True):
            sh(*conf_options)

    def install(self, spec, prefix):
        install_tree(join_path('build', 'install'), prefix)
