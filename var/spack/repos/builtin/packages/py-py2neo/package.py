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


class PyPy2neo(PythonPackage):
    """Py2neo is a client library and toolkit for working with Neo4j from
    within Python applications and from the command line."""

    homepage = "http://py2neo.org/"
    url      = "https://github.com/nigelsmall/py2neo/archive/py2neo-2.0.8.tar.gz"

    version('2.0.8', 'e3ec5172a9e006515ef4155688a05a55')
    version('2.0.7', '4cfbc5b7dfd7757f3d2e324805faa639')
    version('2.0.6', '53e4cdb1a95fbae501c66e541d5f4929')
    version('2.0.5', '143b1f9c0aa22faf170c1b9f84c7343b')
    version('2.0.4', 'b3f7efd3344dc3f66db4eda11e5899f7')

    depends_on("py-setuptools", type='build')
