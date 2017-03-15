##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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


class PyScientificpython(PythonPackage):
    """ScientificPython is a collection of Python modules for
       scientific computing. It contains support for geometry,
       mathematical functions, statistics, physical units, IO,
       visualization, and parallelization."""

    homepage = "https://sourcesup.renater.fr/projects/scientific-py/"
    url      = "https://sourcesup.renater.fr/frs/download.php/file/4411/ScientificPython-2.8.1.tar.gz"
    version('2.8.1', '73ee0df19c7b58cdf2954261f0763c77')

    depends_on('py-numpy')
