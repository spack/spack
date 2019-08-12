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

    version('1.4.1', '0ff84b6c79d0dafb7e2971629c4d127a')

    depends_on('py-setuptools',  type='build')
    depends_on('py-setuptools-scm',  type='build')
    depends_on('py-apipkg@1.4:', type=('build', 'run'))
