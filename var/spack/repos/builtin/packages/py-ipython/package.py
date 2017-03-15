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


class PyIpython(PythonPackage):
    """IPython provides a rich toolkit to help you make the most out of using
       Python interactively."""
    homepage = "https://pypi.python.org/pypi/ipython"
    url      = "https://pypi.io/packages/source/i/ipython/ipython-2.3.1.tar.gz"

    version('5.1.0', '47c8122420f65b58784cb4b9b4af35e3')
    version('3.1.0', 'a749d90c16068687b0ec45a27e72ef8f')
    version('2.3.1', '2b7085525dac11190bfb45bb8ec8dcbf')

    depends_on('py-pygments', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))

    # These dependencies breaks concretization
    # See https://github.com/LLNL/spack/issues/2793
    # depends_on('py-backports-shutil-get-terminal-size', when="^python@:3.2.999")  # noqa
    # depends_on('py-pathlib2', when="^python@:3.3.999")
    depends_on('py-backports-shutil-get-terminal-size', type=('build', 'run'))
    depends_on('py-pathlib2', type=('build', 'run'))

    depends_on('py-pickleshare', type=('build', 'run'))
    depends_on('py-simplegeneric', type=('build', 'run'))
