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


class PyMako(PythonPackage):
    """A super-fast templating language that borrows the best
       ideas from the existing templating languages."""

    homepage = "https://pypi.python.org/pypi/mako"
    url = "https://pypi.python.org/packages/source/M/Mako/Mako-1.0.1.tar.gz"

    version('1.0.4', 'c5fc31a323dd4990683d2f2da02d4e20')
    version('1.0.1', '9f0aafd177b039ef67b90ea350497a54')

    depends_on('py-setuptools', type='build')
    # depends_on('py-mock',   type='test')  # TODO: Add test deptype
    # depends_on('py-pytest', type='test')  # TODO: Add test deptype
    depends_on('py-markupsafe@0.9.2:', type=('build', 'run'))
