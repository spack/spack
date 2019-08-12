# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMxnet(PythonPackage):
    """Python binding for DMLC/MXNet."""

    homepage = "http://mxnet.io"
    url      = "https://github.com/sjtuhpcc/python-mxnet/archive/0.10.0.post2.tar.gz"

    version('0.10.0.post2', '64a646fbf5d1b53ce1008da1bf94d77c',
            url='https://github.com/sjtuhpcc/python-mxnet/archive/0.10.0.post2.tar.gz')

    # TODO
    # install_time_test_callbacks = ['install_test', 'import_module_test']

    # import_modules = ['mxnet', 'mxnet.module', 'mxnet._ctypes', 'mxnet.rnn',
    #      		'mxnet._cy2', 'mxnet._cy3', 'mxnet.notebook', 'mxnet.contrib']

    variant('cuda', default=False, description='Enable CUDA support')

    depends_on('python@2.6:2.8,3.3:')

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-numpy@1.7.1:', type=('build', 'run'))
    # depends_on('py-pip', type='build')

    depends_on('mxnet', type=('build', 'run'))
    depends_on('mxnet+cuda', when='+cuda', type=('build', 'run'))

    def patch(self):
        spec = self.spec
        filter_file('../../../',
                    spec['mxnet'].prefix.lib,
                    'mxnet/libinfo.py', string=True)
