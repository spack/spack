# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Regcm(AutotoolsPackage):
    '''RegCM, ICTP Regional Climate Model (https://ictp.it).'''

    homepage = 'https://gforge.ictp.it/gf/project/regcm/'

    version('4.7.1-SVN6884',
            sha256='fd4eb0fbe911c6c4dacbaaf2a952a45ac8c1fa54a5d905972ffe592e47818c00',
            url='http://clima-dods.ictp.it/Users/ggiulian/RegCM-SVN6884.tar.gz')
    version('4.7.1-SVN6875',
            sha256='112c9cc2e234197c70688bb31b187da3298eb2a2ff15a119838ae8d64338f296',
            url='file:///lustre/exact/achiusole/regcm/RegCM-4.7.1-SVN6875.tar.gz')
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
    # architecture provided (in the configure), so we allow a single arch on
    # GCC. Only GCC and Intel are supported.
    extensions = ('knl', 'skl', 'bdw', 'nhl')
    variant('extension', default=None, values=extensions, multi=True,
            description='Build extensions for a specific architecture. '
                        'Only available on GCC and Intel; GCC allows a single '
                        'architecture optimization.')

    variant('pnetcdf', default=False,
            description='Build NetCDF using the high performance parallel '
                        'NetCDF implementation.')

    depends_on('netcdf')
    depends_on('netcdf-fortran')
    depends_on('hdf5')
    depends_on('mpi')
    depends_on('netcdf +parallel-netcdf', when='+pnetcdf')

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

        optimizations = self.spec.variants['extension'].value
        if len(optimizations) > 1 and self.spec.satisfies('%gcc'):
            # https://github.com/spack/spack/issues/974
            raise InstallError('The GCC compiler does not support multiple '
                               'architecture optimizations.')

        if optimizations[0] and (self.spec.satisfies('%gcc') or
                                 self.spec.satisfies('%intel')):
            args += ('--enable-' + ext for ext in optimizations)
        elif optimizations[0]:
            # This means the user chose some optimizations on a different
            # compiler from GCC and Intel, which are the only compiler
            # supported with RegCM 4.7.x.
            raise InstallError('Architecture optimizations are available only '
                               'for GCC and Intel compilers.')

        for opt in ('debug', 'profile', 'singleprecision'):
            if '+{0}'.format(opt) in self.spec:
                args.append('--enable-' + opt)

        # RegCM doesn't listen to the FFLAGS variable, so we have to convert it
        # to FCFLAGS.
        fcflags = list(self.spec.compiler_flags['fflags'])

        # RegCM complains when compiled with gfortran.
        if self.compiler.fc.endswith('gfortran'):
            fcflags.append('-fno-range-check')

        args.append('FCFLAGS=' + ' '.join(fcflags))

        # The configure needs a hint on the MPI Fortran compiler, otherwise it
        # doesn't find it and tries to compile MPI Fortran code with the system
        # Fortran non-MPI compiler.
        args.append('MPIFC=' + self.spec['mpi'].mpifc)

        return args
