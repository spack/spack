# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPythonRapidjson(PythonPackage):
    """Python wrapper around rapidjson."""

    homepage = "https://github.com/python-rapidjson/python-rapidjson"
    url      = "https://files.pythonhosted.org/packages/41/3e/a150b4ed792b7962c8dad466856e2eda36275e9f547f67f9ae17e1b0a4af/python-rapidjson-0.9.1.tar.gz"

    version('0.9.1', sha256='ad80bd7e4bb15d9705227630037a433e2e2a7982b54b51de2ebabdd1611394a1')

    depends_on('py-readme-renderer@24.0', type=('build', 'run'))
    depends_on('py-twine@1.13.0', type=('build', 'run'))
    depends_on('py-simplejson@3.16.0', type=('build', 'run'))
    depends_on('py-ujson@1.35', type=('build', 'run'))
    depends_on('py-yajl@0.3.5', type=('build', 'run'))
