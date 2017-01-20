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


class PyPytestFlake8(PythonPackage):
    """pytest plugin to check FLAKE8 requirements."""

    homepage = "https://github.com/tholo/pytest-flake8"

    version('0.8.1', '39b64ebceb2849805975a2ff4ea7e947',
            url="https://pypi.python.org/packages/75/b8/7380f4d81cdd5edac344f5699b3f7846b6f56581820fc7d0d673b1d067ac/pytest-flake8-0.8.1.tar.gz")

    depends_on('py-setuptools', type='build')

    # Install requires:
    depends_on('py-flake8@3.0:', type=('build', 'run'))
    depends_on('py-pytest@2.8:', type=('build', 'run'))
