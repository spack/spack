##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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


class PyPy2bit(PythonPackage):
    """A package for accessing 2bit files using lib2bit."""

    homepage = "https://pypi.python.org/pypi/py2bit"
    url      = "https://pypi.python.org/packages/b2/ad/72d0d1cf2a588d9d2b16f5e531063aa33d1c80bf424e810fc1dfe5c5dc72/py2bit-0.2.1.tar.gz#md5=eaf5b1c80a0bbf0b35af1f002f83a556"

    version('0.2.1', 'eaf5b1c80a0bbf0b35af1f002f83a556')

    depends_on('py-setuptools', type='build')
