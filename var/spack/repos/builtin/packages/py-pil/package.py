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


class PyPil(PythonPackage):
    """The Python Imaging Library (PIL) adds image processing capabilities
    to your Python interpreter. This library supports many file formats,
    and provides powerful image processing and graphics capabilities."""

    homepage = "http://www.pythonware.com/products/pil/"
    url      = "http://effbot.org/media/downloads/Imaging-1.1.7.tar.gz"

    version('1.1.7', 'fc14a54e1ce02a0225be8854bfba478e')

    provides('pil')

    # py-pil currently only works with Python2.
    # If you are using Python 3, try using py-pillow instead.
    depends_on('python@1.5.2:2.8')
