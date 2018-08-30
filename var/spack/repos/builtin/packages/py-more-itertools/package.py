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


class PyMoreItertools(PythonPackage):
    """Additions to the standard Python itertools package."""

    homepage = "https://github.com/erikrose/more-itertools"
    url      = "https://pypi.io/packages/source/m/more-itertools/more-itertools-4.3.0.tar.gz"

    import_modules = ['more_itertools', 'more_itertools.tests']

    version('4.3.0', '42157ef9b677bdf6d3609ed6eadcbd4a')
    version('4.1.0', '246f46686d95879fbad37855c115dc52')
    version('2.2',   'b8d328a33f966bf40bb829bcf8da35ce')

    depends_on('py-setuptools', type='build')
    depends_on('py-six@1.0.0:1.999', type=('build', 'run'))
