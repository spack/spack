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


class PyBsddb3(Package):

    """"py-bsddb3" are the Python "bindings" for the excellent Oracle
    Berkeley DB. They are included in stardard Python version 2.3 thru
    2.7, but here you will find a vastly updated version. Python 3.x
    doesn't include native Berkeley DB support, you need to install
    this library by your own.
    """

    homepage = "https://www.jcea.es/programacion/pybsddb.htm"
    version('6.2.1', '17cdf893a9bf09ef50773d2a35715a0e',
        url='https://pypi.python.org/packages/95/1c/e8fb33007192f30b9a7276560c3c16499ab2a2c08abc59141b84e1afd3a9/bsddb3-6.1.1.tar.gz')

    extends('python')
    depends_on('python@3:')
    # depends_on('berkeleydb')    # Not yet in Spack, usually on systems

    def install(self, spec, prefix):
        setup_py('install', '--prefix={0}'.format(prefix))

    # For testing... see here for an example that uses BerkeleyDB
    # http://code.activestate.com/recipes/189060-using-berkeley-db-database/
