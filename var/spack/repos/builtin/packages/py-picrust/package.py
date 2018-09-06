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


class PyPicrust(PythonPackage):
    """bioinformatics software package designed to predict metagenome
        functional content from marker gene surveys and full genomes."""

    homepage = "http://picrust.github.io/picrust/index.html"
    url      = "https://github.com/picrust/picrust/releases/download/v1.1.3/picrust-1.1.3.tar.gz"

    version('1.1.3', sha256='7538c8544899b8855deb73a2d7a4ccac4808ff294e161530a8c8762d472d8906')

    depends_on('python@2.7:2.999', type=('build', 'run'))
    depends_on('py-cogent@1.5.3', type=('build', 'run'))
    depends_on('py-biom-format@2.1.4:2.1.999', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-future@0.16.0', type=('build', 'run'))
    depends_on('py-numpy@1.5.1:', type=('build', 'run'))
