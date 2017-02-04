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


class PyLit(PythonPackage):
    """lit is a portable tool for executing LLVM and Clang style test suites,
       summarizing their results, and providing indication of failures. lit is
       designed to be a lightweight testing tool with as simple a user
       interface as possible."""

    homepage = "https://pypi.python.org/pypi/lit"
    url      = "https://pypi.python.org/packages/5b/a0/dbed2c8dfb220eb9a5a893257223cd0ff791c0fbc34ce2f1a957fa4b6c6f/lit-0.5.0.tar.gz"

    version('0.5.0',  '8144660cc692be8fb903395a5f06564d')

    depends_on('py-setuptools', type='build')
