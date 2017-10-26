##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
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
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install vasp
#
# You can edit this file again by typing:
#
#     spack edit vasp
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#:D
from spack import *
import shutil
import os

class Vasp(MakefilePackage):
    """The Vienna Ab initio Simulation Package (VASP) is a computer program for atomic scale materials modelling, e.g. electronic structure calculations and quantum-mechanical molecular dynamics, from first principles."""

    homepage = "https://www.vasp.at"

    version('5.4.4', '8ac646b108f974371eef398973373bf6')
    version('5.4.1', 'dfd537e43294e9df09c8b5c6916c6a2e')

    patch('patch.5.4.1.14032016', level=0, when='@5.4.1')
    patch('patch.5.4.1.03082016', level=1, when='@5.4.1')

    build_targets = ['all']

    depends_on('mpi%intel')
    depends_on('mkl')
    depends_on('wannier90@1.2%intel')

    parallel = False

    def url_for_version(self, version):
        return 'file:///opt/sources/vasp/{0}/vasp.{0}.tar.gz'.format(version, version)

    def setup_environment(self, spack_env, run_env):

        run_env.prepend_path('PATH', self.spec.prefix.bin)
        run_env.prepend_path('PATH', self.spec['mpi'].prefix.bin)
        run_env.prepend_path('LIBRARY_PATH', self.spec['mpi'].prefix.lib)
        run_env.prepend_path('LD_LIBRARY_PATH', self.spec['mpi'].prefix.lib)
        run_env.prepend_path('PKG_CONFIG_PATH', join_path(self.spec['mpi'].prefix.lib, 'pkgconfig'))
        run_env.prepend_path('CPATH', self.spec['mpi'].prefix.include)

    def edit(self, spec, prefix):

        shutil.copy('arch/makefile.include.linux_intel', 'makefile.include')

        makefile = FileFilter('makefile.include')
        makefile.filter('FC         = .*', 'FC         = %s' % spec['mpi'].mpifc)
        makefile.filter('OFLAG      = .*', 'OFLAG      = -O2 -ip')
        makefile.filter('BLACS      = .*', 'BLACS      = -lmkl_blacs_openmpi_lp64')
        makefile.filter('LLIBS      = .*', 'LLIBS      = %s/lib/libwannier.a $(SCALAPACK) $(LAPACK) $(BLAS)' % self.spec['wannier90'].prefix)
        makefile.filter('OBJECTS    = .*', 'OBJECTS    = fftmpiw.o fftmpi_map.o fft3dlib.o fftw3d.o \\ $(MKLROOT)/interfaces/fftw3xf/libfftw3xf_intel.a')
        makefile.filter('CPP_LIB    = .*', 'CPP_LIB    = $(CPP) -DLONGCHAR')
        makefile.filter('CC_LIB     = .*', 'CC_LIB     = %s' % spec['mpi'].mpicc)

        if spec.satisfies('@5.4.1'):
            makefile.filter('CPP_OPTIONS= .*', 'CPP_OPTIONS= -DMPI -DHOST=\\"RC_Workstations\\" -DIFC \\')
            makefile.filter('-DCACHE_SIZE=.*', '-DCACHE_SIZE=12000 -DPGF90 -Davoidalloc \\')
            makefile.filter('-Duse_shmem.*', '-Duse_shmem -Dtbdyn -DVASP2WANNIER90 -DRPROMU_DGEMV -DRACCMU_DGEMV -DnoSTOPCAR -Ddo_loops')
            makefile.filter('FCL        = .*', 'FCL        = %s -mkl=sequential' % spec['mpi'].mpifc)
        else:
            makefile.filter('CPP_OPTIONS= .*', 'CPP_OPTIONS= -DHOST=\\"RC_Workstations\\" -DIFC \\')
            makefile.filter('-DCACHE_SIZE=.*', '-DCACHE_SIZE=12000 -DPGF90 \\')
            makefile.filter('-Duse_shmem.*', '-Duse_shmem -DnoAugXCmeta -DVASP2WANNIER90 -DRPROMU_DGEMV -DRACCMU_DGEMV -DnoSTOPCAR -Ddo_loops')
            makefile.filter('FCL        = .*', 'FCL        = %s -mkl=sequential -lstdc++' % spec['mpi'].mpifc)

        vdw_nl = FileFilter('src/vdw_nl.F')
        vdw_nl.filter('file=\'vdw_kernel.bindat\'', 'file=\'/opt/share/vasp/common/vdw_kernel.bindat\'')

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def check_install(self):

        shutil.copytree('/opt/share/vasp/common/tests/vasptest', 'vasptest')
        with working_dir('vasptest'):
            spack_tests = Executable('spack.tests.sh')
            spack_tests('--run')

    def install(self, spec, prefix):

        mkdirp(prefix.bin)
        install('bin/vasp_std', prefix.bin+'/vasp')
        install('bin/vasp_gam', prefix.bin+'/vasp-gamma')
        install('bin/vasp_ncl', prefix.bin+'/vasp-so')
