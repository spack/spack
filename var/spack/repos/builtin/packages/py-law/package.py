# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLaw(PythonPackage):
    """Build large-scale task workflows using luigi,
       remote job submission, remote targets, and environment"""

    homepage = "https://github.com/riga/law"
    pypi     = "law/law-0.1.6.tar.gz"

    version('0.1.6', sha256='17c2c1837080590bff4d2e7228bfb418733f11b60e2bac8f589e68da78cf2ab8')

    depends_on('python@2.7:2,3.3:3', type=('build', 'run'))
    depends_on('py-setuptools',       type='build')
    depends_on('py-six@1.13:',        type=('build', 'run'))
    depends_on('py-luigi@2.8.2:2',    type=('build', 'run'), when='^python@:2.7')
    depends_on('py-luigi@2.8.2:',     type=('build', 'run'), when='^python@3:')
