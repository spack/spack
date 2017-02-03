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


class PyPycurl(PythonPackage):
    """PycURL is a Python interface to libcurl. PycURL can be used to fetch
    objects identified by a URL from a Python program."""

    homepage = "http://pycurl.io/"
    url      = "https://pypi.python.org/packages/source/p/pycurl/pycurl-7.43.0.tar.gz"

    version('7.43.0', 'c94bdba01da6004fa38325e9bd6b9760')

    depends_on('python@2.6:')
    depends_on('py-setuptools', type='build')
    depends_on('curl@7.19.0:')
