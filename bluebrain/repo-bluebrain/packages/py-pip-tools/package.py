# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPipTools(PythonPackage):
    """pip-tools keeps your pinned dependencies fresh."""

    homepage = "https://pip-tools.rtfd.io"
    pypi = "pip-tools/pip-tools-6.11.0.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    version('6.11.0', sha256='90c5dc150e3856e4463b81ccc99307ccf9554e5db8393eb273705cb0b8f71c60')

    depends_on('py-setuptools@45:', type='build')
    depends_on('py-setuptools-scm+toml@6.2:', type='build')
