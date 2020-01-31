# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyZmq(PythonPackage):
    """PyZMQ: Python bindings for zeromq."""
    homepage = "https://github.com/zeromq/pyzmq"
    url      = "https://github.com/zeromq/pyzmq/archive/v14.7.0.tar.gz"

    version('17.1.2', sha256='77a32350440e321466b1748e6063b34a8a73768b62cb674e7d799fbc654b7c45')
    version('16.0.2', sha256='717dd902c3cf432b1c68e7b299ad028b0de0d0a823858e440b81d5f1baa2b1c1')
    version('14.7.0', sha256='809a5fcc720d286c840f7f64696e60322b5b2544795a73db626f09b344d16a15')

    depends_on('py-cython@0.16:', type=('build', 'run'))
    depends_on('py-py', type=('build', 'run'))
    depends_on('py-cffi', type=('build', 'run'))
    depends_on('zeromq')
