##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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


class Metasv(PythonPackage):
    """An accurate and integrative structural-variant caller
       for next generation sequencing"""

    homepage = "http://bioinform.github.io/metasv/"
    url      = "https://github.com/bioinform/metasv/archive/0.5.4.tar.gz"

    version('0.5.4', 'de2e21ac4f86bc4d1830bdfff95d8391')

    depends_on('py-pybedtools@0.6.9', type=('build', 'run'))
    depends_on('py-pysam@0.7.7', type=('build', 'run'))
    depends_on('py-pyvcf@0.6.7', type=('build', 'run'))
