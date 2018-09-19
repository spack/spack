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


class PyPybtexDocutils(PythonPackage):
    """A docutils backend for pybtex."""

    homepage = "https://pypi.python.org/pypi/pybtex-docutils/"
    url      = "https://pypi.io/packages/source/p/pybtex-docutils/pybtex-docutils-0.2.1.tar.gz"

    import_modules = ['pybtex_docutils']

    version('0.2.1', '7ae4b00562bd8881f582edf95009cc62')

    depends_on('py-setuptools', type='build')
    depends_on('py-docutils@0.8:', type=('build', 'run'))
    depends_on('py-pybtex@0.16:', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
