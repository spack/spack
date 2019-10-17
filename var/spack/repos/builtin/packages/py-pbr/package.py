# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPbr(PythonPackage):
    """PBR is a library that injects some useful and sensible default
       behaviors into your setuptools run."""
    homepage = "https://pypi.python.org/pypi/pbr"
    url      = "https://pypi.io/packages/source/p/pbr/pbr-1.10.0.tar.gz"

    version('3.1.1', sha256='05f61c71aaefc02d8e37c0a3eeb9815ff526ea28b3b76324769e6158d7f95be1')
    version('2.0.0', sha256='0ccd2db529afd070df815b1521f01401d43de03941170f8a800e7531faba265d')
    version('1.10.0', sha256='186428c270309e6fdfe2d5ab0949ab21ae5f7dea831eab96701b86bd666af39c')
    version('1.8.1', sha256='e2127626a91e6c885db89668976db31020f0af2da728924b56480fc7ccf09649')

    depends_on('py-setuptools', type='build')
    # Only needed for py<3.4, however when='^python@:3.4.2' syntax might be
    # broken, if this fails, remove the when-clause
    depends_on('py-enum34', type='build', when='^python@:3.3')
