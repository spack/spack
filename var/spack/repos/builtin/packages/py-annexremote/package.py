# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAnnexremote(PythonPackage):
    """git annex special remotes made easy."""

    homepage = "https://github.com/Lykos153/AnnexRemote"
    pypi     = "annexremote/annexremote-1.5.0.tar.gz"

    version('1.5.0', sha256='92f32b6f5461cbaeefe0c60b32f9c1e0c1dbe4e57b8ee425affb56f4060f64ef')

    depends_on('py-setuptools', type='build')
    depends_on('py-future', type=('build', 'run'))
