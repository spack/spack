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


class PySymengine(PythonPackage):
    """Python wrappers for SymEngine, a symbolic manipulation library."""

    homepage = "https://github.com/symengine/symengine.py"
    url = "https://github.com/symengine/symengine.py/archive/v0.2.0.tar.gz"

    version('0.2.0', 'e1d114fa12be4c8c7e9f24007e07718c')
    version('develop', git='https://github.com/symengine/symengine.py.git')

    # Build dependencies
    depends_on('python@2.7:2.8,3.3:')
    depends_on('py-setuptools',     type='build')
    depends_on('py-cython@0.19.1:', type='build')
    depends_on('cmake@2.8.7:',      type='build')
    depends_on('symengine@0.2.0:')

    def build_args(self, spec, prefix):
        return ['--symengine-dir={0}'.format(spec['symengine'].prefix)]
