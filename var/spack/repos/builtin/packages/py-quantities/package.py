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


class PyQuantities(PythonPackage):
    """Support for physical quantities with units, based on numpy"""

    homepage = "http://python-quantities.readthedocs.org"
    url      = "https://pypi.io/packages/source/q/quantities/quantities-0.12.1.tar.gz"

    version('0.12.1', '9c9ecda15e905cccfc420e5341199512')
    version('0.11.1', 'f4c6287bfd2e93322b25a7c1311a0243',
            url="https://pypi.io/packages/source/q/quantities/quantities-0.11.1.zip")

    conflicts('py-numpy@1.13:', when='@:0.11.99')

    depends_on('python@2.6.0:')
    depends_on('py-numpy@1.4.0:', type=('build', 'run'))
