##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
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


class PyEfel(PythonPackage):
    """The Electrophys Feature Extract Library (eFEL) allows 
    neuroscientists to automatically extract features from time series data 
    recorded from neurons (both in vitro and in silico).
    Examples are the action potential width and amplitude in 
    voltage traces recorded during whole-cell patch clamp experiments.
    The user of the library provides a set of traces and selects the 
    features to be calculated. The library will then extract the requested 
    features and return the values to the user."""
    homepage = "https://github.com/BlueBrain/eFEL"
    url = "https://pypi.io/packages/source/e/efel/efel-3.0.22.tar.gz"

    version('3.0.22', sha256='97b2c1a0425b12cd419e8539bb1e936ce64c4e93f5d0dd7f81f38554490064a2')
    
    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type='run')
    depends_on('py-six', type='run')
