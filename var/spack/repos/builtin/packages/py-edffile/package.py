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


class PyEdffile(PythonPackage):
    """Generic class for Edf files manipulation."""

    homepage = "https://github.com/vasole/pymca/blob/master/PyMca5/PyMcaIO/EdfFile.py"
    git      = "https://github.com/conda-forge/edffile-feedstock.git"

    import_modules = ['EdfFile']

    version('5.0.0', commit='be5ab4199db9f8209c59e31874934b8536b52301')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))

    build_directory = 'recipe/src'
