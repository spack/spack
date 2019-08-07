# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from os.path import split


class Miniconda2(Package):
    """The minimalist bootstrap toolset for conda and Python2."""

    homepage = "https://conda.io/miniconda.html"
    url      = "https://repo.continuum.io/miniconda/Miniconda2-4.6.14-Linux-x86_64.sh"

    version('4.6.14', sha256='3e20425afa1a2a4c45ee30bd168b90ca30a3fdf8598b61cb68432886aadc6f4d', expand=False)
    version('4.5.11', sha256='0e23e8d0a1a14445f78960a66b363b464b889ee3b0e3f275b7ffb836df1cb0c6', expand=False)
    version('4.5.4', '8a1c02f6941d8778f8afad7328265cf5', expand=False)
    version('4.3.30', 'bd1655b4b313f7b2a1f2e15b7b925d03', expand=False)
    version('4.3.14', '8cb075cf5462480980ef2373ad9fad38', expand=False)
    version('4.3.11', 'd573980fe3b5cdf80485add2466463f5', expand=False)

    def install(self, spec, prefix):
        # peel the name of the script out of the pathname of the
        # downloaded file
        dir, script = split(self.stage.archive_file)
        bash = which('bash')
        bash(script, '-b', '-f', '-p', self.prefix)
