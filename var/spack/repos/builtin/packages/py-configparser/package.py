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


class PyConfigparser(PythonPackage):
    """This library brings the updated configparser from Python 3.5 to
    Python 2.6-3.5."""

    homepage = "https://docs.python.org/3/library/configparser.html"
    url      = "https://pypi.io/packages/source/c/configparser/configparser-3.5.0.tar.gz"

    version('3.5.0', 'cfdd915a5b7a6c09917a64a573140538')

    depends_on('py-setuptools', type='build')

    # This dependency breaks concretization
    # See https://github.com/spack/spack/issues/2793
    # depends_on('py-ordereddict', when='^python@:2.6', type=('build', 'run'))
