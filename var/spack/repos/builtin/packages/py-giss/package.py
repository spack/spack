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


class PyGiss(Package):
    """Misc. Python Stuff."""

    homepage = "https://github.com/citibeth/pygiss"
    url      = "https://codeland.github.com/citibeth/pygiss/tar.gz/v0.1.0.tar.gz"

    version('0.1.2', '1c1c745c2818a6930c29c6ec7f835943')
    version('0.1.1', '172d468690a8b8f474884d7a60064bc7')
    version('develop', git='https://github.com/citibeth/pygiss.git', branch='develop')
    version('glint2', git='https://github.com/citibeth/pygiss.git', branch='glint2')

    maintainers = ['citibeth']

    # Requires python@3:
    extends('python')

    depends_on('python@3:')
    depends_on('py-numpy+blas+lapack')
    depends_on('py-netcdf')
    depends_on('py-matplotlib')
    depends_on('py-basemap')
    depends_on('py-proj')
    depends_on('py-scipy')
    depends_on('py-six')
    depends_on('py-udunits')

    def install(self, spec, prefix):
        setup_py('install', '--prefix=%s' % prefix)
