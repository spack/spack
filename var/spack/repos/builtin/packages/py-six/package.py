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


class PySix(PythonPackage):
    """Python 2 and 3 compatibility utilities."""

    homepage = "https://pypi.python.org/pypi/six"
    url      = "https://pypi.io/packages/source/s/six/six-1.11.0.tar.gz"

    import_modules = ['six']

    version('1.11.0', 'd12789f9baf7e9fb2524c0c64f1773f8')
    version('1.10.0', '34eed507548117b2ab523ab14b2f8b55')
    version('1.9.0',  '476881ef4012262dfc8adc645ee786c4')
    version('1.8.0',  '1626eb24cc889110c38f7e786ec69885')

    extends('python', ignore=r'bin/pytest')

    # Newer versions of setuptools require six. Although setuptools is an
    # optional dependency of six, if it is not found, setup.py will fallback
    # on distutils.core instead. Don't add a setuptools dependency or we
    # won't be able to bootstrap setuptools.

    # depends_on('py-setuptools', type='build')
