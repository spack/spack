# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class PyDataladMetalad(PythonPackage):
    """DataLad extension for semantic metadata handling"""

    homepage = "https://github.com/datalad/datalad-metalad/"
    pypi     = "datalad_metalad/datalad_metalad-0.2.1.tar.gz"

    version('0.2.1', sha256='70fe423136a168f7630b3e0ff1951e776d61e7d5f36670bddf24299ac0870285')

    depends_on('py-setuptools',      type=('build'))
    depends_on('py-datalad@0.12.3:', type=('build', 'run'))
    depends_on('git-annex',          type=('run'))
