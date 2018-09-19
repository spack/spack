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


class PyQuast(PythonPackage):
    """Quality Assessment Tool for Genome Assemblies"""

    homepage = "http://cab.spbu.ru/software/quast"
    url      = "https://github.com/ablab/quast/archive/quast_4.6.1.tar.gz"

    version('4.6.3', '16d77acb2e0f6436b58d9df7b732fb76')
    version('4.6.1', '37ccd34e0040c17aa6f990353a92475c')
    version('4.6.0', 'c04d62c50ec4d9caa9d7388950b8d144')

    depends_on('boost@1.56.0')
    depends_on('perl@5.6.0:')
    depends_on('python@2.5:,3.3:')
    depends_on('py-setuptools',    type='build')
    depends_on('py-matplotlib',    type=('build', 'run'))
    depends_on('java',             type=('build', 'run'))
    depends_on('perl-time-hires',  type=('build', 'run'))
    depends_on('gnuplot',          type=('build', 'run'))
    depends_on('mummer',           type=('build', 'run'))
    depends_on('bedtools2',        type=('build', 'run'))
    depends_on('bwa',              type=('build', 'run'))
    depends_on('glimmer',          type=('build', 'run'))
