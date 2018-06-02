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


class PyCrispresso(PythonPackage):
    """Software pipeline for the analysis of CRISPR-Cas9 genome editing
    outcomes from deep sequencing data."""

    homepage = "https://github.com/lucapinello/CRISPResso"
    url      = "https://pypi.io/packages/source/C/CRISPResso/CRISPResso-1.0.8.tar.gz"

    version('1.0.8', '2f9b52fe62cf49012a9525845f4aea45')

    depends_on('py-setuptools', type='build')
    depends_on('python@2.7.0:2.7.999', type=('build', 'run'))
    depends_on('py-biopython@1.6.5:', type=('build', 'run'))
    depends_on('py-matplotlib@1.3.1:', type=('build', 'run'))
    depends_on('py-numpy@1.9:', type=('build', 'run'))
    depends_on('py-pandas@0.15:', type=('build', 'run'))
    depends_on('py-seaborn@0.7.1:', type=('build', 'run'))
    depends_on('emboss@6:', type=('build', 'run'))
    depends_on('flash', type=('build', 'run'))
    depends_on('java', type=('build', 'run'))
