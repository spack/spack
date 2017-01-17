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


class PyRestview(PythonPackage):
    """A viewer for ReStructuredText documents that renders them on the fly."""

    homepage = "https://mg.pov.lt/restview/"
    url = "https://pypi.python.org/packages/source/r/restview/restview-2.6.1.tar.gz"

    version('2.6.1', 'ac8b70e15b8f1732d1733d674813666b')

    depends_on('python@2.7.0:2.7.999,3.3:3.5')
    depends_on('py-docutils@0.13.1:', type=('build', 'run'))
    depends_on('py-readme-renderer', type=('build', 'run'))
    depends_on('py-pygments', type=('build', 'run'))
