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
import sys


class Parmetis(Package):
    """ParMETIS is an MPI-based parallel library that implements a variety of
       algorithms for partitioning unstructured graphs, meshes, and for
       computing fill-reducing orderings of sparse matrices."""

    homepage = 'http://glaros.dtc.umn.edu/gkhome/metis/parmetis/overview'
    base_url = 'http://glaros.dtc.umn.edu/gkhome/fetch/sw/parmetis'

    version('4.0.3', 'f69c479586bf6bb7aff6a9bc0c739628')
    version('4.0.2', '0912a953da5bb9b5e5e10542298ffdce')

    variant('shared', default=True, description='Enables the build of shared libraries.')
    variant('debug', default=False, description='Builds the library in debug mode.')
    variant('gdb', default=False, description='Enables gdb support.')

    depends_on('cmake@2.8:', type='build')
    depends_on('mpi')
    depends_on('metis@5:')

    patch('enable_external_metis.patch')
    # bug fixes from PETSc developers
    # https://bitbucket.org/petsc/pkg-parmetis/commits/1c1a9fd0f408dc4d42c57f5c3ee6ace411eb222b/raw/  # NOQA: E501
    patch('pkg-parmetis-1c1a9fd0f408dc4d42c57f5c3ee6ace411eb222b.patch')
    # https://bitbucket.org/petsc/pkg-parmetis/commits/82409d68aa1d6cbc70740d0f35024aae17f7d5cb/raw/  # NOQA: E501
    patch('pkg-parmetis-82409d68aa1d6cbc70740d0f35024aae17f7d5cb.patch')

    def url_for_version(self, version):
        verdir = 'OLD/' if version < Version('3.2.0') else ''
        return '%s/%sparmetis-%s.tar.gz' % (Parmetis.base_url, verdir, version)

    def install(self, spec, prefix):
        source_directory = self.stage.source_path
        build_directory = join_path(source_directory, 'build')

        options = std_cmake_args[:]
        options.extend([
            '-DGKLIB_PATH:PATH=%s/GKlib' % spec['metis'].prefix.include,
            '-DMETIS_PATH:PATH=%s' % spec['metis'].prefix,
            '-DCMAKE_C_COMPILER:STRING=%s' % spec['mpi'].mpicc,
            '-DCMAKE_CXX_COMPILER:STRING=%s' % spec['mpi'].mpicxx
        ])

        if '+shared' in spec:
            options.append('-DSHARED:BOOL=ON')
        else:
            # Remove all RPATH options 
            # (RPATHxxx options somehow trigger cmake to link dynamically)
            rpath_options = []
            for o in options:
                if o.find('RPATH') >= 0:
                    rpath_options.append(o)
            for o in rpath_options:
                options.remove(o)

        if '+debug' in spec:
            options.extend(['-DDEBUG:BOOL=ON',
                            '-DCMAKE_BUILD_TYPE:STRING=Debug'])
        if '+gdb' in spec:
            options.append('-DGDB:BOOL=ON')

        with working_dir(build_directory, create=True):
            cmake(source_directory, *options)
            make()
            make('install')

            # The shared library is not installed correctly on Darwin; fix this
            if (sys.platform == 'darwin') and ('+shared' in spec):
                fix_darwin_install_name(prefix.lib)
