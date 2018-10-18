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


class PySparkmanager(PythonPackage):
    """Small shim to manage Spark in a more convenient way"""

    homepage = "https://github.com/matz-e/sparkmanager"
    url      = "https://pypi.org/packages/source/s/sparkmanager/sparkmanager-0.6.0.tar.gz"

    version('0.7.0', sha256='5858728b8c91597970293c26b2f114161a435527a5600f9a7386f4e6d28ec7d9')
    version('0.6.0', sha256='98aa542942690b533f087fab1b5544abe189c4f4ee3e16b65f12f5758671db54')

    depends_on('py-setuptools', type='build')
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-pyspark', type=('build', 'run'))
    depends_on('spark', type='run')
