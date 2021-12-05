# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFlit(PythonPackage):
    """Flit is a simple way to put Python packages and modules on PyPI."""

    pypi = "flit/flit-3.3.0.tar.gz"
    maintainers = ['takluyver']

    version('3.3.0', sha256='65fbe22aaa7f880b776b20814bd80b0afbf91d1f95b17235b608aa256325ce57')

    depends_on('py-flit-core@3.3.0:', type=('build', 'run'))
    depends_on('py-requests', type=('build', 'run'))
    depends_on('py-docutils', type=('build', 'run'))
    depends_on('py-toml', type=('build', 'run'))
