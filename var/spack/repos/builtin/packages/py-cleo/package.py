# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class PyCleo(PythonPackage):
    """Cleo allows you to create beautiful and testable command-line interfaces."""

    homepage = "https://github.com/sdispater/cleo"
    pypi     = "cleo/cleo-0.8.1.tar.gz"

    version('0.8.1', sha256='3d0e22d30117851b45970b6c14aca4ab0b18b1b53c8af57bed13208147e4069f')

    depends_on('python@2.7,3.4:3', type=('build', 'run'))
    depends_on('py-poetry-core@1:', type='build')
    depends_on('py-clikit@0.6.0:0.6', type=('build', 'run'))
