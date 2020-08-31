# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

import glob
import tempfile


class Wrf(Package):
    """The Weather Research and Forecasting (WRF) Model
    is a next-generation mesoscale numerical weather prediction system designed
    for both atmospheric research and operational forecasting applications.
    """

    homepage = "https://www.mmm.ucar.edu/weather-research-and-forecasting-model"
    url      = "https://github.com/wrf-model/WRF/archive/v4.2.tar.gz"

    version('4.2', sha256='c39a1464fd5c439134bbd39be632f7ce1afd9a82ad726737e37228c6a3d74706')
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

    variant('pnetcdf', default=True,
            description='Parallel IO support through Pnetcdf libray')

    # These patches deal with netcdf & netcdf-fortran being two diff things
    # Patches are based on:
    # https://github.com/easybuilders/easybuild-easyconfigs/blob/master/easybuild/easyconfigs/w/WRF/WRF-3.5_netCDF-Fortran_separate_path.patch
    patch('patches/4.0/arch.Config.pl.patch', when='@4.0')
    patch('patches/4.0/arch.configure.defaults.patch', when='@4.0')
    patch('patches/4.0/arch.conf_tokens.patch', when='@4.0')
    patch('patches/4.0/arch.postamble.patch', when='@4.0')
    patch('patches/4.0/configure.patch', when='@4.0')
    patch('patches/4.0/external.io_netcdf.makefile.patch', when='@4.0')
    patch('patches/4.0/Makefile.patch', when='@4.0')

    patch('patches/4.2/arch.Config.pl.patch', when='@4.2')
    patch('patches/4.2/arch.configure.defaults.patch', when='@4.2')
    patch('patches/4.2/arch.conf_tokens.patch', when='@4.2')
    patch('patches/4.2/arch.postamble.patch', when='@4.2')
    patch('patches/4.2/configure.patch', when='@4.2')
    patch('patches/4.2/external.io_netcdf.makefile.patch', when='@4.2')
    patch('patches/4.2/var.gen_be.Makefile.patch', when='@4.2')
    patch('patches/4.2/Makefile.patch', when='@4.2')

    depends_on('mpi')
    # According to:
    # http://www2.mmm.ucar.edu/wrf/users/docs/user_guide_v4/v4.0/users_guide_chap2.html#_Required_Compilers_and_1
    # Section: "Required/Optional Libraries to Download"
    depends_on('parallel-netcdf', when='+pnetcdf')
    depends_on('netcdf-c+parallel-netcdf')
    depends_on('netcdf-fortran')
    depends_on('jasper')
    depends_on('libpng')
    depends_on('zlib')
    depends_on('perl')
    # not sure if +fortran is required, but seems like a good idea
    depends_on('hdf5+fortran+hl+mpi')
    # build script use csh
    depends_on('tcsh', type=('build'))
    # time is not installed on all systems b/c bash provides it
    # this fixes that for csh install scripts
    depends_on('time', type=('build'))

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('m4', type='build')
    depends_on('libtool', type='build')
    phases = ['configure', 'build', 'install']

    def setup_build_environment(self, spack_env):
        spack_env.set('NETCDF', self.spec['netcdf-c'].prefix)
        if '+pnetcdf' in self.spec:
            spack_env.set('PNETCDF', self.spec['parallel-netcdf'].prefix)
        # This gets used via the applied patch files
        spack_env.set('NETCDFF', self.spec['netcdf-fortran'].prefix)
        spack_env.set('PHDF5', self.spec['hdf5'].prefix)
        spack_env.set('JASPERINC', self.spec['jasper'].prefix.include)
        spack_env.set('JASPERLIB', self.spec['jasper'].prefix.lib)

        if self.spec.satisfies('%gcc@10:'):
            args = '-w -O2 -fallow-argument-mismatch -fallow-invalid-boz'
            spack_env.set('FCFLAGS', args)
            spack_env.set('FFLAGS', args)

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

        with tempfile.TemporaryFile(mode='w') as fp:
            fp.write(build_type + '\n' + nesting_value + '\n')
            fp.seek(0)
            Executable('./configure')(input=fp)

    def build(self, spec, prefix):
        csh = which('csh')
        # num of compile jobs capped at 20 in wrf
        csh('./compile', '-j', str(min(int(make_jobs), 20)),
            spec.variants['compile_type'].value)

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install('./main/wrf.exe', prefix.bin)
        install('./main/ndown.exe', prefix.bin)
        install('./main/real.exe', prefix.bin)
