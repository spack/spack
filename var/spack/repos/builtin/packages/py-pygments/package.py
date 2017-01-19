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


class PyPygments(PythonPackage):
    """Pygments is a syntax highlighting package written in Python."""

    homepage = "https://pypi.python.org/pypi/pygments"
    url      = "https://pypi.python.org/packages/source/P/Pygments/Pygments-2.0.1.tar.gz"

    version('2.1.3', 'ed3fba2467c8afcda4d317e4ef2c6150')
    version('2.0.1', 'e0daf4c14a4fe5b630da765904de4d6c')
    version('2.0.2', '238587a1370d62405edabd0794b3ec4a')

    depends_on('py-setuptools', type='build')
