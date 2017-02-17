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


class Xsdktrilinos(CMakePackage):
    """xSDKTrilinos contains the portions of Trilinos that depend on PETSc
    because they would cause a circular dependency if built as part of
    Trilinos.
    """
    homepage = "https://trilinos.org/"
    base_url = "https://github.com/trilinos/xSDKTrilinos/archive"

    version('develop', git='https://github.com/trilinos/xSDKTrilinos.git', tag='master')
    version('xsdk-0.2.0', git='https://github.com/trilinos/xSDKTrilinos.git', tag='master')
    version('12.8.1', '9cc338ded17d1e10ea6c0dc18b22dcd4')
    version('12.6.4', '44c4c54ccbac73bb8939f68797b9454a')

    def url_for_version(self, version):
        return '%s/trilinos-release-%s.tar.gz' % \
            (Xsdktrilinos.base_url, version.dashed)

    variant('hypre',        default=True,
            description='Compile with Hypre preconditioner')
    variant('petsc',        default=True,
            description='Compile with PETSc solvers')
    variant('shared',       default=True,
            description='Enables the build of shared libraries')
    variant('debug',        default=False,
            description='Builds a debug version of the libraries')

    # MPI related dependencies
    depends_on('mpi')
    depends_on('hypre@xsdk-0.2.0~internal-superlu', when='@xsdk-0.2.0+hypre')
    depends_on('hypre@develop~internal-superlu', when='@develop+hypre')    
    depends_on('petsc@xsdk-0.2.0+mpi~complex', when='@xsdk-0.2.0+petsc')
    depends_on('petsc@develop+mpi~complex', when='@develop+petsc')    
    depends_on('trilinos@12.6.4', when='@12.6.4')
    depends_on('trilinos@12.8.1', when='@12.8.1')
    depends_on('trilinos@xsdk-0.2.0', when='@xsdk-0.2.0')
    depends_on('trilinos@develop', when='@develop')    

    def cmake_args(self):
        spec = self.spec

        options = []

        mpi_bin = spec['mpi'].prefix.bin
        options.extend([
            '-DxSDKTrilinos_VERBOSE_CONFIGURE:BOOL=OFF',
            '-DxSDKTrilinos_ENABLE_TESTS:BOOL=ON',
            '-DxSDKTrilinos_ENABLE_EXAMPLES:BOOL=ON',
            '-DTrilinos_INSTALL_DIR=%s' % spec['trilinos'].prefix,
            '-DCMAKE_BUILD_TYPE:STRING=%s' % (
                'DEBUG' if '+debug' in spec else 'RELEASE'),
            '-DBUILD_SHARED_LIBS:BOOL=%s' % (
                'ON' if '+shared' in spec else 'OFF'),
            '-DTPL_ENABLE_MPI:BOOL=ON',
            '-DMPI_BASE_DIR:PATH=%s' % spec['mpi'].prefix,
            '-DxSDKTrilinos_ENABLE_CXX11:BOOL=ON',
            '-DTPL_ENABLE_HYPRE:BOOL=%s' % (
                'ON' if '+hypre' in spec else 'OFF'),
            '-DTPL_ENABLE_PETSC:BOOL=%s' % (
                'ON' if '+petsc' in spec else 'OFF'),
            '-DCMAKE_INSTALL_NAME_DIR:PATH=%s/lib' % self.prefix
        ])

        # Fortran lib
        if spec.satisfies('%gcc') or spec.satisfies('%clang'):
            libgfortran = os.path.dirname(os.popen(
                '%s --print-file-name libgfortran.a' %
                join_path(mpi_bin, 'mpif90')).read())
            options.extend([
                '-DxSDKTrilinos_EXTRA_LINK_FLAGS:STRING=-L%s/ -lgfortran' % (
                    libgfortran),
                '-DxSDKTrilinos_ENABLE_Fortran=ON'
            ])

        return options
