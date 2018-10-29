# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Regcm(AutotoolsPackage):
    """RegCM ICTP Regional Climate Model."""

    homepage = 'https://gforge.ictp.it/gf/project/regcm/'

    version('4.7.0', sha256='456631c10dcb83d70e51c3babda2f7a1aa41ed9e60cb4209deb3764655267519',
            url='https://gforge.ictp.it/gf/download/frsrelease/259/1845/RegCM-4.7.0.tar.gz')

    variant('debug', default=False,
            description='Build RegCM using debug options.')
    variant('profile', default=False,
            description='Build RegCM using profiling options.')
    variant('singleprecision', default=False,
            description='Build RegCM using single precision float type.')

    variant('knl', default=False,
            description='Build RegCM using Intel Xeon Phi options.')
    variant('skl', default=False,
            description='Build RegCM using Intel Sky Lake options.')
    variant('bdw', default=False,
            description='Build RegCM using Intel Broadwell (AVX2) options.')
    variant('nhl', default=False,
            description='Build RegCM using Intel Nehalem (SSE4.2) options.')

    depends_on('netcdf')
    depends_on('netcdf-fortran')
    depends_on('hdf5')
    depends_on('mpi')

    def flag_handler(self, name, flags):
        if name == 'fflags' and self.compiler.fc.endswith('gfortran'):
            flags.extend(['-Wall', '-Wextra', '-Warray-temporaries',
                          '-Wconversion', '-fimplicit-none', '-fbacktrace',
                          '-ffree-line-length-0', '-finit-real=nan',
                          '-ffpe-trap=zero,overflow,underflow', '-fcheck=all'])

        elif name == 'ldlibs':
            flags.extend(['-lnetcdff', '-lnetcdf'])
            if self.compiler.fc.endswith('gfortran'):
                flags.extend(['-lm', '-ldl'])
            else:
                flags.extend(['-lhdf5_hl', '-lhdf5', '-lz'])

        return (None, None, flags)

    def configure_args(self):
        args = ['--enable-shared']

        for opt in ('debug', 'profile', 'singleprecision',
                    'knl', 'skl', 'bdw', 'nhl'):
            if '+{}'.format(opt) in self.spec:
                args.append('--enable-{}'.format(opt))

        # RegCM complains when compiled with gfortran, and unfortunately FFLAGS
        # is ignored by the configure, so we need to set the option in FCFLAGS.
        if self.compiler.fc.endswith('gfortran'):
            args.append('FCFLAGS=-fno-range-check')

        return args
