# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyZmq(PythonPackage):
    """PyZMQ: Python bindings for zeromq."""
    homepage = "https://github.com/zeromq/pyzmq"
    url      = "https://github.com/zeromq/pyzmq/archive/v14.7.0.tar.gz"

    version('17.1.2', 'b368115d2c5989dc45ec63a9da801df6')
    version('16.0.2', '4cf14a2995742253b2b009541f4436f4')
    version('14.7.0', 'bf304fb73d72aee314ff82d3554328c179938ecf')

    depends_on('py-cython@0.16:', type=('build', 'run'))
    depends_on('py-py', type=('build', 'run'))
    depends_on('py-cffi', type=('build', 'run'))
    depends_on('zeromq')
