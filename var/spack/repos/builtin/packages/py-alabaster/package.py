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


class PyAlabaster(PythonPackage):
    """Alabaster is a visually (c)lean, responsive, configurable theme
    for the Sphinx documentation system."""

    homepage = "https://pypi.python.org/pypi/alabaster"
    url      = "https://pypi.python.org/packages/source/a/alabaster/alabaster-0.7.9.tar.gz"

    version('0.7.9', 'b29646a8bbe7aa52830375b7d17b5d7a',
            url="https://pypi.python.org/packages/71/c3/70da7d8ac18a4f4c502887bd2549e05745fa403e2cd9d06a8a9910a762bc/alabaster-0.7.9.tar.gz")

    depends_on('py-setuptools', type='build')
