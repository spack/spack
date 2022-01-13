# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTomli(Package):
    """Tomli is a Python library for parsing TOML.

    Tomli is fully compatible with TOML v1.0.0."""

    homepage = "https://github.com/hukkin/tomli"
    url = "https://pypi.io/packages/py3/t/tomli/tomli-1.2.1-py3-none-any.whl"

    version('1.2.1', sha256='8dd0e9524d6f386271a36b41dbf6c57d8e32fd96fd22b6584679dc569d20899f', expand=False)

    extends('python')
    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-pip', type='build')

    def install(self, spec, prefix):
        # TODO: figure out how to build with flit
        pip = which('pip')
        pip('install', self.stage.archive_file, '--prefix={0}'.format(prefix))
