# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class PyGreenlet(PythonPackage):
    """Lightweight in-process concurrent programming"""

    homepage = "https://github.com/python-greenlet/greenlet"
    pypi = "greenlet/greenlet-0.4.17.tar.gz"

    version('1.1.2', sha256='e30f5ea4ae2346e62cedde8794a56858a67b878dd79f7df76a0767e356b1744a')
    version('1.1.0', sha256='c87df8ae3f01ffb4483c796fe1b15232ce2b219f0b18126948616224d3f658ee')
    version('0.4.17', sha256='41d8835c69a78de718e466dd0e6bfd4b46125f21a67c3ff6d76d8d8059868d6b')
    version('0.4.13', sha256='0fef83d43bf87a5196c91e73cb9772f945a4caaff91242766c5916d1dd1381e4')

    depends_on('python@2.7:2.8,3.5:', when='@1:', type=('build', 'link', 'run'))
    depends_on('python', when='@:0.9', type=('build', 'link', 'run'))
    depends_on('py-setuptools', type='build')
