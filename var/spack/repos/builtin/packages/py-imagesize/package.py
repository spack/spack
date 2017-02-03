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


class PyImagesize(PythonPackage):
    """Parses image file headers and returns image size. Supports PNG, JPEG,
    JPEG2000, and GIF image file formats."""

    homepage = "https://pypi.python.org/pypi/imagesize"
    url      = "https://pypi.python.org/packages/source/i/imagesize/imagesize-0.7.1.tar.gz"

    version('0.7.1', '976148283286a6ba5f69b0f81aef8052',
            url="https://pypi.python.org/packages/53/72/6c6f1e787d9cab2cc733cf042f125abec07209a58308831c9f292504e826/imagesize-0.7.1.tar.gz")

    depends_on('py-setuptools', type='build')
