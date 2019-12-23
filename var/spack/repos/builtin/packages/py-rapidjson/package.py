# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

from os import symlink
from shutil import rmtree


class PyRapidjson(PythonPackage):
    """Python wrapper around rapidjson."""

    homepage = "https://github.com/python-rapidjson/python-rapidjson"
    url      = "https://github.com/python-rapidjson/python-rapidjson/archive/v0.9.1.tar.gz"

    version('0.9.1', sha256='5820f6dd3ca2a247269cce7bd3cae42edb078e925fff130e519bff9946c5cbcf')

    resource(
        name='rapidjson',
        git='https://github.com/Tencent/rapidjson.git',
        commit='7484e06c589873e1ed80382d262087e4fa80fb63',
        destination='rapidjsonsrc',
    )

    depends_on('py-readme-renderer@24.0', type=('build', 'run'))
    depends_on('py-twine@1.13.0', type=('build', 'run'))
    depends_on('py-simplejson@3.16.0', type=('build', 'run'))
    depends_on('py-ujson@1.35', type=('build', 'run'))
    depends_on('py-yajl@0.3.5', type=('build', 'run'))

    @run_before('build')
    def prep_rapidjson(self):
        rmtree('rapidjson')
        symlink('rapidjsonsrc/rapidjson', 'rapidjson')
