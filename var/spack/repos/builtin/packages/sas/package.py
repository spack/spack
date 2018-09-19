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


class Sas(CMakePackage):
    """SAS (Static Analysis Suite) is a powerful tool for running static
    analysis on C++ code."""

    homepage = "https://github.com/dpiparo/SAS"
    url      = "https://github.com/dpiparo/SAS/archive/0.1.3.tar.gz"

    version('0.2.0', 'e6fecfb71d9cdce342c8593f4728c9f0')
    version('0.1.4', '20d7311258f2a59c9367ae1576c392b6')
    version('0.1.3', '1e6572afcc03318d16d7321d40eec0fd')

    depends_on('python@2.7:')
    depends_on('llvm@3.5:')
    depends_on('cmake@2.8:', type='build')

    def cmake_args(self):
        args = [
            '-DLLVM_DEV_DIR=%s' % self.spec['llvm'].prefix
        ]
        return args
