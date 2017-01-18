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


class PyMarkupsafe(PythonPackage):
    """MarkupSafe is a library for Python that implements a unicode
    string that is aware of HTML escaping rules and can be used to
    implement automatic string escaping. It is used by Jinja 2, the
    Mako templating engine, the Pylons web framework and many more."""

    homepage = "http://www.pocoo.org/projects/markupsafe/"
    url      = "https://pypi.python.org/packages/source/M/MarkupSafe/MarkupSafe-0.23.tar.gz"

    version('0.23', 'f5ab3deee4c37cd6a922fb81e730da6e')
    version('0.22', 'cb3ec29fd5361add24cfd0c6e2953b3e')
    version('0.21', 'fde838d9337fa51744283f46a1db2e74')
    version('0.20', '7da066d9cb191a70aa85d0a3d43565d1')
    version('0.19', 'ccb3f746c807c5500850987006854a6d')

    depends_on('py-setuptools', type='build')
