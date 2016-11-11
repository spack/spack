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


class PyAstropy(Package):
    """The Astropy Project is a community effort to develop a single core
    package for Astronomy in Python and foster interoperability between
    Python astronomy packages."""

    homepage = 'http://www.astropy.org/'
    url = 'https://pypi.python.org/packages/source/a/astropy/astropy-1.1.2.tar.gz'

    version('1.1.2',     'cbe32023b5b1177d1e2498a0d00cda51')
    version('1.1.post1', 'b52919f657a37d45cc45f5cb0f58c44d')

    # Required dependencies
    extends('python')
    depends_on('py-numpy', type=nolink)

    # Optional dependencies
    depends_on('py-h5py', type=nolink)
    depends_on('py-beautifulsoup4', type=nolink)
    depends_on('py-pyyaml', type=nolink)
    depends_on('py-scipy', type=nolink)
    depends_on('libxml2')
    depends_on('py-matplotlib', type=nolink)
    depends_on('py-pytz', type=nolink)
    depends_on('py-scikit-image', type=nolink)
    depends_on('py-pandas', type=nolink)

    # System dependencies
    depends_on('cfitsio')
    depends_on('expat')

    def install(self, spec, prefix):
        setup_py('build', '--use-system-cfitsio', '--use-system-expat')
        setup_py('install', '--prefix={0}'.format(prefix))
