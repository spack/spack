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


class PyTheano(PythonPackage):
    """Optimizing compiler for evaluating mathematical expressions on CPUs
    and GPUs."""

    homepage = "http://deeplearning.net/software/theano/"
    url      = "https://pypi.io/packages/source/T/Theano/Theano-0.8.2.tar.gz"
    git      = "https://github.com/Theano/Theano.git"

    version('master', branch='master')
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
