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


class PyVirtualenv(PythonPackage):
    """virtualenv is a tool to create isolated Python environments."""

    homepage = "https://virtualenv.pypa.io/"
    url      = "https://pypi.io/packages/source/v/virtualenv/virtualenv-15.1.0.tar.gz"

    version('15.1.0', '44e19f4134906fe2d75124427dc9b716')
    version('15.0.1', '28d76a0d9cbd5dc42046dd14e76a6ecc')
    version('13.0.1', '1ffc011bde6667f0e37ecd976f4934db')
    version('1.11.6', 'f61cdd983d2c4e6aeabb70b1060d6f49')

    depends_on('python@2.6:')

    # not just build-time, requires pkg_resources
    depends_on('py-setuptools', type=('build', 'run'))
