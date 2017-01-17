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


class PyCffi(PythonPackage):
    """Foreign Function Interface for Python calling C code"""
    homepage = "http://cffi.readthedocs.org/en/latest/"
    # base https://pypi.python.org/pypi/cffi
    url      = "https://pypi.python.org/packages/source/c/cffi/cffi-1.1.2.tar.gz"

    version('1.1.2', 'ca6e6c45b45caa87aee9adc7c796eaea')

    depends_on('py-setuptools', type='build')
    depends_on('py-pycparser', type=('build', 'run'))
    depends_on('libffi')

    def setup_environment(self, spack_env, run_env):
        # This sets the compiler (and flags) that distutils will use
        # to create the final shared library.  It will use the
        # compiler specified by the environment variable 'CC' for all
        # other compilation.  We are setting the 'LDSHARED" to the
        # spack compiler wrapper plus a few extra flags necessary for
        # building the shared library.
        spack_env.set('LDSHARED', "{0} -shared -pthread".format(spack_cc))
