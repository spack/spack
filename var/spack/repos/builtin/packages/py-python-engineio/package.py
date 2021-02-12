# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPythonEngineio(PythonPackage):
    """Engine.IO is the implementation of transport-based
    cross-browser/cross-device bi-directional communication
    layer for Socket.IO."""

    homepage = "http://python-engineio.readthedocs.io/en/latest/"
    url      = "https://github.com/miguelgrinberg/python-engineio/archive/v2.0.2.tar.gz"

    version('4.0.0',  sha256='f5ea4ad31030b5539a572e14c90f3eefaa3b4778654995ba1bf8b2da260ccfa4')
    version('3.14.2', sha256='6764678026fb45f62fd9cb03eb6ca3840b47905dc9eccf3fdde64596508b82d5')
    version('3.14.1', sha256='98419a1d4465baf104e5f69de8c480565cd2451cbb639d71218968b3ebcf8ed9')
    version('3.14.0', sha256='3c2453185f69ae9a0a98b32ee236f27efa668ff6ac0d920511bdf1eff10aba9f')
    version('3.13.2', sha256='08584bdb0fc11bbe509934a7c9cc4c52a77b5f348e9e73d167bc8d0a93027850')
    version('3.13.1', sha256='d92434c545b1cab618266d096d7b8fa2e9146c7f0efbb235840997daf4a4312d')
    version('3.13.0', sha256='c14704190ff9d8ab21262601284925a54aab916baf1363a11525e9ec1a37e76b')
    version('3.12.1', sha256='060bab661f549459b0de63002347d677cf4ffcfb8c5e56ec077973c1dce2bb0d')
    version('3.12.0', sha256='5f8a74571065858ddc81dd2d3859de99cd64db5fe37496d194de9e68fb9742c8')
    version('3.11.2', sha256='d21d3715e2999e2b56955790ec6534952cd85012919721c0cb5eac925e97d7fe')
    version('2.0.2', sha256='9fbe531108a95bc61518b61c4718e2661fc81d32b54fd6af34799bf10a367a6b')

    depends_on('py-setuptools', type='build')
    depends_on('py-six@1.9.0:', type=('build', 'run'))
