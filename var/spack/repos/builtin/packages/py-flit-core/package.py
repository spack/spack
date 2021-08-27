# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFlitCore(Package):
    """Distribution-building parts of Flit."""

    homepage = "https://github.com/takluyver/flit"
    url = "https://pypi.io/packages/py3/f/flit-core/flit_core-3.3.0-py3-none-any.whl"

    version('3.3.0', sha256='9b247b3095cb3c43933a59a7433f92ddfdd7fc843e08ef0f4550d53a9cfbbef6', expand=False)

    extends('python')
    depends_on('python@3.4:', type=('build', 'run'))
    depends_on('py-pip', type='build')
    depends_on('py-toml', type=('build', 'run'))

    def install(self, spec, prefix):
        # Install wheel instead of installing from source
        # to prevent circular dependency on flit
        pip = which('pip')
        pip('install', self.stage.archive_file, '--prefix={0}'.format(prefix))
