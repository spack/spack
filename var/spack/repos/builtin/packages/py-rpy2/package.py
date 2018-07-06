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


class PyRpy2(PythonPackage):
    """rpy2 is a redesign and rewrite of rpy. It is providing a low-level
       interface to R from Python, a proposed high-level interface,
       including wrappers to graphical libraries, as well as R-like
       structures and functions.

    """
    homepage = "https://pypi.python.org/pypi/rpy2"
    url = "https://pypi.io/packages/source/r/rpy2/rpy2-2.5.4.tar.gz"

    version('2.9.4', '7df2562cdf43a0ccdd1e44ee1c16614f')
    version('2.8.6', '85046aa58ba586622f67271fbca05933')
    version('2.5.6', 'a36e758b633ce6aec6a5f450bfee980f')
    version('2.5.4', '115a20ac30883f096da2bdfcab55196d')

    # FIXME: Missing dependencies:
    # ld: cannot find -licuuc
    # ld: cannot find -licui18

    # All versions
    depends_on('py-setuptools', type='build')
    depends_on('r',             type=('build', 'run'))

    # @2.9.0:
    depends_on('r@3.3:',    when='@2.9.0:', type=('build', 'run'))
    depends_on('python@3:', when='@2.9.0:', type=('build', 'run'))
    depends_on('py-jinja2', when='@2.9.0:', type=('build', 'run'))
    depends_on('py-six',    when='@2.9.0:', type=('build', 'run'))

    # @:2.8.6
    depends_on('r@2.8:', when='@:2.8.6', type=('build', 'run'))
    depends_on('py-singledispatch', when='^python@:2',   type=('build', 'run'))
