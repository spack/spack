##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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


class PyGevent(PythonPackage):
    """gevent is a coroutine-based Python networking library."""

    homepage = "http://www.gevent.org"
    url      = "https://pypi.io/packages/source/g/gevent/gevent-1.3a2.tar.gz"

    version('1.3a2', '8d73a7b0ceb0ca791b22e6f7b7061e9e')

    depends_on('py-setuptools@24.2:',   type='build')
    depends_on('py-cython@0.27:',       type='build')
    depends_on('py-cffi@1.4.0:',        type=('build', 'run'))
    depends_on('py-greenlet@0.4.13:',   type=('build', 'run'))
    depends_on('python@2.7:2.8,3.4:',   type=('build', 'run'))
