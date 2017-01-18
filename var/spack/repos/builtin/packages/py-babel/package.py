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


class PyBabel(PythonPackage):
    """Babel is an integrated collection of utilities that assist in
    internationalizing and localizing Python applications, with an
    emphasis on web-based applications."""

    homepage = "http://babel.pocoo.org/en/latest/"
    url      = "https://pypi.python.org/packages/source/B/Babel/Babel-2.3.4.tar.gz"

    version('2.3.4', 'afa20bc55b0e991833030129ad498f35',
            url="https://pypi.python.org/packages/6e/96/ba2a2462ed25ca0e651fb7b66e7080f5315f91425a07ea5b34d7c870c114/Babel-2.3.4.tar.gz")

    depends_on('py-setuptools', type='build')
    depends_on('py-pytz',       type=('build', 'run'))
