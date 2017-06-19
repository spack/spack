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


class PyBleach(PythonPackage):
    """An easy whitelist-based HTML-sanitizing tool."""

    homepage = "http://github.com/mozilla/bleach"
    url      = "https://pypi.python.org/packages/99/00/25a8fce4de102bf6e3cc76bc4ea60685b2fee33bde1b34830c70cacc26a7/bleach-1.5.0.tar.gz"

    version('1.5.0', 'b663300efdf421b3b727b19d7be9c7e7')

    depends_on('python@2.6:2.7,3.2:3.5')
    depends_on('py-setuptools', type='build')
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-html5lib@0.999,0.999999:0.9999999', type=('build', 'run'))
