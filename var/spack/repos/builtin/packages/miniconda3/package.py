# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from os.path import split


class Miniconda3(Package):
    """The minimalist bootstrap toolset for conda and Python3."""

    homepage = "https://conda.io/miniconda.html"
    url      = "https://repo.continuum.io/miniconda/Miniconda3-4.6.14-Linux-x86_64.sh"

    version('4.6.14', sha256='0d6b23895a91294a4924bd685a3a1f48e35a17970a073cd2f684ffe2c31fc4be', expand=False)
    version('4.5.11', sha256='ea4594241e13a2671c5b158b3b813f0794fe58d514795fbf72a1aad24db918cf', expand=False)
    version('4.5.4', 'a946ea1d0c4a642ddf0c3a26a18bb16d', expand=False)
    version('4.3.30', '0b80a152332a4ce5250f3c09589c7a81', expand=False)
    version('4.3.14', 'fc6fc37479e3e3fcf3f9ba52cae98991', expand=False)
    version('4.3.11', '1924c8d9ec0abf09005aa03425e9ab1a', expand=False)

    def install(self, spec, prefix):
        # peel the name of the script out of the pathname of the
        # downloaded file
        dir, script = split(self.stage.archive_file)
        bash = which('bash')
        bash(script, '-b', '-f', '-p', self.prefix)
