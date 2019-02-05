# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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

    # On Intel and PGI compilers, multiple archs can be built at the same time,
    # producing a so-called fat binary. Unfortunately, gcc builds only the last
    # architecture provided (in the configure), so we allow a single arch.
    extensions = ('knl', 'skl', 'bdw', 'nhl')
    variant(
        'extension', values=any_combination_of(extensions),
        description='Build extensions for a specific Intel architecture.'
    )

    depends_on('netcdf')
    depends_on('netcdf-fortran')
    depends_on('hdf5')
    depends_on('mpi')

    # 'make' sometimes crashes when compiling with more than 10-12 cores.
    # Moreover, parallel compile time is ~ 1m 30s, while serial is ~ 50s.
    parallel = False

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

        for opt in ('debug', 'profile', 'singleprecision'):
            if '+{0}'.format(opt) in self.spec:
                args.append('--enable-' + opt)

        for ext in self.extensions:
            if 'extension={0}'.format(ext) in self.spec:
                args.append('--enable-' + ext)
                break

        # RegCM complains when compiled with gfortran, and unfortunately FFLAGS
        # is ignored by the configure, so we need to set the option in FCFLAGS.
        if self.compiler.fc.endswith('gfortran'):
            args.append('FCFLAGS=-fno-range-check')

        return args
