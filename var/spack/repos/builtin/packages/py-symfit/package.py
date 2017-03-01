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


class PySymfit(PythonPackage):
    """Symbolic Fitting; fitting as it should be."""

    homepage = "http://symfit.readthedocs.org"
    url      = "https://pypi.io/packages/source/s/symfit/symfit-0.3.5.tar.gz"

    version('0.3.5', '7f62552ffeba4b4d203c01ff52fe15d5')

    depends_on('py-setuptools@17.1:', type='build')
    depends_on('py-pbr@1.9:',         type='build')
    depends_on('py-numpy',            type='run')
    depends_on('py-scipy',            type='run')
    depends_on('py-sympy',            type='run')
    depends_on('py-funcsigs',         type='run', when='^python@:2.7.999')
