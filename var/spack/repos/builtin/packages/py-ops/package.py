# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyOps(PythonPackage):
    """The Python library behind great charms"""

    homepage = "https://github.com/canonical/operator"
    pypi     = "ops/ops-1.4.0.tar.gz"

    version('1.4.0', sha256='6bb7c8d8cd3eb1da99469564e37a04f9677205c4c07ef97167e0b93a17ccb59a')

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-pyyaml', type=('build', 'run'))
