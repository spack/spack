# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class PyPythonRapidjson(PythonPackage):
    """Python wrapper around rapidjson."""

    homepage = "https://github.com/python-rapidjson/python-rapidjson"
    pypi = "python-rapidjson/python-rapidjson-0.9.1.tar.gz"

    version('1.5', sha256='04323e63cf57f7ed927fd9bcb1861ef5ecb0d4d7213f2755969d4a1ac3c2de6f')
    version('0.9.1', sha256='ad80bd7e4bb15d9705227630037a433e2e2a7982b54b51de2ebabdd1611394a1')

    depends_on('python@3.4:', type=('build', 'run'))
    depends_on('python@3.6:', type=('build', 'run'), when='@1.5:')
    depends_on('py-setuptools', type='build')
