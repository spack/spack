# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyJsonLogger(PythonPackage):
    """simple json switch for logging"""
    pypi     = "json_logger/json_logger-0.0.1.tar.gz"

    version('0.0.1', sha256='132b7db97fa2b3bff50c6056b9d31f7c70df0f5523f01f45f9ed53f48229fcfe')

    depends_on('py-setuptools', type=('build'))
    depends_on('python@2.7:', type=('build', 'run'))
