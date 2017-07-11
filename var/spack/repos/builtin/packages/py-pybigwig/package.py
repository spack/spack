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


class PyPybigwig(PythonPackage):
    """A package for accessing bigWig files using libBigWig."""

    homepage = "https://pypi.python.org/pypi/pyBigWig"
    url      = "https://pypi.python.org/packages/4d/7c/911e92392cf2d70d1a0da8fbb95be1e203f3cf9f858e030e98d4882c9ec7/pyBigWig-0.3.4.tar.gz#md5=8e0a91e26e87eeaa071408a3a749bfa9"

    version('0.3.4', '8e0a91e26e87eeaa071408a3a749bfa9')

    depends_on('py-setuptools', type='build')
    depends_on('curl', type='build')
