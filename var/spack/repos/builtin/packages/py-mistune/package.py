# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMistune(PythonPackage):
    """
    Python markdown parser
    """
    homepage = "http://mistune.readthedocs.org/en/latest/"
    url      = "https://github.com/lepture/mistune/archive/v0.7.1.tar.gz"

    version('0.7.1', sha256='d6684534174caa30e0169e106a7152aee14507796a610b76be9fe9b335b18410')
    version('0.7', sha256='9b2cac8053d21dde5f2b3edb01948dac8ee5c3a85eeeeb6913c3ddf2f773c7b6')
    version('0.6', sha256='c2d976c06c099edb525b8ac3745f3d3b5c49af6189edb6de390ddf9c248913cf')
    version('0.5.1', sha256='c4ecfbb99acbb034c4f4580496502bde6b33f3dfc47873c59ee7e509c05dc822')
    version('0.5', sha256='3320b7fd80e44a1ac27658e19e67215f464c080b02c8af9fce57050d411560d2')

    depends_on('py-setuptools', type='build')
