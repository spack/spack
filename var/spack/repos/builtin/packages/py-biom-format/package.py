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


class PyBiomFormat(PythonPackage):
    """The BIOM file format (canonically pronounced biome) is designed to be
       a general-use format for representing biological sample by observation
       contingency tables."""

    homepage = "https://pypi.python.org/pypi/biom-format/2.1.6"
    url      = "https://pypi.io/packages/source/b/biom-format/biom-format-2.1.6.tar.gz"

    version('2.1.6', '1dd4925b74c56e8ee864d5e1973068de')

    variant('h5py', default=True, description='For use with BIOM 2.0+ files')

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-cython', type='build')
    depends_on('py-h5py', type=('build', 'run'), when='+h5py')
    depends_on('py-click', type=('build', 'run'))
    depends_on('py-numpy@1.3.0:', type=('build', 'run'))
    depends_on('py-future@0.16.0:', type=('build', 'run'))
    depends_on('py-scipy@0.13.0:', type=('build', 'run'))
    depends_on('py-pandas@0.19.2:', type=('build', 'run'))
    depends_on('py-six@1.10.0:', type=('build', 'run'))
    depends_on('py-pyqi', type=('build', 'run'))
