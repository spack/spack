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


class PyPyparsing(PythonPackage):
    """A Python Parsing Module."""
    homepage = "https://pypi.python.org/pypi/pyparsing"
    url      = "https://pypi.io/packages/source/p/pyparsing/pyparsing-2.0.3.tar.gz"

    version('2.1.10', '065908b92904e0d3634eb156f44cc80e')
    version('2.0.3',  '0fe479be09fc2cf005f753d3acc35939')

    patch('setuptools-import.patch', when='@:2.1.10')

    # Newer versions of setuptools require pyparsing. Although setuptools is an
    # optional dependency of pyparsing, if it is not found, setup.py will
    # fallback on distutils.core instead. Don't add a setuptools dependency
    # or we won't be able to bootstrap setuptools.

    # depends_on('py-setuptools', type='build')
