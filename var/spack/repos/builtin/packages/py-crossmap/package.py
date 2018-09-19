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


class PyCrossmap(PythonPackage):
    """CrossMap is a program for convenient conversion of genome
       coordinates (or annotation files) between different assemblies"""

    homepage = "http://crossmap.sourceforge.net"
    url      = "https://downloads.sourceforge.net/project/crossmap/CrossMap-0.2.7.tar.gz"

    version('0.2.7', '91dadec9644ee3038f20ee7a6eb8dfb7')

    depends_on('python@2.7:2.7.999', type=('build', 'run'))
    depends_on('py-cython@0.17:', type='build')
    depends_on('py-pysam', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-bx-python', type=('build', 'run'))
