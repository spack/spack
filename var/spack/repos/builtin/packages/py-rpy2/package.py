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


class PyRpy2(PythonPackage):
    """rpy2 is a redesign and rewrite of rpy. It is providing a low-level
       interface to R from Python, a proposed high-level interface,
       including wrappers to graphical libraries, as well as R-like
       structures and functions.

    """
    homepage = "https://pypi.python.org/pypi/rpy2"
    url = "https://pypi.python.org/packages/source/r/rpy2/rpy2-2.5.4.tar.gz"

    version('2.5.4', '115a20ac30883f096da2bdfcab55196d')
    version('2.5.6', 'a36e758b633ce6aec6a5f450bfee980f')

    # FIXME: Missing dependencies:
    # ld: cannot find -licuuc
    # ld: cannot find -licui18

    depends_on('py-six', type=('build', 'run'))
    depends_on('py-setuptools', type='build')

    depends_on('r')
