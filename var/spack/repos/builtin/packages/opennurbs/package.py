##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
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
import glob


class Opennurbs(Package):
    """OpenNURBS is an open-source NURBS-based geometric modeling library
    and toolset, with meshing and display / output functions.
    """

    homepage = "https://github.com/OpenNURBS/OpenNURBS"
    git      = "https://github.com/OpenNURBS/OpenNURBS.git"

    maintainers = ['jrood-nrel']

    version('develop', branch='develop')

    version('percept', '59163fd085a24c7a4c2170c70bb60fea',
            url='https://github.com/PerceptTools/percept/raw/master/build-cmake/opennurbs-percept.tar.gz')

    variant('shared', default=True,
            description="Build shared libraries")

    # CMake installation method
    def install(self, spec, prefix):
        cmake_args = [
            '-DBUILD_SHARED_LIBS:BOOL=%s' % (
                'ON' if '+shared' in spec else 'OFF')
        ]

        cmake_args.extend(std_cmake_args)

        with working_dir('spack-build', create=True):
            cmake('..', *cmake_args)
            make()
            make('install')

    # Pre-cmake installation method
    @when('@percept')
    def install(self, spec, prefix):
        make(parallel=False)

        # Install manually
        mkdir(prefix.lib)
        mkdir(prefix.include)
        install('libopenNURBS.a', prefix.lib)
        install_tree('zlib', join_path(prefix.include, 'zlib'))
        headers = glob.glob(join_path('.', '*.h'))
        for h in headers:
            install(h, prefix.include)
