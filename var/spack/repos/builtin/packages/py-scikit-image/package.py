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

class PyScikitImage(Package):
    """Image processing algorithms for SciPy, including IO, morphology, filtering, warping, color manipulation, object detection, etc."""
    homepage = "http://scikit-image.org/"
    url      = "https://pypi.python.org/packages/source/s/scikit-image/scikit-image-0.12.3.tar.gz"

    version('0.12.3', '04ea833383e0b6ad5f65da21292c25e1')

    extends('python', ignore=r'bin/.*\.py$')

    depends_on('py-dask')
    depends_on('py-pillow')
    depends_on('py-networkx')
    depends_on('py-six')
    depends_on('py-scipy')
    depends_on('py-matplotlib')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
