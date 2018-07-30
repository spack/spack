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


class PyAttrs(PythonPackage):
    """Classes Without Boilerplate"""

    homepage = "http://attrs.org/"
    url      = "https://pypi.io/packages/source/a/attrs/attrs-18.1.0.tar.gz"

    import_modules = ['attr']

    version('18.1.0', '3f3f3e0750dab74cfa1dc8b0fd7a5f86')
    version('16.3.0', '4ec003c49360853cf935113d1ae56151')

    depends_on('py-setuptools', type='build')

    depends_on('py-coverage', type='test')
    depends_on('py-hypothesis', type='test')
    depends_on('py-pympler', type='test')
    depends_on('py-pytest', type='test')
    depends_on('py-six', type='test')
    depends_on('py-zope-interface', type='test')
