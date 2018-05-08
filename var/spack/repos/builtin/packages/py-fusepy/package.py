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


class PyFusepy(PythonPackage):
    """Fusepy is a Python module that provides a simple interface to FUSE and
    MacFUSE. It's just one file and is implemented using ctypes.

    The original version of fusepy was hosted on Google Code, but is now 
    officially hosted on GitHub.

    fusepy is written in 2x syntax, but trying to pay attention to bytes and other
    changes 3x would care about."""

    homepage = "https://github.com/fusepy/fusepy"
    url      = "https://github.com/fusepy/fusepy/archive/v2.0.4.tar.gz"

    version('2.0.4', '0b0bf1283d6fe9532ecbf6c8204f05d3')

    depends_on('py-setuptools', type='build')

