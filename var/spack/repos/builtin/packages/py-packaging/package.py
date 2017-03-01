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


class PyPackaging(PythonPackage):
    """Core utilities for Python packages."""

    homepage = "https://github.com/pypa/packaging"
    url      = "https://pypi.io/packages/source/p/packaging/packaging-16.8.tar.gz"

    version('16.8', '53895cdca04ecff80b54128e475b5d3b')

    # Not needed for the installation, but used at runtime
    depends_on('py-six',       type='run')
    depends_on('py-pyparsing', type='run')

    # Newer versions of setuptools require packaging. Although setuptools is an
    # optional dependency of packaging, if it is not found, setup.py will
    # fallback on distutils.core instead. Don't add a setuptools dependency
    # or we won't be able to bootstrap setuptools.

    # depends_on('py-setuptools', type='build')
