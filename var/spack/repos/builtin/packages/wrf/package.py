# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import glob


class Wrf(AutotoolsPackage):
    """The Weather Research and Forecasting (WRF) Model
    is a next-generation mesoscale numerical weather prediction system designed
    for both atmospheric research and operational forecasting applications"""

    homepage = "https://www.mmm.ucar.edu/weather-research-and-forecasting-model"
    url      = "http://www2.mmm.ucar.edu/wrf/src/WRFV3.9.1.TAR.gz"

    version('4.0', sha256='a5b072492746f96a926badda7e6b44cb0af26695afdd6c029a94de5e1e5eec73')

    variant('build_type',
            default='dmpar',
            values=('serial', 'smpar', 'dmpar', 'dmsm'))

    variant('nesting',
            default='basic',
            values=('basic', 'preset', 'vortex')
           )

    variant('compile_type',
            default='em_real',
            values=('em_real', 'em_quarter_ss', 'em_b_wave', 'em_les',
                    'em_heldsuarez', 'em_tropical_cyclone', 'em_hill2d_x',
                    'em_squall2d_x', 'em_squall2d_y', 'em_grav2d_x',
                    'em_seabreeze2d_x', 'em_scm_xy')
           )

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
    # build scripts use csh
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

    def patch(self):
        # Let's not assume csh is intalled in bin
        files = glob.glob('*.csh')

        filter_file('^#!/bin/csh -f', '#!/usr/bin/env csh', *files)
        filter_file('^#!/bin/csh', '#!/usr/bin/env csh', *files)

    def configure(self, spec, prefix):
        if spec.variants['build_type'].value == 'dmpar':
            build_type_value = '34'
        if spec.variants['nesting'].value == 'basic':
            nesting_value = '1'

        install_answer = [build_type_value + '\n', nesting_value + '\n']
        install_answer_input = 'spack-config.in'
        with open(install_answer_input, 'w') as f:
            f.writelines(install_answer)
        with open(install_answer_input, 'r') as f:
            bash = which('bash')
            bash('./configure', input=f)

    def build(self, spec, prefix):
        sh = which('csh')
        sh('./compile', spec.variants['compile_type'].value)

    def install(self, spec, prefix):
        install('main/wrf.exe', prefix.bin)
        install('main/ndown.exe', prefix.bin)
        install('main/real.exe', prefix.bin)
