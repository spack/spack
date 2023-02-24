# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPipTools(PythonPackage):
    """pip-tools keeps your pinned dependencies fresh."""

    homepage = "https://pip-tools.rtfd.io"
    pypi = "pip-tools/pip-tools-6.10.0.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    version('6.3.0', sha256='1835a1848bdfb22b2b6e5d10d630844ff5ee15e24b6c3bf92319c76f205d347f')

    depends_on('py-click@7:')
    depends_on('py-setuptools@45:', type='build')
    depends_on('py-setuptools-scm+toml@6.2:', type='build')
    depends_on('py-pip@20.3:')
    depends_on('py-build')
    depends_on('py-wheel')
