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
    """Keras is a high-level neural networks library, written in Python and 
    capable of running on top of either TensorFlow or Theano. It was developed
    with a focus on enabling fast experimentation. Being able to go from idea
    to result with the least possible delay is key to doing good research."""

    homepage = "http://keras.io"
    url      = "https://github.com/fchollet/keras/archive/1.2.2.tar.gz"

    version('1.2.2', 'ed044936528c9818e95bef4c57187725')
    version('1.2.1', 'd565724240f11913d70efb2d169c9708')
    version('1.2.0', '5739309012b7450b80519d8fcb9b499e')
    version('1.1.2', '5bbf8710be7e0ca5a5c3a1623111a164')
    version('1.1.1', '8e912a380bf563f88b7aefc0cf18f390')
    version('1.1.0', 'f554dff743ac331fb6c4b089b6f52799')
    version('1.0.8', '46f2b12322a62658e4ff5ddf6aef526f')
    version('1.0.7', 'fd9080b40654c43c8a986a22d35b792f')
    version('1.0.6', 'f48b1fd85d927d58a2d297325b9a844c')
    version('1.0.5', 'a13eecc0cdd031ad5e764c8649e5bb65')

    depends_on('python')
    depends_on('py-setuptools', type='build')
    depends_on('py-theano',     type=('build', 'run'))

    extends('python')
