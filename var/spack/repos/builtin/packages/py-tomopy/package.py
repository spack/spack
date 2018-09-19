##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
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


class PyTomopy(PythonPackage):
    """TomoPy is an open-source Python package for tomographic data
       processing and image reconstruction."""

    homepage = "http://tomopy.readthedocs.io/en/latest/index.html"
    url      = "https://github.com/tomopy/tomopy/archive/1.0.0.tar.gz"

    import_modules = [
        'tomopy', 'doc', 'tomopy.util', 'tomopy.sim', 'tomopy.recon',
        'tomopy.prep', 'tomopy.misc', 'tomopy.io', 'doc.demo'
    ]

    version('1.0.0', '986ac2c85a4af9ada0403b4c746d2cd4')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-h5py', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-scikit-image', type=('build', 'run'))
    depends_on('py-pywavelets', type=('build', 'run'))
    depends_on('py-pyfftw', type=('build', 'run'))
    depends_on('py-dxchange', type=('build', 'run'))
