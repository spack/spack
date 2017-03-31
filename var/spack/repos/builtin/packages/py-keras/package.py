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


class PyKeras(PythonPackage):
    """Deep Learning library for Python. Convnets, recurrent neural networks,
    and more. Runs on Theano or TensorFlow."""

    homepage = "http://keras.io"
    url      = "https://pypi.io/packages/source/K/Keras/Keras-1.2.2.tar.gz"

    version('1.2.2', '8e26b25bf16494f6eca726887d232319')
    version('1.2.1', '95525b9faa890267d80d119b13ce2984')
    version('1.2.0', 'd24d8b72747f8cc38e659ce8fc92ad3c')
    version('1.1.2', '53027097f240735f873119ee2e8d27ff')
    version('1.1.1', '4bd8b75e8c6948ec0498cc603bbc6590')
    version('1.1.0', 'd1711362ac8473238b0d198d2e3a0574')

    depends_on('py-setuptools', type='build')
    depends_on('py-theano', type=('build', 'run'))
    depends_on('py-pyyaml', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
