# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Pfft(AutotoolsPackage):
    """PFFT is a software library for computing massively parallel,
       fast Fourier transformations on distributed memory architectures.
       PFFT can be understood as a generalization of FFTW-MPI to
       multidimensional data decomposition."""

    homepage = "https://www-user.tu-chemnitz.de/~potts/workgroup/pippig/software.php.en"
    url      = "https://www-user.tu-chemnitz.de/~potts/workgroup/pippig/software/pfft-1.0.8-alpha.tar.gz"

    version('1.0.8-alpha', sha256='6c43960ad72fcff7e49b87c604c5f471fb5890f1bd11ce750ab52f035e7c5317')

    depends_on('fftw+mpi+pfft_patches')
    depends_on('mpi')

    def configure(self, spec, prefix):
        options = ['--prefix={0}'.format(prefix)]
        if not self.compiler.f77 or not self.compiler.fc:
            options.append("--disable-fortran")

        configure = Executable('../configure')

        fftw_precisions = spec['fftw'].variants.get('precision')
        if 'double' in fftw_precisions:
            with working_dir('double', create=True):
                configure(*options)
        if 'float' in fftw_precisions:
            with working_dir('float', create=True):
                configure('--enable-float', *options)
        if 'long_double' in fftw_precisions:
            with working_dir('long-double', create=True):
                configure('--enable-long-double', *options)

    def build(self, spec, prefix):
        fftw_precisions = spec['fftw'].variants.get('precision')
        if 'double' in fftw_precisions:
            with working_dir('double'):
                make()
        if 'float' in fftw_precisions:
            with working_dir('float'):
                make()
        if 'long_double' in fftw_precisions:
            with working_dir('long-double'):
                make()

    def check(self):
        spec = self.spec
        fftw_precisions = spec['fftw'].variants.get('precision')
        if 'double' in fftw_precisions:
            with working_dir('double'):
                make("check")
        if 'float' in fftw_precisions:
            with working_dir('float'):
                make("check")
        if 'long_double' in fftw_precisions:
            with working_dir('long-double'):
                make("check")

    def install(self, spec, prefix):
        fftw_precisions = spec['fftw'].variants.get('precision')
        if 'double' in fftw_precisions:
            with working_dir('double'):
                make("install")
        if 'float' in fftw_precisions:
            with working_dir('float'):
                make("install")
        if 'long_double' in fftw_precisions:
            with working_dir('long-double'):
                make("install")
