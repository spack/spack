# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyParsl(PythonPackage):
    """
    Simple data dependent workflows in Python
    """

    homepage = "https://github.com/Parsl/parsl"
    url      = "https://github.com/Parsl/parsl/archive/refs/tags/1.1.0.tar.gz"

    maintainers = ['hategan']

    version('1.1.0', sha256='6a623d3550329f028775950d23a2cafcb0f82b199f15940180410604aa5d102c')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-typeguard@2.10:', type=('run', 'test'))
    depends_on('py-pyzmq@17.1.2:', type=('run', 'test'))
    depends_on('py-typing-extensions', type=('run', 'test'))
    depends_on('py-dill', type=('run', 'test'))
    depends_on('py-tblib', type=('run', 'test'))
    depends_on('py-requests', type=('run', 'test'))
    depends_on('py-paramiko', type=('run', 'test'))
    depends_on('py-psutil@5.5.1:', type=('run', 'test'))
    depends_on('py-globus-sdk', type=('run', 'test'))
    depends_on('py-flake8', type='test')
    depends_on('py-ipyparallel', type='test')
    depends_on('py-pandas', type='test')
    depends_on('py-pytest@4.6:4.999', type='test')
    depends_on('py-pytest-cov', type='test')
    depends_on('py-pytest-xdist', type='test')
    depends_on('py-pytest-random-order', type='test')
    depends_on('py-coverage@4.5.4', type='test')
    depends_on('py-mock@1.0.0:', type='test')
    depends_on('py-nbsphinx', type='test')
    depends_on('py-sphinx-rtd-theme', type='test')
    depends_on('py-mypy@0.790', type='test')
    depends_on('py-pytest-xdist', type='test')
    depends_on('py-sphinx@3.4.1', type='test')
    depends_on('py-twine', type='test')
    depends_on('py-wheel', type='test')
