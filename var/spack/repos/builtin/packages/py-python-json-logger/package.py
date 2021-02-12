# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPythonJsonLogger(PythonPackage):
    """"A python library adding a json log formatter."""

    homepage = "https://github.com/madzak/python-json-logger"
    pypi = "python-json-logger/python-json-logger-0.1.11.tar.gz"

    version('2.0.1', sha256='f26eea7898db40609563bed0a7ca11af12e2a79858632706d835a0f961b7d398')
    version('2.0.0', sha256='6c15023a8571200228472d4c9de7cb891cd45f670061f7729b8209bf643d5bbf')
    version('0.1.11', sha256='b7a31162f2a01965a5efb94453ce69230ed208468b0bbc7fdfc56e6d8df2e281')

    depends_on('python@2.7:', type=('build', 'run'))
    depends_on('py-setuptools')
