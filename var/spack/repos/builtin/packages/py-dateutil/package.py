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


class PyDateutil(PythonPackage):
    """Extensions to the standard Python datetime module."""
    homepage = "https://pypi.python.org/pypi/dateutil"
    url      = "https://pypi.python.org/packages/source/p/python-dateutil/python-dateutil-2.4.0.tar.gz"

    version('2.4.0', '75714163bb96bedd07685cdb2071b8bc')
    version('2.4.2', '4ef68e1c485b09e9f034e10473e5add2')
    version('2.5.2', 'eafe168e8f404bf384514f5116eedbb6')

    depends_on('py-setuptools', type='build')
    depends_on('py-six', type=('build', 'run'))
