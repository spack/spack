##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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
from distutils.dir_util import copy_tree


class PyMxnet(PythonPackage):
    """Python binding for DMLC/MXNet."""

    homepage = "http://mxnet.io"
    url      = "https://github.com/apache/incubator-mxnet/archive/0.10.0.post2.tar.gz"

    version('0.10.0.post2', '7819d511cf4a6efad681e6662fa966e4',
            url='https://github.com/apache/incubator-mxnet/archive/0.10.0.post2.tar.gz')
    version('0.10.0.post1',  '16d540f407cd22285555b3ab22040032',
            url='https://github.com/apache/incubator-mxnet/archive/v0.10.0.post1.tar.gz')
    version('0.10.0', '2d0c83c33eda729932d620cca3078826',
            url='https://github.com/apache/incubator-mxnet/archive/v0.10.0.tar.gz')

    # TODO
    # install_time_test_callbacks = ['install_test', 'import_module_test']

    # import_modules = ['mxnet', 'mxnet.module', 'mxnet._ctypes', 'mxnet.rnn',
    #      		'mxnet._cy2', 'mxnet._cy3', 'mxnet.notebook', 'mxnet.contrib']

    depends_on('py-setuptools', type='build')
    depends_on('py-pip', type='build')
    depends_on('py-numpy+blas+lapack', type='run')
    depends_on('mxnet', type=('build', 'run'))

    build_directory = 'python'

    def build(self, spec, prefix):
        # py-mxnet doesn't need build
        pass

    def install(self, spec, prefix):
        with working_dir('python'):
            filter_file('../../../',
                        spec['mxnet'].prefix.lib,
                        'mxnet/libinfo.py', string=True)
            pip = which('pip')
            pip('install', '-e', '.')
