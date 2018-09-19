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


class PyPysam(PythonPackage):
    """A python module for reading, manipulating and writing genomic data
       sets."""

    homepage = "https://pypi.python.org/pypi/pysam"
    url      = "https://github.com/pysam-developers/pysam/archive/v0.14.1.tar.gz"

    version('0.14.1', 'ad88fa5bbcc0fdf4a936734691d9c9d1')
    version('0.13', 'a9b502dd1a7e6403e35e6972211688a2')
    version('0.11.2.2', '56230cd5f55b503845915b76c22d620a')
    version('0.7.7', 'eaf9f37cbccc5e2708754d045909c1a0')

    depends_on('py-setuptools', type='build')
    depends_on('py-cython@0.21:', type='build')
    depends_on('curl')
    depends_on('bcftools')
    depends_on('htslib')
    depends_on('samtools')

    depends_on('htslib@:1.6', when='@:0.13')
