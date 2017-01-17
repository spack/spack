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


class PyLogilabCommon(PythonPackage):
    """Common modules used by Logilab projects"""
    homepage = "https://www.logilab.org/project/logilab-common"
    url      = "https://pypi.python.org/packages/a7/31/1650d23e44794d46935d82b86e73454cc83b814cbe1365260ccce8a2f4c6/logilab-common-1.2.0.tar.gz"

    version('1.2.0', 'f7b51351b7bfe052746fa04c03253c0b')

    extends('python', ignore=r'bin/pytest')
    depends_on("py-setuptools", type='build')
    depends_on("py-six", type=('build', 'run'))
