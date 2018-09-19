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


class PyGoatools(PythonPackage):
    """Python scripts to find enrichment of GO terms"""

    homepage = "https://github.com/tanghaibao/goatools"
    url      = "https://pypi.io/packages/source/g/goatools/goatools-0.7.11.tar.gz"

    version('0.7.11', 'f2ab989ec9c4acdd80504b263c3b3188')

    depends_on('py-nose',        type=('build', 'run'))
    depends_on('py-numpy',       type=('build', 'run'))
    depends_on('py-pandas',      type=('build', 'run'))
    depends_on('py-pydot',       type=('build', 'run'))
    depends_on('py-pyparsing',   type=('build', 'run'))
    depends_on('py-pytest',      type=('build', 'run'))
    depends_on('py-scipy',       type=('build', 'run'))
    depends_on('py-statsmodels', type=('build', 'run'))
    depends_on('py-xlrd',        type=('build', 'run'))
    depends_on('py-xlsxwriter',  type=('build', 'run'))
