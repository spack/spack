##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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
from spack import *
import os


class Pfunit(Package):
    """Regridding/Coupling library for GCM + Ice Sheet Model"""

    homepage = "http://pfunit.sourceforge.net/index.html"
    url = "http://downloads.sourceforge.net/project/pfunit/Source/pFUnit-3.2.7.tar.gz"

    version('3.2.7', '7e994e031c679ed0b446be8b853d5e69')

    # Shared library support.
    version('3.2.7-citibeth', git='git://git.code.sf.net/u/citibeth2/pfunit',
        branch='3.2.7-citibeth')

    depends_on('mpi', when='+mpi')
    depends_on('openmp', when='+openmp')

    depends_on('cmake', type='build')
    depends_on('doxygen', type='build')

    variant('shared', default=True,
        description='Build shared library in addition to static')
    variant('mpi', default=True,
        description='Test MPI-based programs')
    variant('openmp', default=False,
        description='Test OpenMP-based programs')

    def install(self, spec, prefix):

        if '+openmp' in spec:
            raise ValueError(
                'pfUnit works with OpenMP-based programs,\n' +
                'but there is currently no openmp package in Spack.\n' +
                'If you would like to use pfUnit with OpenMP, please\n'+
                'add an OpenMP package and remove this message from\n'+
                'the pfunit package.')

        with working_dir('spack-build', create=True):
            options = std_cmake_args + [
                '-DBUILD_SHARED=%s' % ('YES' if '+shared' in spec else 'NO'),
                '-DMPI=%s' % ('YES' if '+mpi' in spec else 'NO'),
                '-OPENMP=%s' % ('YES' if '+openmp' in spec else 'NO'),
                '-DINSTALL_PATH=%s' % prefix]
            cmake(self.stage.source_path, *options)
#            make('tests')
            make()
            make('install', 'INSTALL_DIR=%s' % prefix)

    def setup_dependent_package(self, module, dspec):
        self.spec.pfunit_prefix = self.prefix

    def setup_environment(self, spack_env, env):
        super(Pfunit, self).setup_environment(spack_env,env)
        env.prepend_path('CPATH', join_path(self.prefix, 'mod'))
        #env.prepend_path('PFUNIT', self.prefix)
