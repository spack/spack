# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTheano(PythonPackage):
    """Optimizing compiler for evaluating mathematical expressions on CPUs
    and GPUs."""

    homepage = "http://deeplearning.net/software/theano/"
    url      = "https://pypi.io/packages/source/T/Theano/Theano-0.8.2.tar.gz"
    git      = "https://github.com/Theano/Theano.git"

    version('master', branch='master')
    version('1.0.4', sha256='35c9bbef56b61ffa299265a42a4e8f8cb5a07b2997dabaef0f8830b397086913')
    version('1.0.2', 'fcae24dfa76babe15f5f3c556d67c9f2')
    version('1.0.1', 'a38b36c0fdc3126c574163db0a253e69')
    version('0.8.2', 'f2d0dfe7df141115201077cd933b2c52')

    variant('gpu', default=False,
            description='Builds with support for GPUs via CUDA and cuDNN')

    depends_on('python@2.6:2.8,3.3:')

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-scipy@0.11:', type=('build', 'run'))
    depends_on('py-numpy@1.7.1:', type=('build', 'run'))
    depends_on('py-six@1.9.0:', type=('build', 'run'))

    depends_on('blas')

    depends_on('cuda', when='+gpu')
    depends_on('cudnn', when='+gpu')
    depends_on('py-pygpu', when='+gpu', type=('build', 'run'))
    depends_on('libgpuarray', when='+gpu')

    depends_on('py-nose@1.3.0:', type='test')
    depends_on('py-nose-parameterized@0.5.0:', type='test')
