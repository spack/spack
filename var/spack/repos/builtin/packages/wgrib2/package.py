# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install wgrib
#
# You can edit this file again by typing:
#
#     spack edit wgrib
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

import os
import sys
import re

from spack import *


class Wgrib2(MakefilePackage):
    """Utility for interacting with grib2 files"""

    homepage = "https://www.cpc.ncep.noaa.gov/products/wesley/wgrib2"
    url = "https://www.ftp.cpc.ncep.noaa.gov/wd51we/wgrib2/wgrib2.tgz.v2.0.8"

    maintainers = ['kgerheiser', 'Hang-Lei-NOAA']

    version('2.0.7', sha256='d7f1a4f9872922c62b3c7818c022465532cca1f5666b75d3ac5735f0b2747793', extension='tar.gz')
    version('2.0.8', sha256='5e6a0d6807591aa2a190d35401606f7e903d5485719655aea1c4866cc2828160', extension='tar.gz')
    version('3.1.0', sha256='5757ef9016b19ae87491918e0853dce2d3616b14f8c42efe3b2f41219c16b78f', extension='tar.gz')
    version('3.1.1', sha256='9236f6afddad76d868c2cfdf5c4227f5bdda5e85ae40c18bafb37218e49bc04a', extension='tar.gz')

    variant('netcdf3', default=True,
            description='Link in netcdf3 library to write netcdf3 files')
    variant('netcdf4', default=False,
            description='Link in netcdf4 library to write netcdf3/4 files')
    variant('ipolates', default='3',
            description='Link in IPOLATES library to interpolate to new grids (0=OFF, 1=ip, 3=ip2)',
            values=('0', '1', '3'))
    variant('spectral', default=False,
            description='Spectral interpolation in -new_grid')
    variant('fortran_api', default=True,
            description='Make wgrib2api which allows fortran code to read/write grib2')
    variant('mysql', default=False,
            description='Link in interface to MySQL to write to mysql database')
    variant('udf', default=False,
            description='Add commands for user-defined functions and shell commands')
    variant('regex', default=True,
            description='Use regular expression library (POSIX-2')
    variant('tigge', default=True,
            description='Ability for TIGGE-like variable names')
    variant('proj4', default=False,
            description='The proj4 library is used to confirm that the gctpc code is working correctly')
    variant('aec', default=True,
            description='Enable use of the libaec library for packing with GRIB2 template')
    variant('g2c', default=False,
            description='include NCEP g2clib (mainly for testing purposes)')
    variant('disable_timezone', default=False,
            description='Some machines do not support timezones')
    variant('disable_alarm', default=False,
            description='Some machines do not support alarm(..) (not POSIX-1, IEEE Std 1003.1) use the alarm to terminate wgrib2 after N seconds')
    variant('png', default=True, description='PNG encoding')
    variant('jasper', default=True, description='JPEG compression using Jasper')
    variant('openmp', default=True, description='OpenMP parallelization')
    variant('wmo_validation', default=False, description='WMO validation')

    conflicts('+openmp', when='%apple-clang')

    variant_map = {
        'netcdf3': 'USE_NETCDF3',
        'netcdf4': 'USE_NETCDF4',
        'spectral': 'USE_SPECTRAL',
        'mysql': 'USE_MYSQL',
        'udf': 'USE_UDF',
        'regex': 'USE_REGEX',
        'tigge': 'USE_TIGGE',
        'proj4': 'USE_PROJ4',
        'aec': 'USE_AEC',
        'g2c': 'USE_G2CLIB',
        'png': 'USE_PNG',
        'jasper': 'USE_JASPER',
        'openmp': 'USE_OPENMP',
        'wmo_validation': 'USE_WMO_VALIDATION',
        'ipolates': 'USE_IPOLATES',
        'disable_timezone': 'DISABLE_TIMEZONE',
        'disable_alarm': 'DISABLE_ALARM',
        'fortran_api': 'MAKE_FTN_API'
    }

    # Disable parallel build
    parallel = False

    # Use Spack compiler wrapper flags
    def inject_flags(self, name, flags):
        if name == 'cflags':
            if self.spec.compiler.name == 'apple-clang':
                flags.append('-Wno-error=implicit-function-declaration')

            # When mixing Clang/gfortran need to link to -lgfortran
            # Find this by searching for gfortran/../lib
            if self.spec.compiler.name in ['apple-clang', 'clang']:
                if 'gfortran' in self.compiler.fc:
                    output = Executable(self.compiler.fc)('-###', output=str, error=str)
                    libdir = re.search('--libdir=(.+?) ', output).group(1)
                    flags.append('-L{}'.format(libdir))
    
        return (flags, None, None)

    flag_handler = inject_flags

    def url_for_version(self, version):
        url = "https://www.ftp.cpc.ncep.noaa.gov/wd51we/wgrib2/wgrib2.tgz.v{}"
        return url.format(version)

    def edit(self, spec, prefix):
        makefile = FileFilter('makefile')

        # ifort no longer accepts -openmp
        makefile.filter(r'-openmp', '-qopenmp')
        makefile.filter(r'-Wall', ' ')
        makefile.filter(r'-Werror=format-security', ' ')

        # clang doesn't understand --fast-math
        if spec.satisfies('%clang') or spec.satisfies('%apple-clang'):
            makefile.filter(r'--fast-math', '-ffast-math')

        for variant_name, makefile_option in self.variant_map.items():
            value = int(spec.variants[variant_name].value)
            makefile.filter(r'^%s=.*' % makefile_option,
                            '{}={}'.format(makefile_option, value))

    def setup_build_environment(self, env):

        if self.spec.compiler.name in 'intel':
            comp_sys = 'intel_linux'
        elif self.spec.compiler.name in ['gcc', 'clang', 'apple-clang']:
            comp_sys = 'gnu_linux'

        env.set('COMP_SYS', comp_sys)

    def build(self, spec, prefix):
        make()

        # Move wgrib2 executable to a tempoary directory
        mkdir('install')
        mkdir(join_path('install', 'bin'))
        move(join_path('wgrib2', 'wgrib2'), join_path('install', 'bin'))

        # Build wgrib2 library by disabling all options
        # and enabling only MAKE_FTN_API=1
        if '+fortran_api' in spec:
            make('clean')
            make('deep-clean')
            makefile = FileFilter('makefile')

            # Disable all options
            for variant_name, makefile_option in self.variant_map.items():
                value = 0
                makefile.filter(r'^%s=.*' % makefile_option,
                                '{}={}'.format(makefile_option, value))

            # Enable MAKE_FTN_API to build library and USE_REGEX (there is a bug when off)
            makefile.filter(r'^MAKE_FTN_API=.*', 'MAKE_FTN_API=1')
            makefile.filter(r'^USE_REGEX=.*', 'USE_REGEX=1')
            make('lib')
            mkdir(join_path('install', 'lib'))
            mkdir(join_path('install', 'include'))

            move(join_path('lib', 'libwgrib2.a'),
                 join_path('install', 'lib'))
            move(join_path('lib', 'wgrib2api.mod'),
                 join_path('install', 'include'))
            move(join_path('lib', 'wgrib2lowapi.mod'),
                 join_path('install', 'include'))

    def install(self, spec, prefix):
        install_tree('install/', prefix)
