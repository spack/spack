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


class PyOpenpmdValidator(PythonPackage):
    """Validator and Example Scripts for the openPMD markup.

    openPMD is an open standard for particle-mesh data files."""

    homepage = "http://www.openPMD.org"
    url      = "https://github.com/openPMD/openPMD-validator/archive/1.0.0.2.tar.gz"
    maintainers = ['ax3l']

    version('1.0.0.2', '2b71b786288c1e7a2134bd6818ad1999')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy@1.6.1:', type=('build', 'run'))
    depends_on('py-dateutil@2.3.0:', type=('build', 'run'))
    depends_on('py-h5py@2.0.0:', type=('build', 'run'))
