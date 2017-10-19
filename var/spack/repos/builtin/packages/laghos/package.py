##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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

from spack import *


class Laghos(Package):
    """CEED miniapp that solves the time-dependent Euler equations using
       MFEM"""

    homepage = "https://github.com/CEED/Laghos"
    url      = "https://github.com/CEED/Laghos/archive/v1.0.tar.gz"

    version('1.0',
            'f58c6089e69ed11d111d63d2629c0e2616219e1d474ff2aee14529953d3e8bb0')

    depends_on('mfem@3.3:+mpi')

    def install(self, spec, prefix):

        options = [
            'MFEM_DIR=%s' % spec['mfem'].prefix,
            'CONFIG_MK=%s' % join_path(spec['mfem'].prefix, 'config.mk'),
            'TEST_MK=%s' % join_path(spec['mfem'].prefix, 'test.mk'),
        ]

        install_options = ['PREFIX=%s' % prefix]

        make(*options)
        make('install', *install_options)
