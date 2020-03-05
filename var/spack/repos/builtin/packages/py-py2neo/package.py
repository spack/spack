# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPy2neo(PythonPackage):
    """Py2neo is a client library and toolkit for working with Neo4j from
    within Python applications and from the command line."""

    homepage = "http://py2neo.org/"
    # url      = "https://github.com/nigelsmall/py2neo/archive/py2neo-2.0.8.tar.gz"
    url      = "https://pypi.io/packages/source/p/py2neo/py2neo-2.0.8.tar.gz"

    version('2.0.8', sha256='06167f5a91a0d9b9b73431baacd876f2d507650a681fdce1fcf3b383a9b991c1')
    version('2.0.7', sha256='9b154053eb93c7f5fb3ebd48b6a5b99df450d3f2e9c6682153c6f8d59369378c')
    version('2.0.6', sha256='6bb828d6d3e48b4d095b3f7d79dbb690a47633f0a9812eb62f141b042bab3186')
    version('2.0.5', sha256='2c04d4223d2d356c4800c586f30c048757334f9391553c852c29aebf2368d101')
    version('2.0.4', sha256='727726b87268ca1e929191b960a5473409e5bd81559ee83a304951104bb6b866')

    depends_on("py-setuptools", type='build')
