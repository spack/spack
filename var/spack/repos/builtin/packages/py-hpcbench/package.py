##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class PyHpcbench(PythonPackage):
    """Define and run your benchmarks"""

    homepage = "https://github.com/BlueBrain/hpcbench"

    url      = "https://pypi.io/packages/source/h/hpcbench/hpcbench-0.8.tar.gz"
    git      = "https://github.com/BlueBrain/hpcbench.git"

    version('develop', branch='master')
    version('0.8', sha256='120f5b1e6ff05a944b34a910f3099b4b0f50e96c60cf550b8fc6c42f64194697')

    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm', type='build')
    depends_on('py-cached-property')
    depends_on('py-clustershell')
    depends_on('py-cookiecutter')
    depends_on('py-docopt')
    depends_on('py-elasticsearch')
    depends_on('py-jinja2')
    depends_on('py-mock', type='test')
    depends_on('py-numpy')
    depends_on('py-pyyaml')
    depends_on('py-magic')
    depends_on('py-six')
