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


class PyDeeptools(PythonPackage):
    """deepTools addresses the challenge of handling the large amounts of data
       that are now routinely generated from DNA sequencing centers."""

    homepage = "https://pypi.io/packages/source/d/deepTools"
    url      = "https://pypi.io/packages/source/d/deepTools/deepTools-2.5.2.tar.gz"

    version('2.5.2', 'ba8a44c128c6bb1ed4ebdb20bf9ae9c2')

    depends_on('python@2.7:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-numpy@1.9.0:', type=('build', 'run'))
    depends_on('py-scipy@0.17.0:', type=('build', 'run'))
    depends_on('py-py2bit@0.2.0:', type=('build', 'run'))
    depends_on('py-pybigwig@0.2.1:', type=('build', 'run'))
    depends_on('py-pysam@0.8.2:', type=('build', 'run'))
    depends_on('py-matplotlib@1.4.0:', type=('build', 'run'))
    depends_on('py-numpydoc@0.5:', type=('build', 'run'))
