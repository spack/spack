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


class PyAppdirs(PythonPackage):
    """A small Python module for determining appropriate platform-specific
    dirs, e.g. a "user data dir"."""

    homepage = "https://github.com/ActiveState/appdirs"
    url      = "https://pypi.io/packages/source/a/appdirs/appdirs-1.4.0.tar.gz"

    version('1.4.0', '1d17b4c9694ab84794e228f28dc3275b')

    patch('setuptools-import.patch', when='@:1.4.0')

    # Newer versions of setuptools require appdirs. Although setuptools is an
    # optional dependency of appdirs, if it is not found, setup.py will
    # fallback on distutils.core instead. Don't add a setuptools dependency
    # or we won't be able to bootstrap setuptools.

    # depends_on('py-setuptools', type='build')
