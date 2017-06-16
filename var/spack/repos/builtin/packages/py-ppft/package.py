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


class PyPpft(PythonPackage):
    """Distributed and parallel python """

    homepage = "https://github.com/uqfoundation/ppft"
    url      = "https://pypi.org/packages/source/p/ppft/ppft-1.6.4.7.1.zip"

    version('1.6.4.7.1',  '2b196a03bfbc102773f849c6b21e617b')
    version('1.6.4.6',   'e533432bfba4b5a523a07d58011df209')
    version('1.6.4.5',   'd2b1f9f07eae22b31bfe90f544dd3044')

    depends_on('python@2.5:2.8,3.1:')

    depends_on('py-setuptools@0.6:', type='build')
    depends_on('py-six@1.7.3:', type=('build', 'run'))
    depends_on('py-dill@0.2.6:', type=('build', 'run'))
