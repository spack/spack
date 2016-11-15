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


class PySncosmo(Package):
    """SNCosmo is a Python library for high-level supernova cosmology
    analysis."""

    homepage = "http://sncosmo.readthedocs.io/"
    url = "https://pypi.python.org/packages/source/s/sncosmo/sncosmo-1.2.0.tar.gz"

    version('1.2.0', '028e6d1dc84ab1c17d2f3b6378b2cb1e')

    # Required dependencies
    # py-sncosmo binaries are duplicates of those from py-astropy
    extends('python', ignore=r'bin/.*')
    depends_on('py-numpy', type=nolink)
    depends_on('py-scipy', type=nolink)
    depends_on('py-astropy', type=nolink)

    # Recommended dependencies
    depends_on('py-matplotlib', type=nolink)
    depends_on('py-iminuit', type=nolink)
    depends_on('py-emcee', type=nolink)
    depends_on('py-nestle', type=nolink)

    def install(self, spec, prefix):
        setup_py('install', '--prefix={0}'.format(prefix))
