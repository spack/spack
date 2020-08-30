# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

import glob
import tempfile
from os.path import dirname,join
import multiprocessing as mp

class Wps(AutotoolsPackage):
    """The Weather Research and Forecasting Pre-Processing System (WPS)
    """

    homepage = "https://www.mmm.ucar.edu/weather-research-and-forecasting-model"
    #url      = "https://www2.mmm.ucar.edu/wrf/src/WPSV4.0.TAR.gz"
    url      = "https://github.com/wrf-model/WPS/archive/v4.2.tar.gz"

    version('4.2', sha256='3e175d033355d3e7638be75bc7c0bc0de6da299ebd175a9bbc1b7a121acd0168')

    variant('build_type', default='dmpar',
            values=('serial', 'serial_NO_GRIB2', 'dmpar', 'dmpar_NO_GRIB2'))

    patch('patches/4.2/arch.Config.pl.patch', when='@4.2')
    patch('patches/4.2/arch.configure.defaults.patch', when='@4.2')
    patch('patches/4.2/configure.patch', when='@4.2')
    patch('patches/4.2/preamble.patch', when='@4.2')


    depends_on('mpi')
    depends_on('wrf')
    # According to:
    # http://www2.mmm.ucar.edu/wrf/users/docs/user_guide_v4/v4.0/users_guide_chap2.html#_Required_Compilers_and_1
    # Section: "Required/Optional Libraries to Download"
    # parallel netcdf should not be used
    depends_on('netcdf-c+parallel-netcdf')
    depends_on('parallel-netcdf')
    depends_on('netcdf-fortran')
    # not sure if +fortran is required, but seems like a good idea
    depends_on('hdf5+fortran+hl')
    # build script use csh
    depends_on('tcsh', type=('build'))
    # time is not installed on all systems b/c bash provides it
    # this fixes that for csh install scripts
    depends_on('time', type=('build'))

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('m4', type='build')
    depends_on('libtool', type='build')
    depends_on('jasper')

    def setup_environment(self, spack_env, run_env):
        spack_env.set('NETCDF', self.spec['netcdf-c'].prefix)
        # This gets used via the applied patch files
        spack_env.set('NETCDFF', self.spec['netcdf-fortran'].prefix)
        spack_env.set('JASPERINC', self.spec['jasper'].prefix.include)
        spack_env.set('JASPERLIB', self.spec['jasper'].prefix.lib)

        # This is a hack - we need to use WRF staging ("spack install -- wrf")
        spack_env.set('WRF_DIR', join(glob.glob(join(dirname(dirname(self.stage.source_path)), "spack-stage-wrf-%s-*" % str(self.version)))[0], "spack-src"))

        if self.spec.satisfies('%gcc@10:'):
            spack_env.set('FCFLAGS', '-w -O2 -fallow-argument-mismatch -fallow-invalid-boz')
            spack_env.set('FFLAGS', '-w -O2 -fallow-argument-mismatch -fallow-invalid-boz')

        spack_env.prepend_path('PATH', dirname(self.compiler.fc))

    def patch(self):
        # Let's not assume csh is intalled in bin
        files = glob.glob('*.csh')

        filter_file('^#!/bin/csh -f', '#!/usr/bin/env csh', *files)
        filter_file('^#!/bin/csh', '#!/usr/bin/env csh', *files)

    def configure(self, spec, prefix):
        build_opts = {"gcc":   {"serial": '1',
                                "serial_NO_GRIB2": '2',
                                "dmpar":           '3',
                                "dmpar_NO_GRIB2":  '4'},
                      "intel": {"serial":          '17',
                                "serial_NO_GRIB2": '18',
                                "dmpar":           '19',
                                "dmpar_NO_GRIB2":  '20'},
                      "pgi":   {"serial":          '5',
                                "serial_NO_GRIB2": '6',
                                "dmpar":           '7',
                                "dmpar_NO_GRIB2":  '8'},
                      }

        try:
            compiler_opts = build_opts[self.spec.compiler.name]
        except KeyError:
            raise InstallError("Compiler not recognized nor supported.")

        # Spack already makes sure that the variant value is part of the set.
        build_type = compiler_opts[spec.variants['build_type'].value]

        with tempfile.TemporaryFile(mode='w') as fp:
            fp.write(build_type + '\n')
            fp.seek(0)
            Executable('./configure')(input=fp)

    def build(self, spec, prefix):
        csh = which('csh')
        csh('./compile')

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install('./geogrid/src/geogrid.exe', prefix.bin)
        install('./metgrid/src/metgrid.exe', prefix.bin)
