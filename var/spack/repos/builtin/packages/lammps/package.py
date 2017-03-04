##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
#
# Please also see the LICENSE file for our notice and the LGPL.
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *
import os
import string
import datetime as dt


class Lammps(MakefilePackage):
    """LAMMPS stands for Large-scale Atomic/Molecular Massively
    Parallel Simulator."""
    homepage = "http://lammps.sandia.gov/"
    url      = "https://github.com/lammps/lammps/archive/stable_17Nov2016.tar.gz"

    version('2016.11.17', '8aecc58a39f9775203517c62a592d13b')

    def url_for_version(self, version):
        vdate = dt.datetime.strptime(str(version), "%Y.%m.%d")
        return "https://github.com/lammps/lammps/archive/stable_{0}.tar.gz".format(
            vdate.strftime("%d%b%Y"))

    supported_packages = ['voronoi', 'rigid', 'user-nc-dump',
                          'user-atc', 'meam', 'manybody']

    for pkg in supported_packages:
        variant(pkg, default=False,
                description='Activate the {0} package'.format(pkg))
    variant('lib', default=True,
            description='Build the liblammps in addition to the executable')

    depends_on('mpi')
    depends_on('fftw')
    depends_on('voropp', when='+voronoi')
    depends_on('netcdf+mpi', when='+user-nc-dump')
    depends_on('blas', when='+user-atc')
    depends_on('lapack', when='+user-atc')

    def setup_environment(self, spack_env, run_env):
        self.target_name = self.compiler.name

    def edit(self, spec, prefix):
        config = []

        config.append('CC = c++')
        if self.compiler.name == 'intel':
            # This is taken from MAKE/OPTIONS/Makefile.intel_cpu_intelmpi
            config.append('OPTFLAGS = -xHost -O2 -fp-model fast=2 -no-prec-div -qoverride-limits')  # noqa: E501
            config.append('CCFLAGS = -g -qopenmp -DLAMMPS_MEMALIGN=64 -no-offload -fno-alias -ansi-alias -restrict $(OPTFLAGS)')  # noqa: E501
            config.append('LINKFLAGS = -qopenmp $(OPTFLAGS)')
        else:
            # This is taken from MAKE/OPTIONS/Makefile.g++
            config.append('OPTFLAGS = -O3')
            config.append('CCFLAGS = -fopenmp')
            config.append('LINKFLAGS = -fopenmp $(OPTFLAGS)')

        config.append('SHFLAGS = -fPIC')
        config.append('DEPFLAGS = -M')
        config.append('LINK = c++')

        config.append('LIB = ')
        config.append('SIZE = size')

        config.append('ARCHIVE = ar')
        config.append('ARFLAGS = -rc')
        config.append('SHLIBFLAGS = -shared')

        config.append('LMP_INC = -DLAMMPS_GZIP')

        mpi_path = self.spec['mpi'].prefix.lib
        mpi_inc = self.spec['mpi'].prefix.include

        config.append(
            'MPI_INC = -DMPICH_SKIP_MPICXX -DOMPI_SKIP_MPICXX=1 -I{0}'.format(
                mpi_inc))
        config.append('MPI_PATH = -L{0}'.format(mpi_path))
        config.append('MPI_LIB = {0}'.format(
            ' '.join(self.spec['mpi'].mpicxx_shared_libs)))

        config.append('FFT_INC = -DFFT_FFTW3 -L{0}'.format(
            self.spec['fftw'].prefix.include))
        config.append('FFT_PATH = -L{0}'.format(self.spec['fftw'].prefix.lib))
        config.append('FFT_LIB = -lfftw3')

        config.append('JPG_INC = ')
        config.append('JPG_PATH = ')
        config.append('JPG_LIB = ')

        makefile_inc_template = \
            join_path(os.path.dirname(self.module.__file__),
                      'Makefile.inc')
        with open(makefile_inc_template, "r") as fhr:
            config.extend(fhr.read().split('\n'))

        with working_dir('src/MAKE/'):
            with open('Makefile.{0}'.format(self.target_name), 'w') as fh:
                fh.write('\n'.join(config))

    def build_meam(self):
        with working_dir('lib/meam'):
            filter_file(r'EXTRAMAKE = Makefile.lammps.ifort',
                        'EXTRAMAKE = Makefile.lammps.spack',
                        'Makefile.ifort')
            filter_file('F90 = *ifort',
                        'F90 = {0}'.format(self.compiler.fc),
                        'Makefile.ifort')

            with open('Makefile.lammps.spack', 'w') as fh:
                syslib = ''
                syspath = ''
                if self.compiler.name == 'gcc':
                    syslib = '-lgfortran'
                elif self.compiler.name == 'intel':
                    syslib = '-lifcore'

                makefile = ['meam_SYSINC =',
                            'meam_SYSLIB = {0}'.format(syslib),
                            'meam_SYSPATH = {0}'.format(syspath)]

                fh.write('\n'.join(makefile))

            make('lib', '-f', 'Makefile.ifort')

    def build_user_atc(self):
        with working_dir('lib/atc'):
            filter_file(r'CC =.*',
                        'CC = {0}'.format(self.compiler.cxx),
                        'Makefile.icc')

            mpi_include = self.spec['mpi'].prefix.include

            filter_file(r'CCFLAGS = *',
                        'CCFLAGS = -I{0} '.format(mpi_include),
                        'Makefile.icc')

            filter_file('LINK =.*',
                        'LINK = {0}'.format(self.compiler.cxx),
                        'Makefile.icc')

            make('lib', '-f', 'Makefile.icc')
            with open('Makefile.lammps', 'w') as fh:
                lapack_blas = (self.spec['lapack'].libs +
                               self.spec['blas'].libs)
                makefile = [
                    'user-atc_SYSINC =',
                    'user-atc_SYSLIB = {0}'.format(lapack_blas.ld_flags),
                    'user-atc_SYSPATH = ']
                fh.write('\n'.join(makefile))

    def build_voronoi(self):
        # no need to set the voronoi_SYS variable in Makefile.lammps
        # since the spack wrapper takes care of the path
        with working_dir('src/VORONOI'):
            filter_file(r'#include "voro\+\+\.hh"',
                        '#include <voro++/voro++.hh>',
                        'compute_voronoi_atom.h')

    def build(self, spec, prefix):
        for pkg in self.supported_packages:
            _build_pkg_name = string.replace('build_{0}'.format(pkg), '-', '_')
            if hasattr(self, _build_pkg_name):
                _build_pkg = getattr(self, _build_pkg_name)
                _build_pkg()

        with working_dir('src'):
            for pkg in self.supported_packages:
                if '+{0}'.format(pkg) in spec:
                    make('yes-{0}'.format(pkg))

            make(self.target_name)

            if '+lib' in spec:
                make('mode=shlib', self.target_name)

    def install(self, spec, prefix):
        with working_dir('src'):
            mkdirp(prefix.bin)
            install('lmp_{0}'.format(self.target_name), prefix.bin)

            if '+lib' in spec:
                mkdirp(prefix.lib)
                install('liblammps_{0}.{1}'.format(self.target_name,
                                                   dso_suffix), prefix.lib)

                # TODO: install the necessary headers
                mkdirp(prefix.include)
