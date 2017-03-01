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


class PyPbr(PythonPackage):
    """PBR is a library that injects some useful and sensible default
       behaviors into your setuptools run."""
    homepage = "https://pypi.python.org/pypi/pbr"
    url      = "https://pypi.io/packages/source/p/pbr/pbr-1.10.0.tar.gz"

    version('1.10.0', '8e4968c587268f030e38329feb9c8f17')
    version('1.8.1', 'c8f9285e1a4ca6f9654c529b158baa3a')

    depends_on('py-setuptools', type='build')
    # Only needed for py<3.4, however when='^python@:3.4.2' syntax might be
    # broken, if this fails, remove the when-clause
    depends_on('py-enum34', type='build', when='^python@:3.3')
