# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class PyRequestsUnixsocket(PythonPackage):
    """Use requests to talk HTTP via a UNIX domain socket."""

    homepage = "https://github.com/msabramo/requests-unixsocket"
    pypi     = "requests-unixsocket/requests-unixsocket-0.2.0.tar.gz"

    version('0.2.0', sha256='9e5c1a20afc3cf786197ae59c79bcdb0e7565f218f27df5f891307ee8817c1ea')

    depends_on('py-setuptools', type='build')
    depends_on('py-pbr', type='build')
    depends_on('py-requests@1.1:', type=('build', 'run'))
    depends_on('py-urllib3@1.8:', type=('build', 'run'))
