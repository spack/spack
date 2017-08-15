##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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


class PyMisopy(PythonPackage):
    """MISO (Mixture of Isoforms) is a probabilistic framework that
       quantitates the expression level of alternatively spliced genes from
       RNA-Seq data, and identifies differentially regulated isoforms or exons
       across samples."""

    homepage = "http://miso.readthedocs.io/en/fastmiso/"
    url      = "http://pypi.python.org/packages/source/m/misopy/misopy-0.5.4.tar.gz"

    # checksum and url are not correct due to download link above not working
    version('0.5.4', 'fe0c9c2613304defbdead12ea99e4194')

    depends_on('py-setuptools', type='build')
    depends_on('python@2.6:', type=('build', 'run'))
    depends_on('py-numpy@1.6:', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-pysam', type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('samtools')
    depends_on('bedtools2')
