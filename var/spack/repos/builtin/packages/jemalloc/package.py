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


class Jemalloc(Package):
    """jemalloc is a general purpose malloc(3) implementation that emphasizes
       fragmentation avoidance and scalable concurrency support."""
    homepage = "http://www.canonware.com/jemalloc/"
    url      = "https://github.com/jemalloc/jemalloc/releases/download/4.0.4/jemalloc-4.0.4.tar.bz2"

    version('4.5.0', 'a5624318fbf5bf653697306642683a11')
    version('4.4.0', '81b59778e19696d99e2f7922820671b0')
    version('4.3.1', 'f204c0ea1aef92fbb339dc640de338a6')
    version('4.2.1', '094b0a7b8c77c464d0dc8f0643fd3901')
    version('4.2.0', 'e6b5d5a1ea93a04207528d274efdd144')
    version('4.1.0', 'c4e53c947905a533d5899e5cc3da1f94')
    version('4.0.4', '687c5cc53b9a7ab711ccd680351ff988')

    variant('stats', default=False, description='Enable heap statistics')
    variant('prof', default=False, description='Enable heap profiling')

    def install(self, spec, prefix):
        configure_args = ['--prefix=%s' % prefix, ]

        if '+stats' in spec:
            configure_args.append('--enable-stats')
        if '+prof' in spec:
            configure_args.append('--enable-prof')

        configure(*configure_args)

        # Don't use -Werror
        filter_file(r'-Werror=\S*', '', 'Makefile')

        make()
        make("install")
