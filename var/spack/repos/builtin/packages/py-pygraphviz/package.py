# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class PyPygraphviz(PythonPackage):
    """Python interface to Graphviz"""

    homepage = "https://pygraphviz.github.io/"
    pypi     = "pygraphviz/pygraphviz-1.7.zip"

    maintainers = ['haralmha']

    version('1.7', sha256='a7bec6609f37cf1e64898c59f075afd659106cf9356c5f387cecaa2e0cdb2304')

    depends_on('python@3.7:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('graphviz')
