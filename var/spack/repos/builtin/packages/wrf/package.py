# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

import glob
import tempfile
from os.path import dirname
import multiprocessing as mp

class Wrf(AutotoolsPackage):
    """The Weather Research and Forecasting (WRF) Model
    is a next-generation mesoscale numerical weather prediction system designed
    for both atmospheric research and operational forecasting applications.
    """

    homepage = "https://www.mmm.ucar.edu/weather-research-and-forecasting-model"
    url      = "http://www2.mmm.ucar.edu/wrf/src/WRFV3.9.1.TAR.gz"

    version('4.0', sha256='a5b072492746f96a926badda7e6b44cb0af26695afdd6c029a94de5e1e5eec73')

    variant('build_type', default='dmpar',
            values=('serial', 'smpar', 'dmpar', 'dmsm'))

    variant('nesting', default='basic',
            values=('basic', 'preset', 'vortex'))

    variant('compile_type', default='em_real',
            values=('em_real', 'em_quarter_ss', 'em_b_wave', 'em_les',
                    'em_heldsuarez', 'em_tropical_cyclone', 'em_hill2d_x',
                    'em_squall2d_x', 'em_squall2d_y', 'em_grav2d_x',
                    'em_seabreeze2d_x', 'em_scm_xy'))

    # These patches deal with netcdf & netcdf-fortran being two diff things
    # Patches are based on:
    # https://github.com/easybuilders/easybuild-easyconfigs/blob/master/easybuild/easyconfigs/w/WRF/WRF-3.5_netCDF-Fortran_separate_path.patch
    patch('patches/4.0/arch.Config.pl.patch')
    patch('patches/4.0/arch.configure.defaults.patch')
    patch('patches/4.0/arch.conf_tokens.patch')
    patch('patches/4.0/arch.postamble.patch')
    patch('patches/4.0/configure.patch')
    patch('patches/4.0/external.io_netcdf.makefile.patch')
    patch('patches/4.0/Makefile.patch')

    depends_on('mpi')
    # According to:
    # http://www2.mmm.ucar.edu/wrf/users/docs/user_guide_v4/v4.0/users_guide_chap2.html#_Required_Compilers_and_1
    # Section: "Required/Optional Libraries to Download"
    # parallel netcdf should not be used
    depends_on('netcdf~parallel-netcdf')
    depends_on('netcdf-fortran')
    depends_on('jasper')
    depends_on('libpng')
    depends_on('zlib')
    depends_on('perl')
    # not sure if +fortran is required, but seems like a good idea
    depends_on('hdf5+fortran')
    # build script use csh
    depends_on('tcsh', type=('build'))
    # time is not installed on all systems b/c bash provides it
    # this fixes that for csh install scripts
    depends_on('time', type=('build'))

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('m4', type='build')
    depends_on('libtool', type='build')

    def setup_environment(self, spack_env, run_env):
        spack_env.set('NETCDF', self.spec['netcdf'].prefix)
        # This gets used via the applied patch files
        spack_env.set('NETCDFF', self.spec['netcdf-fortran'].prefix)

        spack_env.prepend_path('PATH', dirname(self.compiler.fc))

    def patch(self):
        # Let's not assume csh is intalled in bin
        files = glob.glob('*.csh')

        filter_file('^#!/bin/csh -f', '#!/usr/bin/env csh', *files)
        filter_file('^#!/bin/csh', '#!/usr/bin/env csh', *files)

    def configure(self, spec, prefix):
        build_opts = {"gcc":   {"serial": '32',
                                "smpar":  '33',
                                "dmpar":  '34',
                                "dmsm":   '35'},
                      "intel": {"serial": '13',
                                "smpar":  '14',
                                "dmpar":  '15',
                                "dmsm":   '16'},
                      "pgi":   {"serial": '52',
                                "smpar":  '53',
                                "dmpar":  '54',
                                "dmsm":   '55'},
                      }

        nesting_opts = {"basic":  "1",
                        "preset": "2",
                        "vortex": "3"}

        try:
            compiler_opts = build_opts[self.spec.compiler.name]
        except KeyError:
            raise InstallError("Compiler not recognized nor supported.")

        # Spack already makes sure that the variant value is part of the set.
        build_type = compiler_opts[spec.variants['build_type'].value]

        nesting_value = nesting_opts[spec.variants['nesting'].value]

        with tempfile.TemporaryFile() as fp:
            fp.write(build_type + '\n' + nesting_value + '\n')
            fp.seek(0)
            Executable('./configure')(input=fp)

    def build(self, spec, prefix):
        csh = which('csh')
        csh('./compile', '-j', str(mp.cpu_count()), spec.variants['compile_type'].value)

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install('main/wrf.exe', prefix.bin)
        install('main/ndown.exe', prefix.bin)
        install('main/real.exe', prefix.bin)
