##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
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
from spack import *


class Boost(Package):
    """Fake boost package."""

    homepage = "http://www.boost.org"
    url      = "http://downloads.sourceforge.net/project/boost/boost/1.63.0/boost_1_63_0.tar.bz2"

    version('1.63.0', '1c837ecd990bb022d07e7aab32b09847')

    default_install_libs = set(['atomic',
                                'chrono',
                                'date_time',
                                'filesystem',
                                'graph',
                                'iostreams',
                                'locale',
                                'log',
                                'math',
                                'program_options',
                                'random',
                                'regex',
                                'serialization',
                                'signals',
                                'system',
                                'test',
                                'thread',
                                'timer',
                                'wave'])

    # mpi/python are not installed by default because they pull in many
    # dependencies and/or because there is a great deal of customization
    # possible (and it would be difficult to choose sensible defaults)
    default_noinstall_libs = set(['mpi', 'python'])

    all_libs = default_install_libs | default_noinstall_libs

    for lib in all_libs:
        variant(lib, default=(lib not in default_noinstall_libs),
                description="Compile with {0} library".format(lib))

    variant('debug', default=False,
            description='Switch to the debug version of Boost')
    variant('shared', default=True,
            description="Additionally build shared libraries")
    variant('multithreaded', default=True,
            description="Build multi-threaded versions of libraries")
    variant('singlethreaded', default=False,
            description="Build single-threaded versions of libraries")
    variant('icu', default=False,
            description="Build with Unicode and ICU suport")
    variant('graph', default=False,
            description="Build the Boost Graph library")
    variant('taggedlayout', default=False,
            description="Augment library names with build options")

    def install(self, spec, prefix):
        pass
