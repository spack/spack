# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class NfftBase(AutotoolsPackage):
    """Base class for building Nfft."""

    variant(
        'precision', values=any_combination_of(
            'float', 'double', 'long_double'
        ).prohibit_empty_set().with_default('float,double'),
        description='Build the selected floating-point precision libraries'
    )

    @property
    def selected_precisions(self):
        """Precisions that have been selected in this build"""
        return self.spec.variants['precision'].value

    def configure(self, spec, prefix):
        # Base options
        options = ['--prefix={0}'.format(prefix),
                   '--with-fftw3=%s'  % spec['fftw'].prefix]

        # Double is the default precision, for all the others we need
        # to enable the corresponding option.
        enable_precision = {
            'float': ['--enable-float'],
            'double': None,
            'long_double': ['--enable-long-double'],
        }

        # Different precisions must be configured and compiled one at a time
        configure = Executable('../configure')
        for precision in self.selected_precisions:
            opts = (enable_precision[precision] or []) + options[:]

            with working_dir(precision, create=True):
                configure(*opts)

    def for_each_precision_make(self, *targets):
        for precision in self.selected_precisions:
            with working_dir(precision):
                make(*targets)

    def build(self, spec, prefix):
        self.for_each_precision_make()

    def check(self):
        self.for_each_precision_make('check')

    def install(self, spec, prefix):
        self.for_each_precision_make('install')


class Nfft(NfftBase):
    """NFFT is a C subroutine library for computing the nonequispaced discrete
    Fourier transform (NDFT) in one or more dimensions, of arbitrary input
    size, and of complex data."""

    homepage = "https://www-user.tu-chemnitz.de/~potts/nfft"
    url = "https://github.com/NFFT/nfft/releases/download/3.5.2/nfft-3.5.2.tar.gz"

    version('3.5.2', sha256='cf3b2f3b2eabd79e49a5fbabf7f8d73fc3c57c4f68ae71e29f6dead853ab2901')
    version('3.4.1', sha256='1cf6060eec0afabbbba323929d8222397a77fa8661ca74927932499db26b4aaf')
    version('3.3.2', sha256='9dcebd905a82c4f0a339d0d5e666b68c507169d9173b66d5ac588aae5d50b57c')

    depends_on('fftw')
