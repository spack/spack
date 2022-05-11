# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class PyHttpcore(PythonPackage):
    """The HTTP Core package provides a minimal low-level HTTP client,
    which does one thing only. Sending HTTP requests."""

    homepage = "https://github.com/encode/httpcore"
    pypi = "httpcore/httpcore-0.11.0.tar.gz"

    version('0.14.7', sha256='7503ec1c0f559066e7e39bc4003fd2ce023d01cf51793e3c173b864eb456ead1')
    version('0.11.0', sha256='35ffc735d746b83f8fc6d36f82600e56117b9e8adc65d0c0423264b6ebfef7bf')

    depends_on('python@3.6:',      type=('build', 'run'))
    depends_on('py-setuptools',    type='build')
    depends_on('py-sniffio@1.0:1', type=('build', 'run'))
    depends_on('py-h11@0.8:0.9',   type=('build', 'run'), when='@0.11.0')
    depends_on('py-h11@0.11:0.12', type=('build', 'run'), when='@0.14.7')
    depends_on('py-anyio@3.0:3',   type=('build', 'run'), when='@0.14.7')
    depends_on('py-certifi',       type=('build', 'run'), when='@0.14.7:')
