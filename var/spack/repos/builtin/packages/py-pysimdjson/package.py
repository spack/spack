# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPysimdjson(PythonPackage):
    """Python bindings for the simdjson project, a SIMD-accelerated
    JSON parser. If SIMD instructions are unavailable a fallback parser
    is used, making pysimdjson safe to use anywhere."""

    homepage = "http://github.com/TkTech/pysimdjson"
    pypi     = "pysimdjson/pysimdjson-4.0.3.tar.gz"

    maintainers = ['haralmha']

    version('4.0.3', sha256='61900992d7f992b073a8c5f93cafa4af9bfd3209624baa775699b0fdd6f67517')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
