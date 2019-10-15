# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyExecnet(PythonPackage):
    """execnet provides a share-nothing model with channel-send/receive
    communication for distributing execution across many Python interpreters
    across version, platform and network barriers."""

    homepage = "http://codespeak.net/execnet"
    url      = "https://pypi.io/packages/source/e/execnet/execnet-1.4.1.tar.gz"

    version('1.4.1', sha256='f66dd4a7519725a1b7e14ad9ae7d3df8e09b2da88062386e08e941cafc0ef3e6')

    depends_on('py-setuptools',  type='build')
    depends_on('py-setuptools-scm',  type='build')
    depends_on('py-apipkg@1.4:', type=('build', 'run'))
