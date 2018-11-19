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


class PyIpyparallel(PythonPackage):
    """Use multiple instances of IPython in parallel, interactively."""

    homepage = "http://ipython.org"
    url = "https://pypi.io/packages/source/i/ipyparallel/ipyparallel-6.2.2.tar.gz"

    version('6.2.2', sha256='02b225966d5c20f12b1fba0b6b10aa5d352a6b492e075f137ff0ff6e95b9358e')

    depends_on('py-setuptools', type='build')
    depends_on('py-tornado', type='run')
    depends_on('py-traitlets', type='run')
    depends_on('py-zmq', type='run')
    depends_on('py-ipython', type='run')
    depends_on('py-ipykernel', type='run')
    depends_on('py-futures', type='run', when='^python@2.7.0:2.7.999')
