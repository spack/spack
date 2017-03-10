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


class PyJpype(PythonPackage):
    """JPype is an effort to allow python programs full access to java class
    libraries."""

    homepage = "https://github.com/originell/jpype"
    url      = "https://pypi.io/packages/source/J/JPype1/JPype1-0.6.2.tar.gz"

    version('0.6.2', '16e5ee92b29563dcc63bbc75556810c1')
    version('0.6.1', '468ca2d4b2cff7802138789e951d5d58')
    version('0.6.0', 'f0cbbe1d0c4b563f7e435d2bffc31736')

    depends_on('python@2.6:')

    depends_on('py-setuptools', type='build')
    depends_on('jdk', type=('build', 'run'))
    # extra requirements
    # depends_on('py-numpy@1.6:', type=('build', 'run'))
