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


class PyXopen(PythonPackage):
    """This small Python module provides a xopen function that works like the
    built-in open function, but can also deal with compressed files. Supported
    compression formats are gzip, bzip2 and xz. They are automatically
    recognized by their file extensions .gz, .bz2 or .xz."""

    homepage = "https://github.com/marcelm/xopen"
    url      = "https://pypi.io/packages/source/x/xopen/xopen-0.1.1.tar.gz"

    version('0.1.1', '4e0e955546ee6bee4ea736b54623a671')

    depends_on('py-setuptools', type='build')
    depends_on('python@2.6:', type=('build', 'run'))
